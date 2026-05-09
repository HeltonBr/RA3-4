# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass

from analisador_sintatico_ll1.ast_nodes import AstNode
from analisador_sintatico_ll1.ast_nodes import BinaryOpNode
from analisador_sintatico_ll1.ast_nodes import BoolNode
from analisador_sintatico_ll1.ast_nodes import IfNode
from analisador_sintatico_ll1.ast_nodes import LogicalNotNode
from analisador_sintatico_ll1.ast_nodes import LogicalOpNode
from analisador_sintatico_ll1.ast_nodes import MemoryReadNode
from analisador_sintatico_ll1.ast_nodes import MemoryWriteNode
from analisador_sintatico_ll1.ast_nodes import NumberNode
from analisador_sintatico_ll1.ast_nodes import ProgramNode
from analisador_sintatico_ll1.ast_nodes import RelationalOpNode
from analisador_sintatico_ll1.ast_nodes import ResultRefNode
from analisador_sintatico_ll1.ast_nodes import SequenceNode
from analisador_sintatico_ll1.ast_nodes import WhileNode
from analisador_sintatico_ll1.ast_nodes import node_to_rpn_string
from analisador_sintatico_ll1.errors import AssemblyGenerationError


@dataclass
class ARMProgramContext:
    result_label_by_index: dict[int, str]
    memory_label_by_name: dict[str, str]
    const_label_by_value: dict[str, str]
    const_lines: list[str]
    const_counter: int = 0
    label_counter: int = 0

    def get_const_label(self, value: float) -> str:
        key = float_key(value)
        if key not in self.const_label_by_value:
            label = f"const_{self.const_counter}"
            self.const_counter += 1
            self.const_label_by_value[key] = label
            self.const_lines.append("    .balign 8")
            self.const_lines.append(f"{label}:")
            self.const_lines.append(f"    .double {repr(value)}")
        return self.const_label_by_value[key]

    def new_label(self, base: str) -> str:
        label = f"{base}_{self.label_counter}"
        self.label_counter += 1
        return label


def gerarAssembly(arvore: dict[str, object]) -> str:
    program = arvore.get("_ast")
    if not isinstance(program, ProgramNode):
        raise AssemblyGenerationError("A arvore informada nao contem a AST interna esperada.")
    return "\n".join(build_armv7_program(program)) + "\n"


def build_armv7_program(program: ProgramNode) -> list[str]:
    result_label_by_index = {
        statement.ordinal: f"result_line_{statement.ordinal}" for statement in program.statements
    }

    identifiers: set[str] = set()
    for statement in program.statements:
        collect_identifiers(statement.node, identifiers)

    memory_label_by_name = {
        name: f"mem_{sanitize_symbol_name(name)}" for name in sorted(identifiers)
    }

    const_lines: list[str] = []
    ctx = ARMProgramContext(
        result_label_by_index=result_label_by_index,
        memory_label_by_name=memory_label_by_name,
        const_label_by_value={},
        const_lines=const_lines,
    )

    max_temp_slots = 0
    for statement in program.statements:
        max_temp_slots = max(max_temp_slots, count_temp_slots(statement.node))
    temp_labels = [f"tmp_slot_{indice}" for indice in range(max_temp_slots)]

    lines: list[str] = [
        ".syntax unified",
        ".arch armv7-a",
        ".fpu vfpv3",
        ".global _start",
        "",
        ".text",
        "_start:",
        "    @ Programa gerado automaticamente a partir da arvore atribuida da Fase 3",
        "",
    ]

    for statement in program.statements:
        msg_label = f"msg_line_{statement.ordinal}"
        result_label = result_label_by_index[statement.ordinal]

        lines.append("    .balign 4")
        lines.append("    @ ================================================")
        lines.append(f"    @ LINHA {statement.source_line}")
        lines.append(f"    @ {node_to_rpn_string(statement.node)}")
        lines.append("    @ ================================================")

        emit_node_armv7(statement.node, lines, ctx, statement.ordinal, temp_labels.copy())
        emit_store_label_double(lines, result_label, "d0")
        lines.append(f"    ldr r0, ={msg_label}")
        lines.append("    bl puts_jtag")
        lines.append("    bl print_qword_hex_d0")
        lines.append("    bl print_newline")
        lines.append("")

    lines.extend(
        [
            "program_end:",
            "    b program_end",
        ]
    )

    emit_runtime_helpers(lines)

    lines.extend(
        [
            "",
            ".data",
            "    .balign 8",
            "const_zero_runtime:",
            "    .double 0.0",
            "    .balign 8",
            "const_one_runtime:",
            "    .double 1.0",
            "",
        ]
    )

    for statement in program.statements:
        lines.append("    .balign 4")
        lines.append(f"msg_line_{statement.ordinal}:")
        lines.append(f'    .asciz "L{statement.source_line}: 0x"')
    if program.statements:
        lines.append("")

    if result_label_by_index:
        lines.append("    .balign 8")
        for result_label in result_label_by_index.values():
            lines.append(f"{result_label}:")
            lines.append("    .double 0.0")
        lines.append("")

    if memory_label_by_name:
        lines.append("    .balign 8")
        for memory_label in memory_label_by_name.values():
            lines.append(f"{memory_label}:")
            lines.append("    .double 0.0")
        lines.append("")

    if temp_labels:
        lines.append("    .balign 8")
        for temp_label in temp_labels:
            lines.append(f"{temp_label}:")
            lines.append("    .double 0.0")
        lines.append("")

    lines.extend(const_lines)
    lines.append("")
    return lines


