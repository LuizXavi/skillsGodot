# Fontes de persistência

Consultadas em 2026-10-05. Selecione a versão do projeto no site; páginas de versões anteriores abaixo documentam conceitos, não comprovam compatibilidade integral com outra versão.

- [FileAccess](https://docs.godotengine.org/en/stable/classes/class_fileaccess.html): operações e erros de arquivo; consulte os avisos de deserialização de objetos em `get_var`.
- [Saving games, Godot 4.4](https://docs.godotengine.org/en/4.4/tutorials/io/saving_games.html): exemplo didático de save; não é protocolo completo de recuperação.
- [ConfigFile](https://docs.godotengine.org/en/stable/classes/class_configfile.html) e [JSON](https://docs.godotengine.org/en/stable/classes/class_json.html): formatos e resultados de parsing.
- [ResourceLoader](https://docs.godotengine.org/en/stable/classes/class_resourceloader.html): carregamento de recursos do motor, distinto de um schema de save em dados simples.
- [Quit requests, Godot 4.4](https://docs.godotengine.org/en/4.4/tutorials/inputs/handling_quit_requests.html) e [Node](https://docs.godotengine.org/en/stable/classes/class_node.html): encerramento e notificações de ciclo de vida.

Snapshot consistente, backup por geração, migração e testes de interrupção são recomendações de engenharia desta skill; não são promessas de atomicidade fornecidas por FileAccess. Nenhuma dependência externa é exigida.
