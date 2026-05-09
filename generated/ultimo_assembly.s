.syntax unified
.arch armv7-a
.fpu vfpv3
.global _start

.text
_start:
    @ Programa gerado automaticamente a partir da arvore atribuida da Fase 3

    .balign 4
    @ ================================================
    @ LINHA 3
    @ (12 N)
    @ ================================================
    ldr r0, =const_0
    vldr d0, [r0]
    ldr r0, =mem_N
    vstr d0, [r0]
    ldr r0, =result_line_1
    vstr d0, [r0]
    ldr r0, =msg_line_1
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 4
    @ (4 D)
    @ ================================================
    ldr r0, =const_1
    vldr d0, [r0]
    ldr r0, =mem_D
    vstr d0, [r0]
    ldr r0, =result_line_2
    vstr d0, [r0]
    ldr r0, =msg_line_2
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 5
    @ (3.25 TAXA)
    @ ================================================
    ldr r0, =const_2
    vldr d0, [r0]
    ldr r0, =mem_TAXA
    vstr d0, [r0]
    ldr r0, =result_line_3
    vstr d0, [r0]
    ldr r0, =msg_line_3
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 6
    @ (TRUE ATIVO)
    @ ================================================
    ldr r0, =const_3
    vldr d0, [r0]
    ldr r0, =mem_ATIVO
    vstr d0, [r0]
    ldr r0, =result_line_4
    vstr d0, [r0]
    ldr r0, =msg_line_4
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 7
    @ ((N) (D) +)
    @ ================================================
    ldr r0, =mem_N
    vldr d0, [r0]
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =mem_D
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d1, [r0]
    vadd.f64 d0, d0, d1
    ldr r0, =result_line_5
    vstr d0, [r0]
    ldr r0, =msg_line_5
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 8
    @ (((N) (D) +) 2 -)
    @ ================================================
    ldr r0, =mem_N
    vldr d0, [r0]
    ldr r0, =tmp_slot_2
    vstr d0, [r0]
    ldr r0, =mem_D
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vstr d0, [r0]
    ldr r0, =tmp_slot_2
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vldr d1, [r0]
    vadd.f64 d0, d0, d1
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =const_4
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d1, [r0]
    vsub.f64 d0, d0, d1
    ldr r0, =result_line_6
    vstr d0, [r0]
    ldr r0, =msg_line_6
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 9
    @ (((N) 2 *) ((D) 3 *) +)
    @ ================================================
    ldr r0, =mem_N
    vldr d0, [r0]
    ldr r0, =tmp_slot_2
    vstr d0, [r0]
    ldr r0, =const_4
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vstr d0, [r0]
    ldr r0, =tmp_slot_2
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vldr d1, [r0]
    vmul.f64 d0, d0, d1
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =mem_D
    vldr d0, [r0]
    ldr r0, =tmp_slot_2
    vstr d0, [r0]
    ldr r0, =const_5
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vstr d0, [r0]
    ldr r0, =tmp_slot_2
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vldr d1, [r0]
    vmul.f64 d0, d0, d1
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d1, [r0]
    vadd.f64 d0, d0, d1
    ldr r0, =result_line_7
    vstr d0, [r0]
    ldr r0, =msg_line_7
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 10
    @ (27 5 /)
    @ ================================================
    ldr r0, =const_6
    vldr d0, [r0]
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =const_7
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d1, [r0]
    bl intdiv_double
    ldr r0, =result_line_8
    vstr d0, [r0]
    ldr r0, =msg_line_8
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 11
    @ (27.0 5 |)
    @ ================================================
    ldr r0, =const_6
    vldr d0, [r0]
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =const_7
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d1, [r0]
    vdiv.f64 d0, d0, d1
    ldr r0, =result_line_9
    vstr d0, [r0]
    ldr r0, =msg_line_9
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 12
    @ (27 5 %)
    @ ================================================
    ldr r0, =const_6
    vldr d0, [r0]
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =const_7
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d1, [r0]
    bl mod_double
    ldr r0, =result_line_10
    vstr d0, [r0]
    ldr r0, =msg_line_10
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 13
    @ ((D) 2 ^)
    @ ================================================
    ldr r0, =mem_D
    vldr d0, [r0]
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =const_4
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d1, [r0]
    bl pow_double_int
    ldr r0, =result_line_11
    vstr d0, [r0]
    ldr r0, =msg_line_11
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 14
    @ ((2 RES) (1 RES) +)
    @ ================================================
    ldr r0, =result_line_10
    vldr d0, [r0]
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =result_line_11
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d1, [r0]
    vadd.f64 d0, d0, d1
    ldr r0, =result_line_12
    vstr d0, [r0]
    ldr r0, =msg_line_12
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 15
    @ (((N) (D) >=) (ATIVO) AND)
    @ ================================================
    ldr r0, =mem_N
    vldr d0, [r0]
    ldr r0, =tmp_slot_2
    vstr d0, [r0]
    ldr r0, =mem_D
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vstr d0, [r0]
    ldr r0, =tmp_slot_2
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    bge rel_true_0
    ldr r0, =const_8
    vldr d0, [r0]
    b rel_end_1