def emit_node_armv7(
    node: AstNode,
    lines: list[str],
    ctx: ARMProgramContext,
    current_statement_index: int,
    temp_pool: list[str],
) -> None:
    if isinstance(node, NumberNode):
        emit_load_const(lines, ctx, node.value, "d0")
        return

    if isinstance(node, BoolNode):
        emit_load_const(lines, ctx, 1.0 if node.value else 0.0, "d0")
        return

    if isinstance(node, MemoryReadNode):
        emit_load_label_double(lines, ctx.memory_label_by_name[node.name], "d0")
        return

    if isinstance(node, ResultRefNode):
        history_index = current_statement_index - node.offset
        if history_index < 1 or history_index not in ctx.result_label_by_index:
            raise AssemblyGenerationError(
                f"RES invalido: nao existe resultado {node.offset} linhas atras."
            )
        emit_load_label_double(lines, ctx.result_label_by_index[history_index], "d0")
        return

    if isinstance(node, MemoryWriteNode):
        emit_node_armv7(node.value, lines, ctx, current_statement_index, temp_pool)
        emit_store_label_double(lines, ctx.memory_label_by_name[node.name], "d0")
        return

    if isinstance(node, BinaryOpNode):
        _emit_binary_op(node, lines, ctx, current_statement_index, temp_pool)
        return

    if isinstance(node, RelationalOpNode):
        _emit_relational_op(node, lines, ctx, current_statement_index, temp_pool)
        return

    if isinstance(node, LogicalOpNode):
        _emit_logical_op(node, lines, ctx, current_statement_index, temp_pool)
        return

    if isinstance(node, LogicalNotNode):
        _emit_logical_not(node, lines, ctx, current_statement_index, temp_pool)
        return

    if isinstance(node, SequenceNode):
        emit_node_armv7(node.first, lines, ctx, current_statement_index, temp_pool.copy())
        emit_node_armv7(node.second, lines, ctx, current_statement_index, temp_pool.copy())
        return

    if isinstance(node, IfNode):
        _emit_if(node, lines, ctx, current_statement_index, temp_pool)
        return

    if isinstance(node, WhileNode):
        _emit_while(node, lines, ctx, current_statement_index, temp_pool)
        return

    raise AssemblyGenerationError(f"No de AST desconhecido: {type(node)!r}")


def _emit_truthy_branch(lines: list[str], ctx: ARMProgramContext, target_label: str) -> None:
    emit_load_const(lines, ctx, 0.0, "d1")
    lines.append("    vcmp.f64 d0, d1")
    lines.append("    vmrs APSR_nzcv, fpscr")
    lines.append(f"    bne {target_label}")


