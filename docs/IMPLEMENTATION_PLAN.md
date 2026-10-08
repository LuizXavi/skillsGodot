# Plano da implementação — 2026-10-05

## Análise inicial
O repositório possuía cinco skills úteis na raiz: desenvolvimento, pesquisa, UI 2D, saves e offline. Não havia ferramentas, templates executáveis nem fixtures. As skills já estavam publicadas e instaladas no perfil do usuário; mover seus caminhos quebraria consumidores existentes.

## Plano
1. Preservar skills históricas e criar índice único, router e modelos compactos de contexto.
2. Delegar ferramentas Python e testes, templates Godot e smoke tests, e skills adicionais em áreas separadas.
3. Implementar o ambiente `/ai` no projeto consumidor GameSurvive, sem incorporar dados específicos do jogo nesta toolbox.
4. Executar testes Python, validação estrutural e smoke tests Godot quando o motor estiver disponível; registrar limitações.
5. Revisar conteúdo, registrar commits lógicos e publicar a toolbox no remoto existente.

## Decisões
- DEC-001: caminhos antigos continuam canônicos; novas skills ficam por domínio em `skills/`. Evita duplicação e quebra de instalações.
- DEC-002: ferramentas usam Python stdlib e análise estática limitada. Não executar código de um projeto apenas para criar contexto.
- DEC-003: outras engines não recebem pastas vazias; separar futuros adaptadores quando houver necessidade real.
- DEC-004: perfis de agentes são contratos portáveis; a ferramenta de orquestração do host cria subagentes sob demanda, sem daemon ou custo recorrente.
