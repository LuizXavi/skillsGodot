---
name: godot-save-system
description: Implementar e corrigir saves locais Godot, autosave, slots, migrações, backup e recuperação de corrupção sem perder progresso existente.
---

# Saves recuperáveis

Primeiro localize o mecanismo existente, `user://`, schema, slots, pontos de autosave e fixtures. Preserve o formato quando ele atende ao pedido. Leia [fontes](references/sources.md) para confirmar APIs de persistência e ciclo de vida na versão/plataforma usada.

## Dados e compatibilidade

- Salve dados explícitos e versionados com IDs estáveis. Não serialize a árvore de cenas, referências vivas de Node nem Object como substituto de um schema.
- Use JSON para dados interoperáveis ou ConfigFile quando se ajustar ao modelo existente. Valide formato, tipos, limites, IDs e números finitos antes de aplicar qualquer estado; parsing bem-sucedido não valida o jogo. JSON não preserva todos os tipos Godot automaticamente.
- Faça migrações sequenciais sobre uma cópia validada. Preserve o original até confirmar a gravação. Para versão futura desconhecida, não sobrescreva com defaults nem force downgrade silencioso.
- Use dados simples para saves externos; não carregue `.tres`, `.res` ou objetos arbitrários de origem não confiável por ResourceLoader/deserialização com objetos habilitados.

## Gravação e recuperação

Capture um snapshot consistente, incluindo jobs, inventário, progressão e marcos de recompensa que pertencem à mesma transação lógica. Serialize gravações concorrentes; um autosave antigo não deve sobrescrever um estado mais novo.

Grave primeiro em arquivo temporário no diretório do slot, confira retornos/erros, feche e valide a leitura antes de promover. Preserve ao menos uma geração conhecida como válida. Planeje a recuperação se houver interrupção entre gravar temporário, preservar backup e promover principal. Confira semântica de substituição na plataforma; renomear arquivos e `flush()` não são garantia universal contra perda de energia.

Ao carregar, valide candidatos antes de escolher; metadados de geração ajudam a ordenar apenas snapshots válidos. Não promova arquivos truncados nem substitua o último backup válido por um principal corrompido. Diferencie ausência de save, corrupção e falha de permissão/espaço. Informe falha real de gravação sem anunciar sucesso ou apagar progresso.

Autosave deve ter cadência e checkpoints proporcionais ao jogo. Não dependa apenas de fechar a janela: mobile pode suspender e terminar o processo. Trate pausa/suspensão dentro do orçamento da plataforma e mantenha trabalho pequeno nesse momento. Testes usam slots/diretórios temporários, nunca o save real do usuário.

## Verificação de comportamento

Escolha casos relevantes: round-trip com estado real; migração de fixture antiga; versão futura; truncação; schema/tipos/IDs inválidos; falha de escrita; interrupções entre fases; principal inválido com backup válido; autosaves sobrepostos; pausa/retorno e reinício. Confirme invariantes do estado recuperado e preservação dos originais, não apenas existência de arquivos.

Para recompensas durante ausência, combine com `godot-offline-progress` quando disponível. Resultado concedido e marco temporal devem ser persistidos juntos; não adicione uma segunda gravação independente para a UI de coleta.