def _emit_logical_op(
    node: LogicalOpNode,
    lines: list[str],
    ctx: ARMProgramContext,
    current_statement_index: int,
    temp_pool: list[str],
) -> None:
    if len(temp_pool) < 2:
        raise AssemblyGenerationError("Pilha temporaria insuficiente para operacao logica.")

    temp_left = temp_pool.pop(0)
    temp_right = temp_pool.pop(0)
    emit_node_armv7(node.left, lines, ctx, current_statement_index, temp_pool.copy())
    emit_store_label_double(lines, temp_left, "d0")
    emit_node_armv7(node.right, lines, ctx, current_statement_index, temp_pool.copy())
    emit_store_label_double(lines, temp_right, "d0")

    label_true = ctx.new_label("logic_true")
    label_false = ctx.new_label("logic_false")
    label_end = ctx.new_label("logic_end")

    if node.operator == "AND":
        emit_load_label_double(lines, temp_left, "d0")
        emit_load_const(lines, ctx, 0.0, "d1")
        lines.append("    vcmp.f64 d0, d1")
        lines.append("    vmrs APSR_nzcv, fpscr")
        lines.append(f"    beq {label_false}")
        emit_load_label_double(lines, temp_right, "d0")
        _emit_truthy_branch(lines, ctx, label_true)
        lines.append(f"    b {label_false}")
    elif node.operator == "OR":
        emit_load_label_double(lines, temp_left, "d0")
        _emit_truthy_branch(lines, ctx, label_true)
        emit_load_label_double(lines, temp_right, "d0")
        _emit_truthy_branch(lines, ctx, label_true)
        lines.append(f"    b {label_false}")
    else:
        raise AssemblyGenerationError(f"Operador logico nao suportado: {node.operator}")

    lines.append(f"{label_true}:")
    emit_load_const(lines, ctx, 1.0, "d0")
    lines.append(f"    b {label_end}")
    lines.append(f"{label_false}:")
    emit_load_const(lines, ctx, 0.0, "d0")
    lines.append(f"{label_end}:")


def _emit_logical_not(
    node: LogicalNotNode,
    lines: list[str],
    ctx: ARMProgramContext,
    current_statement_index: int,
    temp_pool: list[str],
) -> None:
    label_true = ctx.new_label("not_true")
    label_end = ctx.new_label("not_end")
    emit_node_armv7(node.operand, lines, ctx, current_statement_index, temp_pool.copy())
    emit_load_const(lines, ctx, 0.0, "d1")
    lines.append("    vcmp.f64 d0, d1")
    lines.append("    vmrs APSR_nzcv, fpscr")
    lines.append(f"    beq {label_true}")
    emit_load_const(lines, ctx, 0.0, "d0")
    lines.append(f"    b {label_end}")
    lines.append(f"{label_true}:")
    emit_load_const(lines, ctx, 1.0, "d0")
    lines.append(f"{label_end}:")


def _emit_binary_op(
    node: BinaryOpNode,
    lines: list[str],
    ctx: ARMProgramContext,
    current_statement_index: int,
    temp_pool: list[str],
) -> None:
    if len(temp_pool) < 2:
        raise AssemblyGenerationError("Pilha temporaria insuficiente para operacao binaria.")

    temp_left = temp_pool.pop(0)
    temp_right = temp_pool.pop(0)

    emit_node_armv7(node.left, lines, ctx, current_statement_index, temp_pool.copy())
    emit_store_label_double(lines, temp_left, "d0")
    emit_node_armv7(node.right, lines, ctx, current_statement_index, temp_pool.copy())
    emit_store_label_double(lines, temp_right, "d0")

    emit_load_label_double(lines, temp_left, "d0")
    emit_load_label_double(lines, temp_right, "d1")

    if node.operator == "+":
        lines.append("    vadd.f64 d0, d0, d1")
        return
    if node.operator == "-":
        lines.append("    vsub.f64 d0, d0, d1")
        return
    if node.operator == "*":
        lines.append("    vmul.f64 d0, d0, d1")
        return
    if node.operator == "|":
        lines.append("    vdiv.f64 d0, d0, d1")
        return
    if node.operator == "^":
        lines.append("    bl pow_double_int")
        return
    if node.operator == "/":
        lines.append("    bl intdiv_double")
        return
    if node.operator == "%":
        lines.append("    bl mod_double")
        return

    raise AssemblyGenerationError(f"Operador aritmetico nao suportado: {node.operator}")


