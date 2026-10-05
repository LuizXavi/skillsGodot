---
name: godot-offline-progress
description: Implementar jogos Godot que funcionam sem internet e calcular progresso durante ausência, com limites de tempo, produção consistente e prevenção de recompensas duplicadas.
---

# Modo offline e progresso durante ausência

Identifique qual comportamento o pedido exige: jogar sem conexão, simular a ausência ou ambos. Use o contexto do produto antes de perguntar. Não acrescente progressão durante ausência a um jogo que apenas precisa abrir sem internet. Consulte [fontes e cenários](references/offline-cases.md) para tempo e ciclo de vida.

## Jogar sem conexão

Verifique boot, carregamento de assets, saves e sistemas essenciais com a rede indisponível. Não faça uma chamada remota obrigatória antes de abrir um jogo local. Serviços opcionais devem falhar com timeout limitado e feedback apropriado, preservando progresso local. Cloud sync, contas e conflito entre dispositivos exigem regras próprias; não adicione sincronização nem assuma que timestamp mais recente é suficiente.

## Progresso durante ausência

Defina quais sistemas avançam, limite de duração, caps de armazenamento, consumo de insumos, ordem de jobs, desbloqueios e se a concessão é automática ou por coleta. Extraia essas regras do jogo; não escolha um teto arbitrário silenciosamente.

- Durante execução, use delta/relógio monotônico apropriado. Entre sessões, persista timestamp UTC do sistema: ticks de processo não são relógio persistente. Injete o relógio nos testes.
- Calcule duração não negativa e limitada. Defina o tratamento de relógio para trás ou muito à frente e a atualização da âncora nesses casos. Clamp isolado sem política de reancoragem pode repetir recompensa ou bloquear futuras sessões.
- Relógio local é ajustável: limite impacto sem prometer proteção contra fraude. Só use tempo confiável de servidor quando o produto exigir e já houver arquitetura online compatível; mantenha explícito o fallback offline.
- Simule a partir do snapshot salvo com função testável. Multiplicação por taxa só é correta se a taxa e as condições permanecerem constantes. Para produção encadeada, trate eventos de conclusão, falta de insumos, capacidade e mudanças de taxa; limite complexidade sem executar um frame por segundo ausente.
- Desconte exatamente o intervalo já simulado online, inclusive em pausa/resume, para não contar o mesmo tempo duas vezes. Timers não devem ser tratados como se continuassem executando com o aplicativo fechado.

## Persistência da concessão

Resultado e marco de tempo/processamento pertencem ao mesmo snapshot. Em coleta manual, persista a recompensa pendente e seu identificador; ao coletar, grave inventário atualizado e remoção da pendência juntos. Em concessão automática, grave o estado atualizado antes de permitir consumo irreversível do ganho ou reportar a operação como persistida.

Se a gravação falhar, preserve um estado recuperável e impeça nova concessão do mesmo intervalo na sessão; não deixe ganhos transitórios serem gastos e depois recalculados. Após recuperação de backup antigo, reconheça o limite de durabilidade: garantia entre dispositivos ou após rollback deliberado exige autoridade adicional.

## Validação

Teste duração zero, negativa, limite/excesso, relógio alterado, carga repetida, coleta repetida, falha de escrita e interrupção antes/depois de persistir. Confira produção com insumos esgotados, armazenamento cheio e cadeia de jobs; compare a simulação offline com a online quando a equivalência fizer parte do design. Teste pausa/retorno e rede ausente separadamente. Use dados temporários.
