import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import pygame
import os

class AnimatedGIF(tk.Label):
    def __init__(self, master, gif_path):
        super().__init__(master)
        self.gif_path = gif_path
        self.frames = self.load_gif()
        self.frame_index = 0
        self.after(100, self.animate)

    def load_gif(self):
        img = Image.open(self.gif_path)
        frames = []
        for i in range(img.n_frames):
            img.seek(i)
            frames.append(ImageTk.PhotoImage(img.copy()))
        return frames

    def animate(self):
        self.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(100, self.animate)

class JogoDePerguntas:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.setup_game_variables()
        pygame.mixer.init()
        self.load_sounds()
        self.setup_initial_screen()

    def setup_window(self):
        self.master.title("Jogo de Perguntas e Respostas")
        self.master.geometry("1000x800")
        self.master.configure(bg="#f0f0f0")
        self.master.resizable(False, False)

    def setup_initial_screen(self):
        # Tela inicial onde o jogador insere o nome
        self.entry_frame = tk.Frame(self.master, bg="white")
        self.entry_frame.place(relwidth=1, relheight=1)

        title_label = tk.Label(self.entry_frame, text="Bem-vindo ao Jogo de Perguntas!", font=("Arial", 20, "bold"), bg="white")
        title_label.pack(pady=30)

        name_label = tk.Label(self.entry_frame, text="Digite seu nome:", font=("Arial", 14), bg="white")
        name_label.pack(pady=10)

        self.name_entry = tk.Entry(self.entry_frame, font=("Arial", 14))
        self.name_entry.pack(pady=10)

        start_button = tk.Button(self.entry_frame, text="Iniciar Jogo", command=self.iniciar_jogo, font=("Arial", 14), bg="#4CAF50", fg="white")
        start_button.pack(pady=20)

    def setup_game_variables(self):
        self.pontuacao = 0
        self.fase_atual = 0
        self.nome_jogador = ""
        self.fases = []
        self.timer = None
        self.time_left = 30
        self.respostas_corretas_consecutivas = 0
        self.ajudas_usadas = 0
        self.pergunta_index = 0

    def load_sounds(self):
        # Som de fundo do jogo
        pygame.mixer.music.load(r"C:\Users\lb16243\Downloads\mario-type-beat-131248.mp3")
        self.som_fim_jogo = r"C:\Users\lb16243\Downloads\game over.mp3"
        self.som_ranking = r"C:\Users\lb16243\Downloads\mario rankig.mp3"

    def load_questions(self):
        self.fases = [
            {"titulo": "Fase 1: Conceitos Básicos de TI", "perguntas": self.perguntas_fase1()},
            {"titulo": "Fase 2: Redes e Internet", "perguntas": self.perguntas_fase2()},
            {"titulo": "Fase 3: Segurança da Informação", "perguntas": self.perguntas_fase3()},
            {"titulo": "Fase 4: Algoritmos e Programação", "perguntas": self.perguntas_fase4()},
            {"titulo": "Fase 5: Banco de Dados e Armazenamento", "perguntas": self.perguntas_fase5()},
        ]

    def perguntas_fase1(self):
        return [
            {"pergunta": "Qual é a unidade básica de armazenamento?", "opcoes": ["A) Bit", "B) Byte", "C) Kilobyte", "D) Megabyte"], "resposta": "B"},
            {"pergunta": "Qual sistema operacional é da Microsoft?", "opcoes": ["A) Linux", "B) macOS", "C) Windows", "D) Android"], "resposta": "C"},
            {"pergunta": "O que é um software?", "opcoes": ["A) Parte física", "B) Conjunto de instruções", "C) Sistema de armazenamento", "D) Tipo de hardware"], "resposta": "B"},
            {"pergunta": "O que é um sistema operacional?", "opcoes": ["A) Tipo de software", "B) Hardware", "C) Conjunto de instruções", "D) Sistema de rede"], "resposta": "A"},
            {"pergunta": "O que é o BIOS?", "opcoes": ["A) Sistema de armazenamento", "B) Sistema de entrada e saída", "C) Software do computador", "D) Sistema de comunicação"], "resposta": "C"},
            {"pergunta": "Qual é a principal função da CPU?", "opcoes": ["A) Armazenar dados", "B) Processar informações", "C) Exibir conteúdo", "D) Controlar a energia"], "resposta": "B"},
            {"pergunta": "O que significa a sigla RAM?", "opcoes": ["A) Read Access Memory", "B) Random Access Memory", "C) Remote Access Memory", "D) Real-time Access Memory"], "resposta": "B"},
            {"pergunta": "Qual é a função de um sistema de arquivos?", "opcoes": ["A) Processar dados", "B) Armazenar e organizar dados", "C) Exibir dados", "D) Enviar dados"], "resposta": "B"},
            {"pergunta": "Qual é a função do processador gráfico (GPU)?", "opcoes": ["A) Processar som", "B) Processar imagens e vídeos", "C) Armazenar arquivos", "D) Controlar rede"], "resposta": "B"},
            {"pergunta": "O que é a memória cache?", "opcoes": ["A) Memória de longo prazo", "B) Memória volátil de alta velocidade", "C) Memória de backup", "D) Memória de armazenamento"], "resposta": "B"},
        ]

    def perguntas_fase2(self):
        return [
            {"pergunta": "O que é um servidor?", "opcoes": ["A) Software", "B) Computador que fornece serviços", "C) Dispositivo de entrada", "D) Sistema operacional"], "resposta": "B"},
            {"pergunta": "Qual protocolo para enviar e-mails?", "opcoes": ["A) FTP", "B) SMTP", "C) HTTP", "D) POP3"], "resposta": "B"},
            {"pergunta": "Qual a principal função do protocolo TCP?", "opcoes": ["A) Garantir a entrega de pacotes", "B) Estabelecer conexão", "C) Controlar tráfego de rede", "D) Encaminhar dados para servidores"], "resposta": "A"},
            {"pergunta": "Qual protocolo é utilizado para navegação na web?", "opcoes": ["A) FTP", "B) HTTP", "C) DNS", "D) SMTP"], "resposta": "B"},
            {"pergunta": "O que significa DNS?", "opcoes": ["A) Domain Network System", "B) Domain Name System", "C) Data Network System", "D) Dynamic Network System"], "resposta": "B"},
            {"pergunta": "Qual a diferença entre IPv4 e IPv6?", "opcoes": ["A) Quantidade de endereços possíveis", "B) Velocidade de conexão", "C) Protocolo de segurança", "D) Capacidade de dados"], "resposta": "A"},
            {"pergunta": "O que é um switch de rede?", "opcoes": ["A) Dispositivo que distribui internet", "B) Dispositivo que roteia pacotes de dados", "C) Dispositivo de armazenamento", "D) Dispositivo para conectar dispositivos"], "resposta": "D"},
            {"pergunta": "Qual tipo de conexão é usada para conectar dispositivos em uma rede local?", "opcoes": ["A) Bluetooth", "B) Ethernet", "C) Wi-Fi", "D) NFC"], "resposta": "B"},
            {"pergunta": "O que é uma rede peer-to-peer?", "opcoes": ["A) Rede centralizada", "B) Rede onde todos os dispositivos são iguais", "C) Rede com um servidor central", "D) Rede privada"], "resposta": "B"},
            {"pergunta": "O que é um roteador?", "opcoes": ["A) Dispositivo de armazenamento", "B) Dispositivo que distribui internet", "C) Dispositivo de entrada", "D) Dispositivo de segurança"], "resposta": "B"},
        ]

    def perguntas_fase3(self):
        return [
            {"pergunta": "O que é criptografia?", "opcoes": ["A) Método de compressão de dados", "B) Método de esconder informações", "C) Método de validação de identidade", "D) Método de troca de dados"], "resposta": "B"},
            {"pergunta": "Qual é o objetivo de um firewall?", "opcoes": ["A) Armazenar dados", "B) Controlar o acesso à rede", "C) Proteger contra vírus", "D) Monitorar tráfego de rede"], "resposta": "B"},
            {"pergunta": "O que é autenticação multifatorial?", "opcoes": ["A) Uso de uma senha longa", "B) Uso de vários métodos de verificação", "C) Uso de biometria", "D) Verificação de dispositivos"], "resposta": "B"},
            {"pergunta": "O que é um ataque DDoS?", "opcoes": ["A) Ataque por injeção de código", "B) Ataque que utiliza múltiplos dispositivos", "C) Ataque a servidores de e-mail", "D) Ataque por força bruta"], "resposta": "B"},
            {"pergunta": "O que é um certificado SSL?", "opcoes": ["A) Protocolo de segurança para e-mails", "B) Protocolo de segurança para navegação web", "C) Método de autenticação", "D) Algoritmo de criptografia"], "resposta": "B"},
            {"pergunta": "O que significa phishing?", "opcoes": ["A) Um tipo de malware", "B) Técnica de fraude para roubo de informações", "C) Ataque a servidores", "D) Método de firewall"], "resposta": "B"},
            {"pergunta": "O que é uma VPN?", "opcoes": ["A) Rede privada virtual", "B) Sistema de detecção de intrusos", "C) Antivírus", "D) Protocolo de segurança"], "resposta": "A"},
            {"pergunta": "O que é a técnica de engenharia social?", "opcoes": ["A) Roubo de dados por força bruta", "B) Manipulação psicológica para obter informações", "C) Exposição de vulnerabilidades", "D) Ataque por injeção de código"], "resposta": "B"},
            {"pergunta": "O que são cookies?", "opcoes": ["A) Arquivos de backup", "B) Pequenos arquivos de dados armazenados pelo navegador", "C) Senhas criptografadas", "D) Dados de rede"], "resposta": "B"},
            {"pergunta": "Qual é o risco de usar senhas fracas?", "opcoes": ["A) Aumento do tráfego de rede", "B) Vulnerabilidade a ataques de força bruta", "C) Queda de desempenho", "D) Perda de dados"], "resposta": "B"},
        ]

    def perguntas_fase4(self):
        return [
            {"pergunta": "O que é um algoritmo?", "opcoes": ["A) Conjunto de regras para realizar uma tarefa", "B) Linguagem de programação", "C) Software de automação", "D) Sistema operacional"], "resposta": "A"},
            {"pergunta": "Qual é a principal função de um loop?", "opcoes": ["A) Executar uma ação repetidamente", "B) Verificar um erro", "C) Processar dados", "D) Armazenar informações"], "resposta": "A"},
            {"pergunta": "O que é um array?", "opcoes": ["A) Estrutura de dados para armazenar múltiplos valores", "B) Função matemática", "C) Comando de controle", "D) Tipo de dado inteiro"], "resposta": "A"},
            {"pergunta": "Qual a diferença entre variável e constante?", "opcoes": ["A) Variável pode ser alterada, constante não", "B) Variável é usada em loops, constante não", "C) Constante é usada em funções", "D) Nenhuma diferença"], "resposta": "A"},
            {"pergunta": "O que é recursão?", "opcoes": ["A) Função que chama a si mesma", "B) Função que verifica erros", "C) Função de controle de fluxo", "D) Função de ordenação"], "resposta": "A"},
            {"pergunta": "Qual é a finalidade de um laço 'for'?", "opcoes": ["A) Loop com número de repetições pré-determinado", "B) Loop com número de repetições indefinido", "C) Função de ordenação", "D) Verificação de condição"], "resposta": "A"},
            {"pergunta": "O que é uma função em programação?", "opcoes": ["A) Conjunto de instruções reutilizáveis", "B) Conjunto de variáveis", "C) Comando de controle", "D) Tipo de dado"], "resposta": "A"},
            {"pergunta": "O que significa o termo 'debugging'?", "opcoes": ["A) Verificação de erros no código", "B) Criação de novas funções", "C) Compilação do código", "D) Execução de código"], "resposta": "A"},
            {"pergunta": "Qual linguagem de programação é usada para o desenvolvimento web?", "opcoes": ["A) Java", "B) Python", "C) HTML", "D) C++"], "resposta": "C"},
            {"pergunta": "O que é um banco de dados relacional?", "opcoes": ["A) Banco de dados sem estrutura definida", "B) Banco de dados que organiza informações em tabelas", "C) Banco de dados que usa índices para buscar dados", "D) Banco de dados criptografado"], "resposta": "B"},
        ]

    def perguntas_fase5(self):
        return [
            {"pergunta": "O que é SQL?", "opcoes": ["A) Sistema de controle de versão", "B) Linguagem de consulta estruturada", "C) Sistema de banco de dados", "D) Tipo de servidor"], "resposta": "B"},
            {"pergunta": "O que é normalização de dados?", "opcoes": ["A) Processamento de dados em tempo real", "B) Eliminar redundância de dados", "C) Aumento da segurança de dados", "D) Método de backup de dados"], "resposta": "B"},
            {"pergunta": "O que é uma tabela em um banco de dados?", "opcoes": ["A) Armazenamento de arquivos", "B) Conjunto de registros", "C) Conjunto de algoritmos", "D) Tipo de índice"], "resposta": "B"},
            {"pergunta": "Qual comando SQL é usado para inserir dados?", "opcoes": ["A) SELECT", "B) INSERT", "C) UPDATE", "D) DELETE"], "resposta": "B"},
            {"pergunta": "O que é uma chave primária?", "opcoes": ["A) Chave que identifica unicamente uma linha em uma tabela", "B) Chave usada para criptografar dados", "C) Chave usada para armazenar dados", "D) Chave para backup"], "resposta": "A"},
            {"pergunta": "O que significa JOIN em SQL?", "opcoes": ["A) Junção de duas tabelas", "B) Abertura de uma conexão", "C) Exclusão de uma tabela", "D) Criação de um banco de dados"], "resposta": "A"},
            {"pergunta": "Qual é a função de um índice no banco de dados?", "opcoes": ["A) Organizar dados para facilitar a busca", "B) Armazenar dados criptografados", "C) Fazer backup de dados", "D) Eliminar dados redundantes"], "resposta": "A"},
            {"pergunta": "O que é uma consulta SELECT?", "opcoes": ["A) Consulta de dados em uma tabela", "B) Comando para inserir dados", "C) Comando para atualizar dados", "D) Comando para excluir dados"], "resposta": "A"},
            {"pergunta": "O que significa a cláusula WHERE em SQL?", "opcoes": ["A) Definir condições para uma consulta", "B) Definir qual tabela será usada", "C) Definir qual tipo de dado será consultado", "D) Definir a estrutura de uma tabela"], "resposta": "A"},
            {"pergunta": "O que é uma transação em SQL?", "opcoes": ["A) Uma operação que modifica dados", "B) Uma operação de backup", "C) Uma operação de segurança", "D) Uma operação de indexação"], "resposta": "A"},
        ]

    def iniciar_jogo(self):
        self.nome_jogador = self.name_entry.get()
        if not self.nome_jogador:
            messagebox.showwarning("Aviso", "Por favor, insira seu nome.")
            return
        pygame.mixer.music.play(-1)
        self.entry_frame.place_forget()  # Remove o frame de entrada

        # Frame do jogo
        self.question_frame = tk.Frame(self.master, bg="white")
        self.question_frame.place(relwidth=1, relheight=1)  # Garanta que a tela ocupe a tela inteira

        # Adicionar GIF de fundo
        background_label = AnimatedGIF(self.question_frame, r"C:\Users\lb16243\Downloads\FUNDO GAME.gif")
        background_label.place(relwidth=1, relheight=1)  # Preenche a tela inteira com o GIF

        # Rótulo da pergunta
        self.pergunta_label = tk.Label(self.question_frame, text="", wraplength=900, bg="white", font=("Arial", 14))
        self.pergunta_label.pack(pady=10)

        # Rótulo do timer
        self.timer_label = tk.Label(self.question_frame, text="", bg="white", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        # Rótulo da pontuação
        self.pontuacao_label = tk.Label(self.question_frame, text=f"Pontuação: {self.pontuacao}", bg="white", font=("Arial", 12))
        self.pontuacao_label.pack(pady=5)

        # Opções de respostas (Radio buttons)
        self.opcoes_var = tk.StringVar()
        self.opcoes = [tk.Radiobutton(self.question_frame, variable=self.opcoes_var, value=opcao, bg="white", font=("Arial", 12)) for opcao in ["A", "B", "C", "D"]]
        for opcao in self.opcoes:
            opcao.pack(anchor='w')

        # Resultado após a resposta
        self.resultado_label = tk.Label(self.question_frame, text="", bg="white", font=("Arial", 12))
        self.resultado_label.pack(pady=5)

        # Botões de ação
        self.button_frame = tk.Frame(self.question_frame, bg="white", bd=2, relief="flat", padx=10, pady=10)
        self.button_frame.pack(pady=20)

        # Botões de ação
        tk.Button(self.button_frame, text="Responder", command=self.verificar_resposta, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(self.button_frame, text="Pular Pergunta", command=self.pular_pergunta, bg="#FFC107", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(self.button_frame, text="Ranking", command=self.mostrar_ranking, bg="#FFC107", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(self.button_frame, text="Regras", command=self.mostrar_regras, bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(self.button_frame, text="Ajuda", command=self.mostrar_ajuda, bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(self.button_frame, text="Sair", command=self.show_game_over, bg="#F44336", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)

        self.load_questions()
        self.iniciar_fase()

    def iniciar_fase(self):
        fase = self.fases[self.fase_atual]
        pergunta_info = fase["perguntas"][self.pergunta_index]
        self.pergunta_label.config(text=pergunta_info["pergunta"])
        for i, opcao in enumerate(pergunta_info["opcoes"]):
            self.opcoes[i].config(text=opcao)

        self.start_timer()

    def start_timer(self):
        self.time_left = 30
        self.timer_label.config(text=f"Tempo restante: {self.time_left}s")
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Tempo restante: {self.time_left}s")
            self.timer = self.master.after(1000, self.update_timer)
        else:
            self.verificar_resposta()

    def verificar_resposta(self):
        fase = self.fases[self.fase_atual]
        pergunta_info = fase["perguntas"][self.pergunta_index]
        resposta_correta = pergunta_info["resposta"]
        resposta_dada = self.opcoes_var.get()

        if resposta_dada == resposta_correta:
            self.resultado_label.config(text="Correto!", fg="green")
            self.pontuacao += 10
            self.respostas_corretas_consecutivas += 1
            if self.respostas_corretas_consecutivas == 5:
                self.pontuacao += 50
                self.respostas_corretas_consecutivas = 0
        else:
            self.resultado_label.config(text="Incorreto!", fg="red")
            if self.fase_atual >= 2:
                self.pontuacao -= 20

        self.pontuacao_label.config(text=f"Pontuação: {self.pontuacao}")
        self.pular_pergunta()

    def pular_pergunta(self):
        self.pergunta_index += 1
        if self.pergunta_index >= len(self.fases[self.fase_atual]["perguntas"]):
            self.fase_atual += 1
            self.pergunta_index = 0
        if self.fase_atual >= len(self.fases):
            self.show_game_over()
        else:
            self.iniciar_fase()

    def mostrar_ranking(self):
        ranking_window = Toplevel(self.master)
        ranking_window.title("Ranking")
        ranking_window.geometry("1000x800")

        # Adicionar GIF e som de fundo
        background_label = AnimatedGIF(ranking_window, r"C:\Users\lb16243\Downloads\ranking.gif")
        background_label.place(relwidth=1, relheight=1)  # Preenche a tela inteira com o GIF
        pygame.mixer.music.load(self.som_ranking)  # Carrega o som do ranking
        pygame.mixer.music.play(-1)  # Toca a música em loop

        tk.Label(ranking_window, text="Ranking dos Mestres de TI", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(ranking_window, text="1. João - 500 pontos", font=("Arial", 12)).pack(pady=5)
        tk.Label(ranking_window, text="2. Maria - 450 pontos", font=("Arial", 12)).pack(pady=5)
        tk.Label(ranking_window, text="3. Pedro - 400 pontos", font=("Arial", 12)).pack(pady=5)

        # Botões para iniciar o jogo e sair
        button_frame = tk.Frame(ranking_window, bg="white")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Iniciar Partida", command=self.iniciar_jogo, bg="#4CAF50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        tk.Button(button_frame, text="Sair", command=self.master.quit, bg="#F44336", fg="white", font=("Arial", 14)).pack(side="left", padx=10)

    def mostrar_regras(self):
        messagebox.showinfo("Regras", """ 
        1. Limite de tempo: 30 segundos por pergunta.
        2. Pontuação: 10 pontos por resposta correta.
        3. Ajuda: 2 ajudas por jogo. 
        4. Penalização: Respostas incorretas diminuem pontos após a Fase 3.
        5. Objetivo: Terminar as fases com o maior número de pontos e alcançar o título de Mestre de TI.
        """)

    def mostrar_ajuda(self):
        messagebox.showinfo("Ajuda", """ 
        1. Pular Pergunta: Quando não souber a resposta, pode pular a pergunta.
        2. Eliminar Respostas: Elimina 2 respostas incorretas, ajudando a escolher a correta.
        3. Lembre-se de que você tem um tempo limitado para responder as questões!
        """)

    def show_game_over(self):
        pygame.mixer.music.stop()
        game_over_window = Toplevel(self.master)
        game_over_window.title("Fim de Jogo")
        game_over_window.geometry("1000x800")

        background_label = AnimatedGIF(game_over_window, r"C:\Users\lb16243\Downloads\gameover.gif")
        background_label.place(relwidth=1, relheight=1)

        pygame.mixer.music.load(self.som_fim_jogo)
        pygame.mixer.music.play()

        messagebox.showinfo("Fim de Jogo", f"Parabéns, {self.nome_jogador}! Sua pontuação final foi: {self.pontuacao}.")
        self.master.quit()

# Iniciar o jogo
root = tk.Tk()
jogo = JogoDePerguntas(root)
root.mainloop()