def _emit_relational_op(
    node: RelationalOpNode,
    lines: list[str],
    ctx: ARMProgramContext,
    current_statement_index: int,
    temp_pool: list[str],
) -> None:
    if len(temp_pool) < 2:
        raise AssemblyGenerationError("Pilha temporaria insuficiente para operacao relacional.")

    temp_left = temp_pool.pop(0)
    temp_right = temp_pool.pop(0)
    emit_node_armv7(node.left, lines, ctx, current_statement_index, temp_pool.copy())
    emit_store_label_double(lines, temp_left, "d0")
    emit_node_armv7(node.right, lines, ctx, current_statement_index, temp_pool.copy())
    emit_store_label_double(lines, temp_right, "d0")

    emit_load_label_double(lines, temp_left, "d0")
    emit_load_label_double(lines, temp_right, "d1")
    lines.append("    vcmp.f64 d0, d1")
    lines.append("    vmrs APSR_nzcv, fpscr")

    label_true = ctx.new_label("rel_true")
    label_end = ctx.new_label("rel_end")
    branch_map = {
        ">": "bgt",
        "<": "blt",
        ">=": "bge",
        "<=": "ble",
        "==": "beq",
        "!=": "bne",
    }
    branch = branch_map.get(node.operator)
    if branch is None:
        raise AssemblyGenerationError(f"Operador relacional nao suportado: {node.operator}")

    lines.append(f"    {branch} {label_true}")
    emit_load_const(lines, ctx, 0.0, "d0")
    lines.append(f"    b {label_end}")
    lines.append(f"{label_true}:")
    emit_load_const(lines, ctx, 1.0, "d0")
    lines.append(f"{label_end}:")


def _emit_if(
    node: IfNode,
    lines: list[str],
    ctx: ARMProgramContext,
    current_statement_index: int,
    temp_pool: list[str],
) -> None:
    label_else = ctx.new_label("if_else")
    label_end = ctx.new_label("if_end")

    emit_node_armv7(node.condition, lines, ctx, current_statement_index, temp_pool.copy())
    emit_load_const(lines, ctx, 0.0, "d1")
    lines.append("    vcmp.f64 d0, d1")
    lines.append("    vmrs APSR_nzcv, fpscr")
    lines.append(f"    beq {label_else}")
    emit_node_armv7(node.then_branch, lines, ctx, current_statement_index, temp_pool.copy())
    lines.append(f"    b {label_end}")
    lines.append(f"{label_else}:")
    if node.else_branch is None:
        emit_load_const(lines, ctx, 0.0, "d0")
    else:
        emit_node_armv7(node.else_branch, lines, ctx, current_statement_index, temp_pool.copy())
    lines.append(f"{label_end}:")


def _emit_while(
    node: WhileNode,
    lines: list[str],
    ctx: ARMProgramContext,
    current_statement_index: int,
    temp_pool: list[str],
) -> None:
    if not temp_pool:
        raise AssemblyGenerationError("Pilha temporaria insuficiente para WHILE.")

    result_slot = temp_pool.pop(0)
    label_start = ctx.new_label("while_start")
    label_end = ctx.new_label("while_end")

    emit_load_const(lines, ctx, 0.0, "d0")
    emit_store_label_double(lines, result_slot, "d0")
    lines.append(f"{label_start}:")
    emit_node_armv7(node.condition, lines, ctx, current_statement_index, temp_pool.copy())
    emit_load_const(lines, ctx, 0.0, "d1")
    lines.append("    vcmp.f64 d0, d1")
    lines.append("    vmrs APSR_nzcv, fpscr")
    lines.append(f"    beq {label_end}")
    emit_node_armv7(node.body, lines, ctx, current_statement_index, temp_pool.copy())
    emit_store_label_double(lines, result_slot, "d0")
    lines.append(f"    b {label_start}")
    lines.append(f"{label_end}:")
    emit_load_label_double(lines, result_slot, "d0")