rel_true_0:
    ldr r0, =const_3
    vldr d0, [r0]
rel_end_1:
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =mem_ATIVO
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =const_8
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    beq logic_false_3
    ldr r0, =tmp_slot_1
    vldr d0, [r0]
    ldr r0, =const_8
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    bne logic_true_2
    b logic_false_3
logic_true_2:
    ldr r0, =const_3
    vldr d0, [r0]
    b logic_end_4
logic_false_3:
    ldr r0, =const_8
    vldr d0, [r0]
logic_end_4:
    ldr r0, =result_line_13
    vstr d0, [r0]
    ldr r0, =msg_line_13
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 16
    @ ((((N) (D) >) (ATIVO) AND) (((N) (D) -) N) IF)
    @ ================================================
    ldr r0, =mem_N
    vldr d0, [r0]
    ldr r0, =tmp_slot_2
    vstr d0, [r0]
    ldr r0, =mem_D
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vstr d0, [r0]
    ldr r0, =tmp_slot_2
    vldr d0, [r0]
    ldr r0, =tmp_slot_3
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    bgt rel_true_7
    ldr r0, =const_8
    vldr d0, [r0]
    b rel_end_8
rel_true_7:
    ldr r0, =const_3
    vldr d0, [r0]
rel_end_8:
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =mem_ATIVO
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =const_8
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    beq logic_false_10
    ldr r0, =tmp_slot_1
    vldr d0, [r0]
    ldr r0, =const_8
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    bne logic_true_9
    b logic_false_10
logic_true_9:
    ldr r0, =const_3
    vldr d0, [r0]
    b logic_end_11
logic_false_10:
    ldr r0, =const_8
    vldr d0, [r0]
logic_end_11:
    ldr r0, =const_8
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    beq if_else_5
    ldr r0, =mem_N
    vldr d0, [r0]
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    ldr r0, =mem_D
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d1, [r0]
    vsub.f64 d0, d0, d1
    ldr r0, =mem_N
    vstr d0, [r0]
    b if_end_6
if_else_5:
    ldr r0, =const_8
    vldr d0, [r0]
if_end_6:
    ldr r0, =result_line_14
    vstr d0, [r0]
    ldr r0, =msg_line_14
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

    .balign 4
    @ ================================================
    @ LINHA 17
    @ (((N) 0 >) (((N) 1 -) N) WHILE)
    @ ================================================
    ldr r0, =const_8
    vldr d0, [r0]
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
while_start_12:
    ldr r0, =mem_N
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =const_8
    vldr d0, [r0]
    ldr r0, =tmp_slot_2
    vstr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d0, [r0]
    ldr r0, =tmp_slot_2
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    bgt rel_true_14
    ldr r0, =const_8
    vldr d0, [r0]
    b rel_end_15
rel_true_14:
    ldr r0, =const_3
    vldr d0, [r0]
