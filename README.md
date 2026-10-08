# GameDev AI Toolkit

Memória técnica externa e ferramentas reutilizáveis para agentes desenvolverem jogos com menos contexto e melhor evidência. Prioridade atual: Godot 4 / GDScript, idle, RPG, UI, mobile, saves e debugging. Não exige API, serviço externo ou dependência Python de terceiros.

## Começar

1. Leia [AGENTS.md](AGENTS.md).
2. No projeto-alvo, leia PROJECT_CONTEXT, GAME_STATE e CURRENT_TASK quando existirem. [Modelos compactos](docs/PROJECT_CONTEXT_TEMPLATE.md) ajudam quando faltarem.
3. Se o estado estiver desatualizado, gere um snapshot; selecione uma skill pelo [índice](skills/INDEX.md).
4. Procure símbolos e dependências diretas, reutilize componentes, implemente e valide.
5. Atualize só a memória afetada; não carregue o projeto inteiro por padrão.

## Estrutura

| Caminho | Uso |
| --- | --- |
| AGENTS.md | Router curto, contexto e regras de preservação |
| godot-*/ | Cinco skills históricas, caminhos preservados |
| skills/godot/ | Arquitetura, GDScript, mobile, debugging e performance |
| skills/game-design/ | Inventário, economia idle, crafting, prestígio e progressão |
| skills/workflows/ | Bug fixing, feature, refactor, review e auditorias |
| templates/godot/ | Seis módulos pequenos, cada um com README |
| docs/ | Modelos de memória, decisões, plano e evidências |
| tools/ | Análise, contexto, dependências e validação |
| examples/smoke/ | Projeto temporário que testa templates reais |
| tests/ | Regressões Python com fixtures temporárias |

Outras engines receberão adaptadores e skills quando houver implementação concreta; não há diretórios vazios prometendo suporte.

## Ferramentas

Python 3.11+. A partir desta raiz, substitua o caminho pelo projeto Godot:

```powershell
python tools/project_analyzer/analyze.py ../ --output PROJECT_SNAPSHOT.md
python tools/context_generator/generate.py ../ --focus 'WorkerRoster Progression' --output AI_CONTEXT.md
python tools/dependency_mapper/map.py ../ --output DEPENDENCY_MAP.md
python tools/validation/validate.py .
python -m unittest discover -s tests -v
```

Saídas são Markdown compacto, não cópias de código. `--output` tem de apontar para um diretório existente; um arquivo humano existente não é sobrescrito. Sem `--output`, relatórios vão para o projeto-alvo. `--focus` procura nomes de caminhos, não faz busca semântica. O mapper é heurístico e lista cargas dinâmicas não resolvidas. Consulte [limites e sintaxe](tools/README.md).

## Skills e agentes

Há 21 skills: as cinco originais e 16 especializadas. Consulte [nome, propósito e localização](skills/INDEX.md), depois leia só a skill relevante. Isso serve a Codex, ChatGPT, Claude Code, Copilot ou outro agente com acesso a arquivos; o host precisa ter ferramenta de delegação para executar subagentes em paralelo.

Exemplos: “use godot-2d-ui para corrigir o inventário em janela pequena”; “use godot-save-system para revisar migração”; “use game-idle-economy para calcular payback”. O índice é a fonte de descoberta portável. Preserve a árvore ao copiar o pacote, pois há links entre skills e templates.

As cinco pastas históricas podem continuar instaladas em `~/.agents/skills`. As novas skills agrupadas são carregadas pelo índice e pelo AGENTS do projeto; não afirmar que apenas publicar no Git as instala globalmente. Para instalação pessoal de uma skill especializada, preserve suas referências ou use um instalador que as resolva. Evite nomes duplicados no catálogo.

## Templates

- [Inventário](templates/godot/inventory_manager/README.md): IDs, categorias, filtros e ordenação.
- [Save](templates/godot/save_manager/README.md): schema, migração, backup e corrupção.
- [Crafting](templates/godot/crafting_system/README.md): receitas e planejamento de transações.
- [Prestígio](templates/godot/prestige_system/README.md): reset da run preservando permanentes.
- [Offline](templates/godot/offline_progress/README.md): limite temporal e resumo de ganhos.
- [Debug](templates/godot/debug_menu/README.md): ações por callbacks com bloqueio de release.

Copie apenas o módulo necessário, leia seu contrato e adapte ao estado já existente. Não instale outro manager onde o jogo já possui a responsabilidade. O save JSON rejeita inteiros fora de ±(2^53−1); valores maiores precisam de strings decimais ou outro schema explícito. Nenhum template é uma migração automática do GameSurvive.

```powershell
./examples/smoke/run.ps1 -Godot 'C:/caminho/Godot_console.exe'
```

O smoke usa projeto e save temporários, exige exit code e marcador de sucesso e limpa somente seu diretório. Não comprova UI gráfica, Android nem export release. Ver [resultados](docs/TEST_RESULTS.md).

## Memória e manutenção

Modelos: [Game State](docs/GAME_STATE_TEMPLATE.md), [Architecture](docs/ARCHITECTURE_TEMPLATE.md), [Current Task](docs/CURRENT_TASK_TEMPLATE.md), [Bug](docs/BUG_REPORT_TEMPLATE.md), [System Map](docs/SYSTEM_MAP_TEMPLATE.md) e [Decisions](docs/DECISIONS_TEMPLATE.md). Pequena tarefa usa router + tarefa + uma skill; tarefa transversal acrescenta mapa e arquitetura.

Para contribuir: busque conteúdo semelhante, faça mudança delimitada, acrescente teste comportamental quando necessário, execute validação e teste do domínio, registre compatibilidade/limites e faça commit lógico. Não copie manuais inteiros, não adicione secrets e preserve licenças de materiais externos. Histórico e decisões iniciais: [plano](docs/IMPLEMENTATION_PLAN.md).
