# Skills Godot

Orientações reutilizáveis para desenvolver jogos Godot com Codex e pesquisar exemplos e addons antes de integrá-los.

## Skills

- [godot-game-development](godot-game-development/SKILL.md): implementação e correção de gameplay, cenas, Resources, UI, saves e validação.
- [godot-repository-research](godot-repository-research/SKILL.md): pesquisa de repositórios, compatibilidade, licenças e custo de integração. Inclui [catálogo de fontes](godot-repository-research/references/repositories.md).

## Uso em projetos futuros

Copie as duas pastas para `$CODEX_HOME/skills`, ou `~/.codex/skills` se essa variável não estiver definida. Em uma nova sessão, confira se as skills aparecem disponíveis. Você também pode mantê-las no próprio projeto e adicionar ao `AGENTS.md` instruções para ler o `SKILL.md` relevante, preservando as regras existentes.

Exemplos de pedidos:

- Use $godot-game-development para corrigir o salvamento deste jogo e validar que o progresso anterior continua carregando.
- Use $godot-repository-research para comparar soluções de inventário compatíveis com a versão deste projeto.

As skills não instalam addons, alteram o motor nem iniciam pesquisas recorrentes. A seleção de dependências depende do problema e da versão do projeto. A pesquisa inicial foi realizada em 2026-10-05; revalide as referências antes de adotar material.

## Manutenção

Guarde aprendizados confirmados e fontes primárias. Contexto específico de um jogo deve ficar no repositório desse jogo. Registre tags/commits e atribuições ao incorporar material externo; as licenças dos repositórios pesquisados não são automaticamente a licença destas skills.
