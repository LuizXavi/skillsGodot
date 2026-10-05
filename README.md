# Skills Godot

Orientações reutilizáveis para desenvolver jogos Godot com Codex e pesquisar exemplos e addons antes de integrá-los.

## Skills

- [godot-game-development](godot-game-development/SKILL.md): implementação e correção de gameplay, cenas, Resources, UI, saves e validação.
- [godot-repository-research](godot-repository-research/SKILL.md): pesquisa de repositórios, compatibilidade, licenças e custo de integração. Inclui [catálogo de fontes](godot-repository-research/references/repositories.md).
- [godot-2d-ui](godot-2d-ui/SKILL.md): HUDs, menus, temas, escala e navegação por dispositivos.
- [godot-save-system](godot-save-system/SKILL.md): saves versionados, backup, migração e recuperação.
- [godot-offline-progress](godot-offline-progress/SKILL.md): jogar sem internet e simular ausência sem contar ganhos duas vezes.

## Uso em projetos futuros

Copie as cinco pastas `godot-*` para `~/.agents/skills`, local de descoberta pessoal descrito na [documentação oficial do Codex](https://learn.chatgpt.com/docs/build-skills). Evite instalar a mesma skill em múltiplos locais de descoberta. Se não aparecerem após a instalação, reinicie o Codex. Você também pode mantê-las no próprio projeto e adicionar ao `AGENTS.md` instruções para ler o `SKILL.md` relevante, preservando as regras existentes.

A seleção automática fica habilitada por padrão: o agente considera a skill quando a tarefa corresponde à descrição e lê apenas o conteúdo relevante. Instalar instruções não altera os pesos do modelo nem garante melhora sem validação no jogo.

Exemplos de pedidos:

- Use $godot-game-development para corrigir o salvamento deste jogo e validar que o progresso anterior continua carregando.
- Use $godot-repository-research para comparar soluções de inventário compatíveis com a versão deste projeto.
- Use $godot-2d-ui para corrigir o inventário em janela pequena e navegação por gamepad.
- Use $godot-save-system para recuperar saves antigos sem sobrescrever arquivos corrompidos.
- Use $godot-offline-progress para calcular a produção durante ausência com insumos limitados.

As skills não instalam addons, alteram o motor nem iniciam pesquisas recorrentes. A seleção de dependências depende do problema e da versão do projeto. A pesquisa inicial foi realizada em 2026-10-05; revalide as referências antes de adotar material.

## Manutenção

Guarde aprendizados confirmados e fontes primárias. Contexto específico de um jogo deve ficar no repositório desse jogo. Registre tags/commits e atribuições ao incorporar material externo; as licenças dos repositórios pesquisados não são automaticamente a licença destas skills.
