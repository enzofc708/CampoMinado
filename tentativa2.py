from Tkinter import *
from time import time
from random import randint
from random import seed
import tkMessageBox
#from Tkinter import simpledialog


seed(int(time()))    # Gerando a seed inicial do nosso randomizador



def criarMenu(toplevel, matriz, botoes, inicio):  # Cria a barra de menu no topo do programa, com as opcoes
    global marcadores                             # de tamanho e uma opcao de sair do programa.
    menu = Menu(toplevel)
    menuTamanhos = Menu(toplevel, tearoff=0)
    menuTamanhos.add_command(label="Pequeno (9x9 e 10 minas)", command = lambda : recomecarJogo(toplevel,matriz,botoes, inicio, 9, 9, 10))
    menuTamanhos.add_command(label="Medio (16x16 e 40 minas)", command = lambda : recomecarJogo(toplevel,matriz,botoes, inicio, 16, 16, 40))
    menuTamanhos.add_command(label="Grande (24x24 e 100 minas)", command = lambda : recomecarJogo(toplevel,matriz,botoes, inicio, 24, 24, 100))
    menuTamanhos.add_command(label="Customizado", command = lambda : tamanhoCustomizado(toplevel,matriz,botoes, inicio))
    menuTamanhos.add_separator()
    menu.add_cascade(label="Alterar Tamanho", menu=menuTamanhos)
    menu.add_command(label="Sair", command = lambda: toplevel.destroy())
    toplevel.config(menu=menu)


def tamanhoCustomizado(toplevel,matriz,botoes, inicio):   #Funcao que cria um novo tabuleiro com tamanho customizado

    janela = Toplevel()
    labelLados = Label(janela, text = "Numero de Lados:")
    labelMina = Label(janela, text = "Numero de Minas:")
    entryLados = Entry(janela)
    entryMinas = Entry(janela)
    labelLados.grid(column = 1, row = 1)
    entryLados.grid(column = 2, row = 1)
    labelMina.grid(column = 1, row = 2)
    entryMinas.grid(column = 2, row = 2)
    lados = 0
    numMinas = 0
    ok = Button(janela, text ="OK", command = lambda : destruir_janela(toplevel, matriz, botoes, inicio, lados, numMinas, entryLados, entryMinas, janela))
    ok.grid(column = 2, row = 4)




def destruir_janela(toplevel, matriz, botoes, inicio, lados, numMinas, entryLados, entryMinas, janela):
    lados = int(entryLados.get())
    numMinas = int(entryMinas.get())
    janela.destroy()
    recomecarJogo(toplevel, matriz, botoes, inicio, lados, lados, numMinas)



def gerarMatriz(linhas,colunas,numMinas):   # Funcao que gera a matriz das minas do jogo, tamanho default 9x9

    matriz = []
    for i in range(linhas+2):          # Esse 'for' cria uma matiz de 0's com os tamanhos especificados,com uma
        linha = []                     # borda para evitar index out of bounds
        for j in range(colunas+2):
            linha.append(0)
        matriz.append(linha)

    for i in range(numMinas):       #Gera uma posicao aleatoria p/ bomba
        linhaBomba = randint(1,linhas)
        colunaBomba = randint(1,colunas)
        while matriz[linhaBomba][colunaBomba] == -1:     # Verifica se uma bomba ja foi colocada nessa posicao
            linhaBomba = randint(1,linhas)
            colunaBomba = randint(1,colunas)
        matriz[linhaBomba][colunaBomba] = -1              #Coloca a bomba, representado por -1 na nossa matriz

    for i in range(1,linhas+1):                    #Conta quantas bombas existem na adjacencia de cada vertice
        for j in range(1,colunas+1):
            if matriz[i][j] != -1:
                if matriz[i+1][j] == -1:
                    matriz[i][j] +=1;
                if matriz[i+1][j+1] == -1:
                    matriz[i][j] +=1;
                if matriz[i+1][j-1] == -1:
                    matriz[i][j] +=1;
                if matriz[i][j+1] == -1:
                    matriz[i][j] +=1;
                if matriz[i][j-1] == -1:
                    matriz[i][j] +=1;
                if matriz[i-1][j-1] == -1:
                    matriz[i][j] +=1;
                if matriz[i-1][j] == -1:
                    matriz[i][j] +=1;
                if matriz[i-1][j+1] == -1:
                    matriz[i][j] +=1;
    return matriz


def cliqueNoBotao(x,y,botoes,matriz):               # Funcao que rege o clique nos botoes
    global jogoFinalizado
    if jogoFinalizado:                   # Impede que o usuario clique em botoes apos o encerramento do jogo
        return
    botoes[x][y]['text'] = str(matriz[x+1][y+1])
    if matriz[x+1][y+1] == 0:
        botoes[x][y]['text'] = ' '
        autoClique(x,y,botoes,matriz)
    elif matriz[x+1][y+1] == -1:         # Detecta se um usuario clica numa bomba
        botoes[x][y]['text'] = '*'
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if matriz[i][j] == -1:
                    botoes[i-1][j-1]['text'] = '*'
        tkMessageBox.showinfo("KABOOOM","Voce Perdeu.")
        jogoFinalizado = True

    botoes[x][y]['state'] = 'disabled'
    botoes[x][y].config(relief = SUNKEN)
    checarVitoria(botoes, matriz)      # Checa, apos cada clique, se o jogo encerrou