def collect_identifiers(node: AstNode, out: set[str]) -> None:
    if isinstance(node, MemoryReadNode):
        out.add(node.name)
        return
    if isinstance(node, ResultRefNode):
        return
    if isinstance(node, (NumberNode, BoolNode)):
        return
    if isinstance(node, MemoryWriteNode):
        out.add(node.name)
        collect_identifiers(node.value, out)
        return
    if isinstance(node, (BinaryOpNode, RelationalOpNode, LogicalOpNode)):
        collect_identifiers(node.left, out)
        collect_identifiers(node.right, out)
        return
    if isinstance(node, LogicalNotNode):
        collect_identifiers(node.operand, out)
        return
    if isinstance(node, SequenceNode):
        collect_identifiers(node.first, out)
        collect_identifiers(node.second, out)
        return
    if isinstance(node, IfNode):
        collect_identifiers(node.condition, out)
        collect_identifiers(node.then_branch, out)
        if node.else_branch is not None:
            collect_identifiers(node.else_branch, out)
        return
    if isinstance(node, WhileNode):
        collect_identifiers(node.condition, out)
        collect_identifiers(node.body, out)
        return


def count_temp_slots(node: AstNode) -> int:
    if isinstance(node, (NumberNode, BoolNode, MemoryReadNode, ResultRefNode)):
        return 0
    if isinstance(node, MemoryWriteNode):
        return count_temp_slots(node.value)
    if isinstance(node, (BinaryOpNode, RelationalOpNode, LogicalOpNode)):
        return 2 + count_temp_slots(node.left) + count_temp_slots(node.right)
    if isinstance(node, LogicalNotNode):
        return count_temp_slots(node.operand)
    if isinstance(node, SequenceNode):
        return max(count_temp_slots(node.first), count_temp_slots(node.second))
    if isinstance(node, IfNode):
        ramo_else = count_temp_slots(node.else_branch) if node.else_branch is not None else 0
        return max(count_temp_slots(node.condition), count_temp_slots(node.then_branch), ramo_else)
    if isinstance(node, WhileNode):
        return 1 + max(count_temp_slots(node.condition), count_temp_slots(node.body))
    raise AssemblyGenerationError(f"No de AST desconhecido: {type(node)!r}")


def float_key(value: float) -> str:
    return f"{value:.17g}"


def sanitize_symbol_name(name: str) -> str:
    return "".join(caractere if caractere.isalnum() else "_" for caractere in name)


def emit_load_const(lines: list[str], ctx: ARMProgramContext, value: float, target_dreg: str) -> None:
    const_label = ctx.get_const_label(value)
    lines.append(f"    ldr r0, ={const_label}")
    lines.append(f"    vldr {target_dreg}, [r0]")


def emit_load_label_double(lines: list[str], label: str, target_dreg: str) -> None:
    lines.append(f"    ldr r0, ={label}")
    lines.append(f"    vldr {target_dreg}, [r0]")


def emit_store_label_double(lines: list[str], label: str, source_dreg: str) -> None:
    lines.append(f"    ldr r0, ={label}")
    lines.append(f"    vstr {source_dreg}, [r0]")