rel_end_15:
    ldr r0, =const_8
    vldr d1, [r0]
    vcmp.f64 d0, d1
    vmrs APSR_nzcv, fpscr
    beq while_end_13
    ldr r0, =mem_N
    vldr d0, [r0]
    ldr r0, =tmp_slot_1
    vstr d0, [r0]
    ldr r0, =const_3
    vldr d0, [r0]
    ldr r0, =tmp_slot_2
    vstr d0, [r0]
    ldr r0, =tmp_slot_1
    vldr d0, [r0]
    ldr r0, =tmp_slot_2
    vldr d1, [r0]
    vsub.f64 d0, d0, d1
    ldr r0, =mem_N
    vstr d0, [r0]
    ldr r0, =tmp_slot_0
    vstr d0, [r0]
    b while_start_12
while_end_13:
    ldr r0, =tmp_slot_0
    vldr d0, [r0]
    ldr r0, =result_line_15
    vstr d0, [r0]
    ldr r0, =msg_line_15
    bl puts_jtag
    bl print_qword_hex_d0
    bl print_newline

program_end:
    b program_end

@ ====================================================
@ RUNTIME JTAG UART + VFP
@ ====================================================

jtag_putc:
    push {r1, r2, lr}
jtag_putc_wait:
    ldr r1, =0xFF201000
    ldr r2, [r1, #4]
    mov r2, r2, lsr #16
    cmp r2, #0
    beq jtag_putc_wait
    str r0, [r1]
    pop {r1, r2, lr}
    bx lr

puts_jtag:
    push {r1, r2, lr}
    mov r2, r0
puts_jtag_loop:
    ldrb r1, [r2], #1
    cmp r1, #0
    beq puts_jtag_done
    mov r0, r1
    bl jtag_putc
    b puts_jtag_loop
puts_jtag_done:
    pop {r1, r2, lr}
    bx lr

print_nibble:
    and r0, r0, #0xF
    cmp r0, #9
    addle r0, r0, #'0'
    addgt r0, r0, #55
    b jtag_putc

print_hex32:
    push {r1, r2, lr}
    mov r1, r0
    mov r2, #28
print_hex32_loop:
    mov r0, r1, lsr r2
    bl print_nibble
    subs r2, r2, #4
    bpl print_hex32_loop
    pop {r1, r2, lr}
    bx lr

print_qword_hex_d0:
    push {r2, r3, lr}
    vmov r2, r3, d0
    mov r0, r2
    bl print_hex32
    mov r0, r3
    bl print_hex32
    pop {r2, r3, lr}
    bx lr

print_newline:
    push {lr}
    mov r0, #10
    bl jtag_putc
    pop {lr}
    bx lr

pow_double_int:
    push {r4, lr}
    vcvt.s32.f64 s4, d1
    vmov r4, s4
    cmp r4, #0
    blt pow_double_int_neg
    beq pow_double_int_zero
    vmov.f64 d2, d0
pow_double_int_loop:
    subs r4, r4, #1
    beq pow_double_int_done
    vmul.f64 d0, d0, d2
    b pow_double_int_loop
pow_double_int_zero:
    ldr r0, =const_one_runtime
    vldr d0, [r0]
    pop {r4, lr}
    bx lr
pow_double_int_neg:
    ldr r0, =const_zero_runtime
    vldr d0, [r0]
    pop {r4, lr}
    bx lr
pow_double_int_done:
    pop {r4, lr}
    bx lr

signed_divmod32:
    mov r2, #0
    mov r3, #0
    mov r12, #0
    cmp r1, #0
    beq signed_divmod32_done
    cmp r0, #0
    bge signed_divmod32_dividend_ok
    rsb r0, r0, #0
    mov r3, #1
signed_divmod32_dividend_ok:
    cmp r1, #0
    bge signed_divmod32_divisor_ok
    rsb r1, r1, #0
    mov r12, #1
signed_divmod32_divisor_ok:
signed_divmod32_loop:
    cmp r0, r1
    blt signed_divmod32_after_loop
    sub r0, r0, r1
    add r2, r2, #1
    b signed_divmod32_loop
signed_divmod32_after_loop:
    eor r12, r3, r12
    cmp r12, #0
    beq signed_divmod32_sign_q_done
    rsb r2, r2, #0
signed_divmod32_sign_q_done:
    cmp r3, #0
    beq signed_divmod32_finish
    rsb r0, r0, #0
signed_divmod32_finish:
    mov r1, r0
    mov r0, r2
    bx lr
signed_divmod32_done:
    mov r0, #0
    mov r1, #0
    bx lr

intdiv_double:
    push {r2, lr}
    vcvt.s32.f64 s4, d0
    vcvt.s32.f64 s5, d1
    vmov r0, s4
    vmov r1, s5
    cmp r1, #0
    beq intdiv_by_zero
    bl signed_divmod32
    vmov s6, r0
    vcvt.f64.s32 d0, s6
    pop {r2, lr}
    bx lr
intdiv_by_zero:
    ldr r0, =const_zero_runtime
    vldr d0, [r0]
    pop {r2, lr}
    bx lr

mod_double:
    push {r2, lr}
    vcvt.s32.f64 s4, d0
    vcvt.s32.f64 s5, d1
    vmov r0, s4
    vmov r1, s5
    cmp r1, #0
    beq mod_by_zero
    bl signed_divmod32
    vmov s6, r1
    vcvt.f64.s32 d0, s6
    pop {r2, lr}
    bx lr
mod_by_zero:
    ldr r0, =const_zero_runtime
    vldr d0, [r0]
    pop {r2, lr}
    bx lr

.data
    .balign 8
const_zero_runtime:
    .double 0.0
    .balign 8
const_one_runtime:
    .double 1.0

    .balign 4
msg_line_1:
    .asciz "L3: 0x"
    .balign 4
msg_line_2:
    .asciz "L4: 0x"
    .balign 4
msg_line_3:
    .asciz "L5: 0x"
    .balign 4
msg_line_4:
    .asciz "L6: 0x"
    .balign 4
msg_line_5:
    .asciz "L7: 0x"
    .balign 4
msg_line_6:
    .asciz "L8: 0x"
    .balign 4
msg_line_7:
    .asciz "L9: 0x"
    .balign 4
msg_line_8:
    .asciz "L10: 0x"
    .balign 4
msg_line_9:
    .asciz "L11: 0x"
    .balign 4
msg_line_10:
    .asciz "L12: 0x"
    .balign 4
msg_line_11:
    .asciz "L13: 0x"
    .balign 4
msg_line_12:
    .asciz "L14: 0x"
    .balign 4
msg_line_13:
    .asciz "L15: 0x"
    .balign 4
msg_line_14:
    .asciz "L16: 0x"
    .balign 4
msg_line_15:
    .asciz "L17: 0x"

    .balign 8
result_line_1:
    .double 0.0
result_line_2:
    .double 0.0
result_line_3:
    .double 0.0
result_line_4:
    .double 0.0
result_line_5:
    .double 0.0
result_line_6:
    .double 0.0
result_line_7:
    .double 0.0
result_line_8:
    .double 0.0
result_line_9:
    .double 0.0
result_line_10:
    .double 0.0
result_line_11:
    .double 0.0
result_line_12:
    .double 0.0
result_line_13:
    .double 0.0
result_line_14:
    .double 0.0
result_line_15:
    .double 0.0

    .balign 8
mem_ATIVO:
    .double 0.0
mem_D:
    .double 0.0
mem_N:
    .double 0.0
mem_TAXA:
    .double 0.0

    .balign 8
tmp_slot_0:
    .double 0.0
tmp_slot_1:
    .double 0.0
tmp_slot_2:
    .double 0.0
tmp_slot_3:
    .double 0.0
tmp_slot_4:
    .double 0.0
tmp_slot_5:
    .double 0.0

    .balign 8
const_0:
    .double 12.0
    .balign 8
const_1:
    .double 4.0
    .balign 8
const_2:
    .double 3.25
    .balign 8
const_3:
    .double 1.0
    .balign 8
const_4:
    .double 2.0
    .balign 8
const_5:
    .double 3.0
    .balign 8
const_6:
    .double 27.0
    .balign 8
const_7:
    .double 5.0
    .balign 8
const_8:
    .double 0.0

