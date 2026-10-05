---
name: godot-2d-ui
description: Criar e corrigir HUDs, menus, inventários e interfaces de jogos 2D Godot, incluindo layout responsivo, pixel art e navegação por mouse, teclado e gamepad.
---

# UI de jogos 2D

Inspecione versão do motor, renderer, resolução-base, stretch, tema, cenas de UI e dispositivos-alvo antes de editar. Preserve a direção visual existente; identifique a ação principal, hierarquia de informação e estados normal, hover, foco, pressionado, desativado e bloqueado. Consulte [fontes](references/sources.md) quando precisar confirmar APIs ou configuração de escala.

## Composição e aparência

- Use Containers para layout fluido, anchors/offsets para posicionamento relativo simples. Não dispute posição/tamanho de filhos gerenciados por Container; ajuste size flags, mínimos e espaçamentos do layout.
- Centralize tipografia, cores, margens e StyleBoxes compartilhados em Theme. Prefira variações de tipo e componentes reutilizáveis a overrides repetidos. Diferencie recursos compartilhados de cópias por instância antes de mudar um tema em runtime.
- Separe HUD fixo da câmera do mundo quando necessário (por exemplo, CanvasLayer). Mostre alterações do estado do jogo por sinais ou atualização direcionada; a UI não deve manter outra cópia autoritativa de inventário ou economia.
- Planeje o texto mais longo e os maiores valores esperados; use quebra, tamanho mínimo, scroll ou abreviação explícita. Não resolva tudo encolhendo a fonte. Estados importantes devem ter texto/ícone além de cor.
- Para pixel art, escolha conscientemente resolução-base, filtro e escala inteira. `viewport` e `canvas_items` têm resultados diferentes; não troque o stretch de um projeto inteiro para corrigir um único painel. Arte do mundo e texto do HUD podem precisar de tratamentos distintos.

## Interação

- Use `_gui_input()`/sinais dos Controls conforme o componente. Consuma eventos apropriados com `accept_event()`; gameplay em `_unhandled_input()` pode respeitar eventos consumidos pela UI. `Input.is_action_pressed()` é polling e não fica bloqueado automaticamente por `accept_event()`: controle explicitamente o gameplay quando houver modal.
- Decoração sobre botões geralmente precisa de `MOUSE_FILTER_IGNORE`. Verifique filtros dos ancestrais e overlays antes de culpar o botão. Um overlay bloqueado deve impedir apenas as interações previstas.
- Dê foco inicial a um controle válido e defina vizinhos em layouts complexos. Ao fechar um modal, restaure o foco de origem; evite direcioná-lo a controles ocultos ou desativados. Mantenha ações de navegação `ui_*` separadas das ações de gameplay.
- Durante pausa, confira `process_mode` da UI e do gameplay. Menus devem responder conforme o comportamento solicitado, inclusive ao alternar entre mouse e gamepad.

## Validação

Teste graficamente a resolução-base, a menor janela suportada e uma proporção diferente. Exercite textos longos, lista vazia/cheia, tooltip, modal, bloqueio/desbloqueio, teclado e controle quando disponíveis. Confira clipping, proporção de imagens, contraste e indicador de foco nas capturas.

Meça antes de otimizar. Para listas grandes, investigue reconstrução completa por frame, conexões duplicadas e atualizações desnecessárias; adote reutilização/virtualização somente quando o perfil justificar. Testes headless não comprovam layout nem input gráfico. Registre o que foi exercitado e o que depende de dispositivo indisponível.