def emit_runtime_helpers(lines: list[str]) -> None:
    lines.extend(
        [
            "",
            "@ ====================================================",
            "@ RUNTIME JTAG UART + VFP",
            "@ ====================================================",
            "",
            "jtag_putc:",
            "    push {r1, r2, lr}",
            "jtag_putc_wait:",
            "    ldr r1, =0xFF201000",
            "    ldr r2, [r1, #4]",
            "    mov r2, r2, lsr #16",
            "    cmp r2, #0",
            "    beq jtag_putc_wait",
            "    str r0, [r1]",
            "    pop {r1, r2, lr}",
            "    bx lr",
            "",
            "puts_jtag:",
            "    push {r1, r2, lr}",
            "    mov r2, r0",
            "puts_jtag_loop:",
            "    ldrb r1, [r2], #1",
            "    cmp r1, #0",
            "    beq puts_jtag_done",
            "    mov r0, r1",
            "    bl jtag_putc",
            "    b puts_jtag_loop",
            "puts_jtag_done:",
            "    pop {r1, r2, lr}",
            "    bx lr",
            "",
            "print_nibble:",
            "    and r0, r0, #0xF",
            "    cmp r0, #9",
            "    addle r0, r0, #'0'",
            "    addgt r0, r0, #55",
            "    b jtag_putc",
            "",
            "print_hex32:",
            "    push {r1, r2, lr}",
            "    mov r1, r0",
            "    mov r2, #28",
            "print_hex32_loop:",
            "    mov r0, r1, lsr r2",
            "    bl print_nibble",
            "    subs r2, r2, #4",
            "    bpl print_hex32_loop",
            "    pop {r1, r2, lr}",
            "    bx lr",
            "",
            "print_qword_hex_d0:",
            "    push {r2, r3, lr}",
            "    vmov r2, r3, d0",
            "    mov r0, r2",
            "    bl print_hex32",
            "    mov r0, r3",
            "    bl print_hex32",
            "    pop {r2, r3, lr}",
            "    bx lr",
            "",
            "print_newline:",
            "    push {lr}",
            "    mov r0, #10",
            "    bl jtag_putc",
            "    pop {lr}",
            "    bx lr",
            "",
            "pow_double_int:",
            "    push {r4, lr}",
            "    vcvt.s32.f64 s4, d1",
            "    vmov r4, s4",
            "    cmp r4, #0",
            "    blt pow_double_int_neg",
            "    beq pow_double_int_zero",
            "    vmov.f64 d2, d0",
            "pow_double_int_loop:",
            "    subs r4, r4, #1",
            "    beq pow_double_int_done",
            "    vmul.f64 d0, d0, d2",
            "    b pow_double_int_loop",
            "pow_double_int_zero:",
            "    ldr r0, =const_one_runtime",
            "    vldr d0, [r0]",
            "    pop {r4, lr}",
            "    bx lr",
            "pow_double_int_neg:",
            "    ldr r0, =const_zero_runtime",
            "    vldr d0, [r0]",
            "    pop {r4, lr}",
            "    bx lr",
            "pow_double_int_done:",
            "    pop {r4, lr}",
            "    bx lr",
            "",
            "signed_divmod32:",
            "    mov r2, #0",
            "    mov r3, #0",
            "    mov r12, #0",
            "    cmp r1, #0",
            "    beq signed_divmod32_done",
            "    cmp r0, #0",
            "    bge signed_divmod32_dividend_ok",
            "    rsb r0, r0, #0",
            "    mov r3, #1",
            "signed_divmod32_dividend_ok:",
            "    cmp r1, #0",
            "    bge signed_divmod32_divisor_ok",
            "    rsb r1, r1, #0",
            "    mov r12, #1",
            "signed_divmod32_divisor_ok:",
            "signed_divmod32_loop:",
            "    cmp r0, r1",
            "    blt signed_divmod32_after_loop",
            "    sub r0, r0, r1",
            "    add r2, r2, #1",
            "    b signed_divmod32_loop",
            "signed_divmod32_after_loop:",
            "    eor r12, r3, r12",
            "    cmp r12, #0",
            "    beq signed_divmod32_sign_q_done",
            "    rsb r2, r2, #0",
            "signed_divmod32_sign_q_done:",
            "    cmp r3, #0",
            "    beq signed_divmod32_finish",
            "    rsb r0, r0, #0",
            "signed_divmod32_finish:",
            "    mov r1, r0",
            "    mov r0, r2",
            "    bx lr",
            "signed_divmod32_done:",
            "    mov r0, #0",
            "    mov r1, #0",
            "    bx lr",
            "",
            "intdiv_double:",
            "    push {r2, lr}",
            "    vcvt.s32.f64 s4, d0",
            "    vcvt.s32.f64 s5, d1",
            "    vmov r0, s4",
            "    vmov r1, s5",
            "    cmp r1, #0",
            "    beq intdiv_by_zero",
            "    bl signed_divmod32",
            "    vmov s6, r0",
            "    vcvt.f64.s32 d0, s6",
            "    pop {r2, lr}",
            "    bx lr",
            "intdiv_by_zero:",
            "    ldr r0, =const_zero_runtime",
            "    vldr d0, [r0]",
            "    pop {r2, lr}",
            "    bx lr",
            "",
            "mod_double:",
            "    push {r2, lr}",
            "    vcvt.s32.f64 s4, d0",
            "    vcvt.s32.f64 s5, d1",
            "    vmov r0, s4",
            "    vmov r1, s5",
            "    cmp r1, #0",
            "    beq mod_by_zero",
            "    bl signed_divmod32",
            "    vmov s6, r1",
            "    vcvt.f64.s32 d0, s6",
            "    pop {r2, lr}",
            "    bx lr",
            "mod_by_zero:",
            "    ldr r0, =const_zero_runtime",
            "    vldr d0, [r0]",
            "    pop {r2, lr}",
            "    bx lr",
        ]
    )
