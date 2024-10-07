import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import pygame
import json
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
        return [ImageTk.PhotoImage(img.copy()) for i in range(img.n_frames) if img.seek(i) or img.copy()]

    def animate(self):
        self.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(100, self.animate)

class JogoDePerguntas:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        pygame.mixer.init()
        self.load_sounds()
        self.setup_frames()
        self.setup_game_variables()
        self.load_questions()

    def setup_window(self):
        self.master.title("Jogo de Perguntas e Respostas")
        self.master.geometry("1000x800")
        self.master.configure(bg="#f0f0f0")

    def setup_frames(self):
        self.question_frame = Toplevel(self.master)  # New window for the question frame
        self.question_frame.title("Perguntas")
        self.question_frame.geometry("400x500")
        self.question_frame.configure(bg="white")

        background_label = AnimatedGIF(self.question_frame, r"C:\Users\lb16243\Downloads\FUNDO GAME.gif")
        background_label.place(relwidth=1, relheight=1)

        tk.Label(self.question_frame, text="Teste seus Conhecimentos!", font=("Arial", 20, "bold"), bg="white").pack(pady=10)

        self.pergunta_label = tk.Label(self.question_frame, text="", wraplength=380, bg="white", font=("Arial", 14))
        self.pergunta_label.pack(pady=10)

        self.timer_label = tk.Label(self.question_frame, text="", bg="white", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        self.opcoes_var = tk.StringVar()
        self.opcoes = [tk.Radiobutton(self.question_frame, variable=self.opcoes_var, value=opcao, bg="white", font=("Arial", 12)) for opcao in ["A", "B", "C", "D"]]
        for opcao in self.opcoes:
            opcao.pack(anchor='w')

        self.resultado_label = tk.Label(self.question_frame, text="", bg="white", font=("Arial", 12))
        self.resultado_label.pack(pady=5)

        self.button_frame = tk.Frame(self.question_frame, bg="white", bd=2, relief="flat", padx=10, pady=10)
        self.button_frame.pack(pady=20)

        tk.Button(self.button_frame, text="Responder", command=self.verificar_resposta, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(self.button_frame, text="Ranking", command=self.mostrar_ranking, bg="#FFC107", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(self.button_frame, text="Regras", command=self.mostrar_regras, bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(self.button_frame, text="Sair", command=self.show_game_over, bg="#F44336", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(self.button_frame, text="Ajuda", command=self.mostrar_ajuda, bg="#FF5722", fg="white", font=("Arial", 12, "bold")).pack(side='left', padx=5)

    def setup_game_variables(self):
        self.pontuacao = 0
        self.fase_atual = 0
        self.nome_jogador = ""
        self.fases = []
        self.timer = None
        self.time_left = 30  # Set timer for 30 seconds

    def load_sounds(self):
        pygame.mixer.music.load("C:\\Users\\lb16243\\Downloads\\mario-type-beat-131248.mp3")
        self.som_fim_jogo = "C:\\Users\\lb16243\\Downloads\\game over.mp3"

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
            {"pergunta": "Qual componente é o 'coração' do computador?", "opcoes": ["A) Memória RAM", "B) Processador", "C) Disco rígido", "D) Placa-mãe"], "resposta": "B"},
            {"pergunta": "Qual é a função do sistema operacional?", "opcoes": ["A) Gerenciar hardware e software", "B) Armazenar dados", "C) Proteger contra vírus", "D) Realizar cálculos"], "resposta": "A"},
        ]

    def perguntas_fase2(self):
        return [
            {"pergunta": "O que é um servidor?", "opcoes": ["A) Software", "B) Computador que fornece serviços", "C) Dispositivo de entrada", "D) Sistema operacional"], "resposta": "B"},
            {"pergunta": "Qual protocolo para enviar e-mails?", "opcoes": ["A) FTP", "B) SMTP", "C) HTTP", "D) POP3"], "resposta": "B"},
            {"pergunta": "O que significa IP?", "opcoes": ["A) Internet Protocol", "B) Interconnected Protocol", "C) Internal Protocol", "D) Internet Provider"], "resposta": "A"},
            {"pergunta": "Função de um roteador?", "opcoes": ["A) Armazenar dados", "B) Conectar redes", "C) Proteger contra vírus", "D) Realizar backup"], "resposta": "B"},
            {"pergunta": "Principal função de um firewall?", "opcoes": ["A) Acelerar a internet", "B) Proteger a rede", "C) Gerenciar armazenamento", "D) Controlar temperatura"], "resposta": "B"},
        ]

    def perguntas_fase3(self):
        return [
            {"pergunta": "O que é um firewall?", "opcoes": ["A) Software de proteção", "B) Tipo de antivírus", "C) Dispositivo de armazenamento", "D) Protocolo de segurança"], "resposta": "A"},
            {"pergunta": "O que é criptografia?", "opcoes": ["A) Método de compressão", "B) Proteção de dados", "C) Protocolo de rede", "D) Tipo de software"], "resposta": "B"},
        ]

    def perguntas_fase4(self):
        return [
            {"pergunta": "O que é um algoritmo?", "opcoes": ["A) Conjunto de instruções", "B) Tipo de software", "C) Dispositivo de entrada", "D) Hardware"], "resposta": "A"},
            {"pergunta": "Qual é a linguagem de programação mais popular?", "opcoes": ["A) Java", "B) HTML", "C) CSS", "D) Assembly"], "resposta": "A"},
        ]

    def perguntas_fase5(self):
        return [
            {"pergunta": "O que é um banco de dados?", "opcoes": ["A) Conjunto de dados organizados", "B) Tipo de software", "C) Protocolo de rede", "D) Dispositivo de armazenamento"], "resposta": "A"},
            {"pergunta": "Qual é a função de SQL?", "opcoes": ["A) Gerenciar hardware", "B) Manipular dados", "C) Proteger redes", "D) Compilar código"], "resposta": "B"},
        ]

    def iniciar_jogo(self, nome):
        self.nome_jogador = nome
        if not self.nome_jogador:
            messagebox.showwarning("Aviso", "Por favor, insira seu nome.")
            return
        pygame.mixer.music.play(-1)  # Play background music
        self.question_frame.pack(fill="both", expand=True)
        self.iniciar_fase()

    def iniciar_fase(self):
        if self.fase_atual < len(self.fases):
            self.atualizar_pergunta()
            self.start_timer()
        else:
            self.finalizar_jogo()

    def atualizar_pergunta(self):
        fase = self.fases[self.fase_atual]
        pergunta_info = fase["perguntas"][self.pontuacao]
        self.pergunta_label.config(text=f"Fase {self.fase_atual + 1}: {pergunta_info['pergunta']}")
        for i, opcao in enumerate(pergunta_info["opcoes"]):
            self.opcoes[i].config(text=opcao)
            self.opcoes[i].pack(anchor='w')
        self.timer_label.config(text=f"Tempo: {self.time_left} segundos")
        self.resultado_label.config(text="")
        self.pergunta_label.pack(pady=10)

    def start_timer(self):
        self.time_left = 30  # Reset time for 30 seconds
        self.timer_label.config(text=f"Tempo: {self.time_left} segundos")
        self.countdown()

    def countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Tempo: {self.time_left} segundos")
            self.timer = self.master.after(1000, self.countdown)
        else:
            self.resultado_label.config(text="Tempo esgotado!", fg="red")
            self.verificar_resposta(False)  # Treat as incorrect answer

    def verificar_resposta(self, was_user_answered=True):
        if was_user_answered:
            fase = self.fases[self.fase_atual]
            pergunta_info = fase["perguntas"][self.pontuacao]
            self.resultado_label.config(text="Correto!" if self.opcoes_var.get() == pergunta_info["resposta"] else "Incorreto!",
                                         fg="green" if self.opcoes_var.get() == pergunta_info["resposta"] else "red")

            if self.opcoes_var.get() == pergunta_info["resposta"]:
                self.pontuacao += 1

        if self.pontuacao >= len(fase["perguntas"]):
            self.inserir_no_ranking()
            self.fase_atual += 1
            self.pontuacao = 0
            self.iniciar_fase()
        else:
            self.atualizar_pergunta()

    def inserir_no_ranking(self):
        ranking = []
        if os.path.exists("ranking.json"):
            with open("ranking.json", "r") as f:
                ranking = json.load(f)

        ranking.append({"nome": self.nome_jogador, "pontuacao": self.pontuacao})

        with open("ranking.json", "w") as f:
            json.dump(ranking, f)

    def mostrar_ranking(self):
        ranking_window = Toplevel(self.master)
        ranking_window.title("Ranking")
        ranking_window.geometry("500x400")
        ranking_window.configure(bg="white")

        background_label = AnimatedGIF(ranking_window, r"C:\Users\lb16243\Downloads\ranking.gif")
        background_label.place(relwidth=1, relheight=1)

        pygame.mixer.music.load(r"C:\Users\lb16243\Downloads\mario rankig.mp3")
        pygame.mixer.music.play(-1)  # Play ranking music

        if not os.path.exists("ranking.json"):
            messagebox.showinfo("Ranking", "Ainda não há mestres da TI.")
            ranking_window.destroy()
            return

        with open("ranking.json", "r") as f:
            ranking = json.load(f)

        ranking.sort(key=lambda x: x["pontuacao"], reverse=True)
        ranking_texto = "\n".join(f"{item['nome']}: {item['pontuacao']}" for item in ranking)

        tk.Label(ranking_window, text="Ranking", font=("Arial", 20), bg="white").pack(pady=10)
        ranking_label = tk.Label(ranking_window, text=ranking_texto or "Ranking vazio.", bg="white", font=("Arial", 14))
        ranking_label.pack(pady=10)

    def mostrar_regras(self):
        regras = "Regras do Jogo:\n\n" \
                 "1. Responda corretamente para ganhar pontos.\n" \
                 "2. Você pode pular perguntas.\n" \
                 "3. O objetivo é a maior pontuação possível.\n"
        messagebox.showinfo("Regras", regras)

    def mostrar_ajuda(self):
        fase = self.fases[self.fase_atual]
        pergunta_info = fase["perguntas"][self.pontuacao]
        messagebox.showinfo("Ajuda", f"Dica: A resposta correta está entre: {', '.join(pergunta_info['opcoes'])}")

    def show_game_over(self):
        self.question_frame.withdraw()  # Hide the question window
        self.finalizar_jogo()

    def finalizar_jogo(self):
        pygame.mixer.music.stop()  # Stop background music
        pygame.mixer.music.load(self.som_fim_jogo)
        pygame.mixer.music.play(-1)  # Play game over music

        # New Game Over Window
        game_over_window = Toplevel(self.master)
        game_over_window.title("Fim de Jogo")
        game_over_window.geometry("500x400")
        game_over_window.configure(bg="white")

        background_label = AnimatedGIF(game_over_window, r"C:\Users\lb16243\Downloads\gameover.gif")
        background_label.place(relwidth=1, relheight=1)

        tk.Label(game_over_window, text=f"Você finalizou o jogo com {self.pontuacao} pontos!", font=("Arial", 16), bg="white").pack(pady=20)

        button_frame = tk.Frame(game_over_window, bg="white")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Sair", command=self.master.quit, bg="#F44336", fg="white", font=("Arial", 12)).pack(side='left', padx=5)
        tk.Button(button_frame, text="Nova Partida", command=self.resetar_jogo, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side='left', padx=5)
        tk.Button(button_frame, text="Registrar no Ranking", command=self.inserir_no_ranking, bg="#2196F3", fg="white", font=("Arial", 12)).pack(side='left', padx=5)

    def resetar_jogo(self):
        self.pontuacao = 0
        self.fase_atual = 0
        self.nome_jogador = ""
        self.opcoes_var.set(None)
        self.question_frame.destroy()  # Close the question window
        self.setup_frames()  # Reset the frames for new game

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDePerguntas(root)

    # Entry for player name
    entry_frame = tk.Frame(root, bg="#f0f0f0")
    entry_frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(entry_frame, text="Insira seu nome:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    nome_entry = tk.Entry(entry_frame, font=("Arial", 12))
    nome_entry.pack(pady=5)

    def start_game():
        jogo.iniciar_jogo(nome_entry.get())
        entry_frame.pack_forget()

    tk.Button(entry_frame, text="Iniciar Jogo", command=start_game, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    root.mainloop()
