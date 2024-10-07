# QUIZ-GAME
JOGO DE PERGUNTAS E RESPOSTAS COM OS ASSUNTOS DO CURSO DE ENGENHARIA DE SOFTWARE
Resumo das Funções
AnimatedGIF: Classe que exibe um GIF animado em um tk.Label. Carrega as frames do GIF e as anima conforme o tempo passa.

JogoDePerguntas: Classe principal que gerencia o jogo.

__init__: Inicializa a janela do jogo, carrega sons, configura frames e define variáveis do jogo.
setup_window: Configura as propriedades da janela principal.
setup_frames: Cria a interface gráfica do jogo, incluindo a tela de perguntas e botões.
setup_game_variables: Inicializa variáveis como pontuação, fase atual e tempo do jogo.
load_sounds: Carrega os arquivos de som para o jogo.
load_questions: Define as perguntas e respostas de cada fase do jogo.
iniciar_jogo: Inicia o jogo com o nome do jogador, tocando a música de fundo.
iniciar_fase: Inicia a fase atual, atualizando a pergunta.
atualizar_pergunta: Exibe a pergunta e suas opções de resposta.
start_timer: Inicia um temporizador de 30 segundos para cada pergunta.
countdown: Atualiza o tempo restante na tela.
verificar_resposta: Verifica se a resposta do jogador está correta e avança no jogo.
inserir_no_ranking: Adiciona a pontuação do jogador ao ranking, se houver.
mostrar_ranking: Exibe a classificação dos jogadores a partir de um arquivo JSON.
mostrar_regras: Mostra as regras do jogo em uma janela de mensagem.
mostrar_ajuda: Oferece dicas para a pergunta atual.
show_game_over: Exibe a tela de Game Over quando o jogador termina o jogo ou desiste.
finalizar_jogo: Finaliza o jogo e mostra a pontuação do jogador, junto com a tela de Game Over.
resetar_jogo: Reinicia o jogo, permitindo que o jogador comece novamente.
main: A parte principal do código que inicializa a aplicação e a janela de entrada do nome do jogador.

Funcionamento do Jogo
O jogador inicia o jogo inserindo seu nome.
Ao clicar em "Iniciar Jogo", a tela de perguntas aparece, com a primeira pergunta e opções de resposta.
O jogador tem 30 segundos para responder cada pergunta. Se o tempo acabar, a resposta é considerada incorreta.
Ao responder corretamente, o jogador avança para a próxima pergunta. Ao completar todas as perguntas de uma fase, a pontuação é salva e o jogador avança para a próxima fase.
Se o jogador desiste ou termina o jogo, a tela de Game Over aparece, permitindo que ele escolha entre sair, reiniciar o jogo ou registrar sua pontuação no ranking.
O ranking é exibido em uma nova janela, mostrando a pontuação dos jogadores anteriores.
