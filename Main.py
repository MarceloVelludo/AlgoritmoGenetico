import numpy as np
import random


##Função que compara o objetivo com o individuo, caso forem iguais a distancia é acrescida de 1
def distanciaHamming(cromossomo):

    distancia = np.zeros(12)

    ##Para Treinar o algoritmo para capturar os 0, devemos definir o objetivo com o vetor abaixo.
    objetivo = np.array([1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1])
    for i in range(cromossomo.size):
        if cromossomo[i] == objetivo[i]:
            distancia[i] = + 1
    return distancia
##Fim distanciaHamming

##Função que verifica a aptidão dos individuos na solução do problema em questão.
##A tecnica utilizada para verificar a aptidão neste caso será a distância de Hamming.
def funcAptidao(populacao):
    aptidao = np.zeros((8, 12))
    for i in range(len(populacao)):
        ##Retira uma linha(Individuo) da matriz para fazer o calculo da distância.
        aptidao[i] = distanciaHamming(populacao[i])

    return aptidao
##Fim FuncAptidao

##Função para inicializar a matriz com 8 individuos.
def inicializa():

    return np.random.randint(2, size=(8, 12))
#Fim Inicializa

##Verifica se o critério de parada foi alcançado.
def verifica(aptidao):

    for i,elemento in enumerate(aptidao):
        soma = 0
        for i2, elemento2 in enumerate(elemento):
            soma += elemento2
        ##Criterio de Parada
        if soma == 12:
            print("O objetivo do algoritmo foi alcançado")
            return True
    else:
        return False
##Fim Verifica

##Seleciona os Individuos da população que participaram da reprodução.
##A seleção será feita pelo metodo da roleta.
def seleciona(populacao, aptidao):
    somaAptidao = 0

    selecao = np.zeros(8)
    roleta = np.zeros(8)
    somaIndividuo = np.zeros(8)
    somaTotal = 0

    #Soma Aptidão
    for i, elemento in enumerate(aptidao):
        for i2, elemento2 in enumerate(elemento):
            somaIndividuo[i] += elemento2

    for i in somaIndividuo:
        somaTotal += i

    #Divide Roleta entre os individuos
    for i in range(8):
        roleta[i] = (360*somaIndividuo[i])/somaTotal

    for i in range(8):
        #Gera numero aleatorio de (0,360]
        numeroAleatorio = random.randint(0,360)

        somaRoletaTeto = 0;
        somaRoletaPiso = 0;
        #Verifica a que individuo pertence o numero aleatorio e seleciona para reprodução
        for i2 in range(roleta.size):
            somaRoletaTeto += roleta[i2]
            if (somaRoletaTeto >= numeroAleatorio) and (somaRoletaPiso <= numeroAleatorio):
                selecao[i] = i2

            somaRoletaPiso = somaRoletaTeto

    return selecao
##Fim Seleciona

#Função que define o ponto de crossover e faz a troca gerando novos individuos
def crossOver(individuo1, individuo2, populacaoNova, count):
    pontodeCrossOver = 0
    pontodeCrossOver = np.random.randint(0, 12, 1)

    while pontodeCrossOver < len(individuo1):
        aux = individuo1[pontodeCrossOver]
        individuo1[pontodeCrossOver] = individuo2[pontodeCrossOver]
        individuo2[pontodeCrossOver] = aux
        pontodeCrossOver += 1

    populacaoNova[count] = individuo1
    populacaoNova[count+1] = individuo2
    return
#Fim CrossOver

#É gerado um numero aleatorio para cada par de individuos, se o numero aleatorio for maior que a porcentCrossover o cruzamento é realizado.
def reproduz(populacao, individuosSelecionados, porcentCrossover):

    count = 0
    populacaoNova = np.zeros((8, 12))

    while count < len(individuosSelecionados):
        #Para evitar frações a porcentagem de crossover foi multiplicada por 100.
        numeroAleatorio = random.randint(0, 100)

        if numeroAleatorio <= porcentCrossover:
            crossOver(populacao[int(individuosSelecionados[count])], populacao[int(individuosSelecionados[count+1])], populacaoNova, count)
        else:
            populacaoNova[count] = populacao[int(individuosSelecionados[count])]
            populacaoNova[count+1] = populacao[int(individuosSelecionados[count+1])]
        count += 2

    return populacaoNova


##Fim Reproduz

def variar(populacao, porcentMutacao):

    for i in range(len(populacao)):
        for i2 in range(len(populacao[i])):
            if random.randint(0, 100) <= porcentMutacao:
                if populacao[i][i2] == 0:
                    populacao[i][i2] = 1
                else:
                    populacao[i][i2] = 0



    return populacao
##Fim variar

def procedimento():

    porcentCrossover = 0
    porcentMutacao = 20

    #Inicializa contador de iterações.
    count = 1
    ##Inicializa a população.
    populacao = inicializa();

    print("\nPopulacao Inicial:\n", populacao)
    ##Calcula aptidão de cada individuo.
    aptidao = funcAptidao(populacao)
    print("\nAptidao:\n", aptidao)
    ##Equanto pelo menos 1 indiviuo não chegar no objetivo, o algoritmo prosseguirá
    while not verifica(aptidao):
        print("Interação:", count, "\nPopulação:\n", populacao)
        individuosSelecionados = seleciona(populacao, aptidao)
        print("\nIndividuos Selecionados:", individuosSelecionados)
        populacao = reproduz(populacao, individuosSelecionados, porcentCrossover)
        print("\nNova população após reprodução:\n", populacao)
        populacao = variar(populacao, porcentMutacao)
        print("\nNova população pós mutação:\n", populacao)
        ##Calcula aptidão de cada individuo.
        aptidao = funcAptidao(populacao)
        count += 1
    ##Fim do while

    return
#Fim Procedimento


##Começo Main
procedimento()

##Fim Main