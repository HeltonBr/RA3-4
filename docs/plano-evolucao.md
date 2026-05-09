# Plano sequencial de evolucao

## Meta

Chegar a uma versao otima em 8 atualizacoes pequenas, rastreaveis e validaveis.

## Atualizacao 1 - Base do repositorio e conformidade

Status: concluida

- Inicializar o projeto local.
- Registrar a analise integral do enunciado.
- Fixar arquitetura, convencoes e sintaxe canonica.
- Criar o primeiro commit de baseline.

## Atualizacao 2 - Leitor de tokens e compatibilidade Fase 1

Status: concluida

- Implementar `lerTokens(arquivo)`.
- Ler arquivos no formato serializado da Fase 1.
- Normalizar tokens por linha com tipo, lexema, linha, coluna e metadados numericos.
- Criar testes unitarios para entrada valida e invalida.

## Atualizacao 3 - Gramatica formal LL(1)

Status: concluida

- Definir a EBNF completa.
- Implementar `construirGramatica()`.
- Calcular FIRST e FOLLOW.
- Construir a tabela LL(1).
- Detectar conflitos automaticamente.

## Atualizacao 4 - Parser descendente recursivo

Status: concluida

- Implementar `parsear(tokens, tabela_ll1)`.
- Criar o fluxo com buffer, pilha e funcoes por nao-terminal.
- Produzir derivacao e erros sintaticos descritivos.

## Atualizacao 5 - AST e persistencia

Status: concluida

- Implementar `gerarArvore(derivacao)`.
- Serializar arvore em JSON e texto.
- Persistir artefatos da ultima execucao em `generated/`.

## Atualizacao 6 - Controle de fluxo

Status: concluida

- Consolidar `SEQ`, `IF`, `IFELSE` e `WHILE`.
- Garantir integracao da AST com as estruturas de controle.
- Adicionar casos profundos e cenarios de erro.

## Atualizacao 7 - Geracao de Assembly

Status: concluida

- Implementar `gerarAssembly(arvore)`.
- Gerar rotulos, desvios condicionais e laco em ARMv7.
- Validar coerencia da saida com a AST.

## Atualizacao 8 - Fechamento para entrega

Status: concluida

- Produzir README final.
- Gerar markdown tecnico com gramatica, FIRST/FOLLOW, tabela e arvore.
- Criar e revisar os 3 arquivos de teste completos.
- Organizar a ultima execucao e o historico de commits.
- Consolidar auditoria automatizada e checklist final de entrega.

## Estrategia de commits

Sugestao de mensagens objetivas:

1. `chore: bootstrap do projeto e analise de requisitos`
2. `feat: implementa leitura de tokens da fase 1`
3. `feat: adiciona gramatica ll1 e tabela de analise`
4. `feat: implementa parser descendente recursivo`
5. `feat: gera arvore sintatica e persistencia`
6. `feat: adiciona estruturas de controle`
7. `feat: gera assembly armv7 a partir da ast`
8. `docs: fecha documentacao e artefatos finais`
