---
name: godot-game-development
description: Implementar, corrigir e validar jogos Godot com GDScript, cenas, recursos, interfaces e persistência, respeitando a versão e a arquitetura do projeto.
---

# Desenvolvimento de jogos Godot

## Conhecer o projeto

Leia `project.godot`, as instruções locais e os scripts/cenas envolvidos. Identifique cena inicial, autoloads, ações de entrada, renderer e mecanismo de testes existentes. Compare a versão declarada em `config/features` com `Godot --version`; a declaração não prova qual executável está instalado. Consulte a documentação oficial correspondente à versão antes de usar APIs incertas. Não migre a versão do motor apenas para aproveitar um exemplo.

Se existir `docs/GODOT_PROJECT_CONTEXT.md`, use-o para localizar decisões específicas do jogo. Em outro projeto, descubra o contexto novamente; não transporte nomes de autoloads nem regras econômicas do GameSurvive.

## Implementar

- Preserve as convenções existentes. Separe estado de gameplay da apresentação quando a mudança exigir essa separação; não crie autoloads para dados que pertencem a uma cena.
- Prefira Resources para definições editáveis e cenas/componentes para composição quando isso se encaixar na arquitetura. Ao alterar um Resource compartilhado em runtime, determine se a mudança deve afetar todas as instâncias ou uma cópia local.
- Ao mover scripts, preserve os arquivos `.gd.uid` existentes e atualize referências `res://`, preloads, cenas, recursos e carregamentos dinâmicos. Não regenere UIDs em massa nem edite o cache `.godot` para resolver referências.
- Em UI baseada em Control, confira Containers, anchors, tamanho mínimo, foco e `mouse_filter`. Preserve proporção de imagens e valide os tamanhos de janela relevantes ao produto.
- Em persistência, preserve saves existentes e planeje compatibilidade/migração antes de mudar o esquema. Testes devem usar dados temporários ou desativar o salvamento normal.
- Em economia e progressão, verifique consumo único, saldo insuficiente, limites de desbloqueio e comportamento após carregar/resetar. Se houver produção offline, verifique limites e relógio sem pressupor avanço monotônico do horário do sistema.

## Validar conforme a alteração

Use o executável confirmado e caminhos explícitos. Exemplo em PowerShell, com variáveis apontando para o projeto correto:

```powershell
& $Godot --headless --path $Project --editor --import
& $Godot --headless --path $Project --script 'res://tests/example_test.gd'
```

O segundo comando é ilustrativo: substitua pelo teste existente apropriado. Verifique o código de saída e erros de script/importação; se o runner exige marcador de sucesso, verifique-o também. A importação não comprova gameplay correto.

Execute os testes relevantes ao comportamento alterado. Para mudanças visuais ou de interação, abra a cena com renderer gráfico e exercite o fluxo; testes headless não comprovam aparência, legibilidade nem input real. Não apresente validação gráfica como concluída se não houver evidência.

Resuma o comportamento entregue, verificações executadas e limitações concretas. Atualize referências reutilizáveis apenas com decisões ou falhas confirmadas, sem transformar peculiaridades de um jogo em regras globais.
