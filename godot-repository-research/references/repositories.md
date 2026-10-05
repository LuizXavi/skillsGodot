# Referências para jogos Godot

Consulta às fontes primárias em 2026-10-05. Pesquisa documental; estes candidatos não foram instalados nem testados no GameSurvive. Revalidar versões e licenças antes de adotar. Nenhum commit foi fixado porque ainda não há dependência adotada.

| Fonte | Uso | Compatibilidade e limites | Licença |
| --- | --- | --- | --- |
| [Demos oficiais](https://github.com/godotengine/godot-demo-projects) | Primeira referência para 2D, 3D, GUI, áudio e redes | Escolher branch estável correspondente ao motor; `master` acompanha desenvolvimento da próxima 4.x | [MIT](https://github.com/godotengine/godot-demo-projects/blob/master/LICENSE.md); conferir avisos de arquivos incluídos |
| [GUT](https://github.com/bitwes/Gut) | Testes GDScript, execução por CLI e relatórios JUnit | Matriz consultada associa 9.7.1 / `godot_4_7` ao Godot 4.7. Consultar a matriz para outras versões; não assumir que todo GUT 9.x serve para qualquer Godot 4.x | [MIT](https://github.com/bitwes/Gut/blob/main/addons/gut/LICENSE.md) |
| [GDScript Toolkit](https://github.com/Scony/godot-gdscript-toolkit) | `gdlint` e `gdformat --check` quando padronização for necessária | README indica linha 4.* para Godot 4 e 3.* para Godot 3. Fixar versão; análise estática não substitui o motor | [MIT](https://github.com/Scony/godot-gdscript-toolkit/blob/master/LICENSE) |
| [GDQuest — novos recursos do Godot 4](https://github.com/gdquest-demos/godot-4-new-features) | Estudar navegação, Resources, shaders, UI e redes | Exemplos documentados de 4.0 e 4.1; não comprova execução em todas as versões posteriores | [Código MIT; imagens/modelos CC-BY-NC-SA 4.0](https://github.com/gdquest-demos/godot-4-new-features/blob/main/LICENSE) |
| [GDQuest — controlador 3D em terceira pessoa](https://github.com/gdquest-demos/godot-4-3d-third-person-controller) | Referência opcional para câmera e movimentação 3D | `project.godot` consultado declara 4.7 e Forward Plus. Verificar renderer e revisão antes de adaptar | Repositório declara código MIT; imagens/modelos CC-BY-NC-SA 4.0 |

## Decisão para este projeto

Consultar demos oficiais conforme a necessidade. Manter o runner SceneTree existente; GUT e gdtoolkit são opções futuras, não requisitos. Referências de controle 3D não atendem automaticamente às necessidades da interface atual. Não reutilizar arte com restrição não comercial em um produto comercial sem licença apropriada.

## Documentação oficial

- [CLI do Godot](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html): selecionar a versão correspondente ao motor. `--check-only` acompanha `--script` e não valida o projeto completo.
- [Documentação Godot](https://docs.godotengine.org/): ponto de entrada para selecionar versão e consultar APIs.

## Registro ao adotar material

Registrar junto da integração: problema resolvido, URL, tag/commit, versão e renderer do motor, licença de código/arte/dependências, atribuições preservadas, arquivos incorporados e testes realizados. Distinguir pesquisa documental de compatibilidade executada. Não preencher com versões ou resultados presumidos.
