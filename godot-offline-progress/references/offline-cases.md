# Fontes e casos offline

Pesquisa em 2026-10-05; selecione a documentação da versão real do projeto.

- [Time, Godot 4.3](https://docs.godotengine.org/en/4.3/classes/class_time.html): relógio do sistema pode ser ajustado; ticks são apropriados para duração durante execução.
- [Node](https://docs.godotengine.org/en/stable/classes/class_node.html): notificações de pausa/retorno e modos de processamento.
- [Quit requests, Godot 4.4](https://docs.godotengine.org/en/4.4/tutorials/inputs/handling_quit_requests.html): limitações de suspensão/encerramento em mobile.
- [FileAccess](https://docs.godotengine.org/en/stable/classes/class_fileaccess.html): persistência local para snapshot e marcos de progresso.

As regras de recompensa e transação abaixo são recomendações desta skill, não um subsistema offline pronto do Godot.

| Cenário | Invariante a testar |
| --- | --- |
| Reiniciar duas vezes sem tempo transcorrido | Nenhum ganho adicional pelo mesmo intervalo |
| Interromper entre simulação e persistência | Recuperar snapshot coerente; não combinar inventário novo com marco antigo |
| Falhar ao salvar uma coleta | Não duplicar, descartar silenciosamente ou liberar gasto de uma concessão não consolidada |
| Relógio recua ou avança muito | Aplicar política explícita e recuperar uma âncora utilizável |
| Insumo acaba antes do fim da ausência | Produção para no instante/regra correta |
| Voltar de suspensão | Intervalo não se sobrepõe à simulação já executada |
| Iniciar sem internet | Fluxo local essencial funciona; serviços opcionais não bloqueiam indefinidamente |

Não há addon obrigatório nem código de terceiros incorporado.
