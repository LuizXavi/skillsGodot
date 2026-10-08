# Ferramentas locais

Requerem apenas Python 3.11+ da biblioteca padrão. Execute a partir da raiz deste repositório:

```text
python tools/project_analyzer/analyze.py CAMINHO_DO_PROJETO --output PROJECT_SNAPSHOT.md
python tools/context_generator/generate.py CAMINHO_DO_PROJETO --focus inventario --output AI_CONTEXT.md
python tools/dependency_mapper/map.py CAMINHO_DO_PROJETO --output DEPENDENCY_MAP.md
python tools/validation/validate.py RAIZ_DAS_SKILLS
python -m unittest discover -s tests -v
```

Os três primeiros comandos usam, por padrão, os nomes de relatório indicados dentro do projeto analisado. Um `--output` existente só é substituído se contiver o marcador de geração destas ferramentas; arquivos Markdown humanos e arquivos fonte são protegidos. O validador imprime problemas e retorna código 1 quando encontra algum.

O inventário lê `project.godot` e scripts `.gd`, e conta cenas `.tscn`, recursos `.tres` e binários `.res`. O contexto seleciona até 28 caminhos; `--focus` prioriza termos encontrados nos caminhos, sem pesquisar o conteúdo dos arquivos. O mapa procura chamadas literais `preload`/`load`, `extends`, `class_name`, `ext_resource`, declarações/uso de sinais e referências heurísticas a autoloads. Chamadas dinâmicas aparecem com caminho e linha, sem fingir que o destino foi resolvido. Saídas são limitadas e nunca incluem corpos inteiros de scripts nem valores gerais de configuração.

O validador aceita um subconjunto YAML: frontmatter entre duas linhas `---`, chaves escalares `name:` e `description:` sem indentação, valores simples ou entre aspas, descrição em bloco `|`/`>` com linhas indentadas e um mapping `metadata:` com valores escalares indentados. O nome deve usar letras minúsculas, números e hífens. Recursos YAML mais complexos não são interpretados. Links Markdown relativos simples são checados por existência; âncoras não são validadas. Pastas de template em `templates/<nome>` e folhas em `templates/godot/<nome>` precisam de `README.md` e ao menos outro arquivo; `templates/godot` é uma pasta agrupadora. Duplicação significa conteúdo byte a byte idêntico.

As varreduras não entram em `.git`, `.godot`, backups, repositórios aninhados, pastas com `.gdignore`, links simbólicos ou junctions. Ignoram binários conhecidos; `.res` é contado sem leitura. Arquivos de texto acima de 2 MB são ignorados. A análise é estática e pode perder referências construídas em runtime ou marcar menções em comentários como dependências; confirme o comportamento no Godot quando necessário.