def autoClique(x, y, botoes, matriz):        # Funcao que controla o clique nos espacos em branco
    if botoes[x][y]["state"] == "disabled":
        return                               # Marca o fim da recursao

    if matriz[x+1][y+1] != 0:
        botoes[x][y]["state"] = "disabled"
        botoes[x][y].config(relief= SUNKEN)
        botoes[x][y]["text"] = str(matriz[x+1][y+1])

    else:
        botoes[x][y]["text"] = " "
        botoes[x][y].config(relief= SUNKEN)
        botoes[x][y]['state'] = 'disabled'

    if matriz[x+1][y+1] == 0:                   #Clica recursivamente nos espacos em branco adjacentes
        if x != 0 and y != 0:
            autoClique(x-1,y-1,botoes,matriz)
        if x != 0:
            autoClique(x-1,y,botoes,matriz)
        if x != 0 and y != len(botoes[0])-1:
            autoClique(x-1,y+1,botoes,matriz)
        if y != 0:
            autoClique(x,y-1,botoes,matriz)
        if y != len(botoes[0])-1:
            autoClique(x,y+1,botoes,matriz)
        if x != len(botoes)-1 and y != 0:
            autoClique(x+1,y-1,botoes,matriz)
        if x != len(botoes)-1:
            autoClique(x+1,y,botoes,matriz)
        if x != len(botoes)-1 and y != len(botoes[0])-1:
            autoClique(x+1,y+1,botoes,matriz)


def cliqueBotaoDireito(event,x,y,botoes):           # Rege a "marcacao" dos botoes
    global jogoFinalizado, marcadores, indicadorMarcadores
    if jogoFinalizado:
        return

    if botoes[x][y]["text"] == "?":
        botoes[x][y]["text"] = " "
        botoes[x][y]["state"] = "active"
        marcadores = marcadores + 1
        indicadorMarcadores.destroy()
        indicadorMarcadores = Label(text = "Marcadores Restantes: " + str(marcadores) )
        indicadorMarcadores.pack()
    elif botoes[x][y]["text"] == " " and  botoes[x][y]["state"] == "active" and marcadores > 0:
        botoes[x][y]["text"] = "?"
        botoes[x][y]["state"] = "disabled"
        marcadores = marcadores - 1
        indicadorMarcadores.destroy()
        indicadorMarcadores = Label(text = "Marcadores Restantes: " + str(marcadores) )
        indicadorMarcadores.pack()





def checarVitoria(botoes,matriz):               # Checa se o usuario ganhou a partida
    global jogoFinalizado
    for i in range(len(botoes)):
        for j in range(len(botoes[0])):
            if matriz[i+1][j+1] !=-1 and botoes[i][j]["state"] == "normal":
                return

    tkMessageBox.showinfo("PARABENS!","VOCE GANHOU!!!")
    jogoFinalizado = True

def recomecarJogo(toplevel, matriz, botoes, inicio, linhas, colunas, numMinas):    # Destroi o tabuleiro atual
    for i in toplevel.winfo_children():                                            # e cria um novo no lugar
        i.destroy()
    criarMenu(toplevel, matriz, botoes, inicio)
    preJogo(matriz, botoes, inicio, linhas, colunas, numMinas)


def preJogo(matriz, botoes,inicio,linhas = 9, colunas = 9, numMinas = 10): # Realiza os procedimentos pre-jogo
    global jogoFinalizado, marcadores, indicadorMarcadores
    marcadores = numMinas
    jogoFinalizado = False
    inicio = Frame(raiz)
    inicio.pack()
    matriz = []
    matriz = gerarMatriz(linhas, colunas, numMinas)   #Gerando o tabuleiro inicial
    botoes = []
    for i in range(linhas):            #Criando um grid com j colunas e i linhas de botoes
        botoes.append([])
        for j in range(colunas):
            btn = Button(inicio, width = 2, text = " ", command = lambda x=i,y=j: cliqueNoBotao(x,y,botoes,matriz))
            btn.bind("<Button-3>", lambda event, x = i, y = j, botoes = botoes : cliqueBotaoDireito(event, x, y, botoes))
            btn.config(disabledforeground= "black")
            btn.grid(column = j, row = i, sticky = N+ W+ S+ E)
            botoes[i].append(btn)
    indicadorMarcadores = Label(text = "Marcadores Restantes: " + str(marcadores))
    indicadorMarcadores.pack()



raiz = Tk()
raiz.title("Campo Minado")


inicio = Frame(raiz)
inicio.pack()
matriz = []
botoes = []
jogoFinalizado = False
marcadores = 10
indicadorMarcadores = Label()
criarMenu(raiz, matriz, botoes, inicio)
preJogo(matriz,botoes,inicio)


raiz.mainloop()
