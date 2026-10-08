# Evidências de validação

Validação final da infraestrutura em 2026-10-08. Python 3.11 e Godot 4.7.2 stable Windows.

| Check | Resultado | Evidência / limite |
| --- | --- | --- |
| `python -m unittest discover -s tests -v` | PASS | 17 testes: 16 executados com sucesso, 1 skip porque criação de symlink não estava disponível |
| `python tools/validation/validate.py .` | PASS | Frontmatter, links, nomes duplicados, templates e duplicação exata; 0 issues após integração dos relatórios |
| `examples/smoke/run.ps1 -Godot <executável>` | PASS | `TOOLKIT_SMOKE: OK`; projeto e saves temporários |
| Três CLIs no projeto GameSurvive | PASS | PROJECT_SNAPSHOT, AI_CONTEXT e DEPENDENCY_MAP gerados; 80 scripts, 14 cenas, 381 .tres, seis autoloads |
| Quatro testes de `ai/tests` no consumidor | PASS | Link inválido, escape de raiz, papel ausente e alteração de runtime detectados |

Testes Python usam fixtures temporárias e verificam contagem/ignorados, cargas literais e dinâmicas, foco por caminho, prioridade de entrada/autoload, proteção contra sobrescrita, configuração ausente, frontmatter e templates agrupados. O mapper não é um parser completo. O validador suporta o subconjunto YAML documentado e links Markdown inline; não valida âncoras.

Smoke Godot cobre inventário/filtros/ordenação/import atômico, crafting/consumo/overflow, reset de prestígio com permanentes, limite offline/repetição/relógio atrasado, save/migração/backup/corrupção/versão futura e limites numéricos JSON. O ramo de export release do debug menu não foi exercitado; UI gráfica e mobile não foram verificados.

## Regressão do jogo consumidor

Executável: `C:/Users/hultr/Documents/Godot_v4.7.2-stable_win64.exe/Godot_v4.7.2-stable_win64_console.exe`.

Cinco testes do runner principal passaram: ui_smoke, crafting_smoke, permanent_upgrades, campaign_reachability e progression_integration. generator_research separado passou. resource_audit falhou em `Generator elapsed cycles` porque a fixture não prepara o desbloqueio atual. dev_panel falhou na asserção de hired_workers na linha 28 e foi encerrado depois de permanecer aberto. Essas falhas foram registradas na memória do consumidor; a infraestrutura não alterou seu código para escondê-las.

Nenhuma destas evidências representa playtest completo, auditoria de segurança do addon ou balanceamento integral da campanha.
