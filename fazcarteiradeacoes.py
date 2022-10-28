# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 00:17:50 2022

@author: lucas
"""

#meu primeiro projeto

#importação das bíbliotecas
import pandas as pd
import fundamentus
from pandas_datareader import data as pdr
from time import sleep

#1 separar os setores das ações que estão contidas na bíblioteca fundamentus em listas
setor_valor_unico = [['Varejo', 7], ['Construção', 11], ['Educação', 12], ['Energia', 14], 
                     ['Hotel e Restaurante', 19], ['Bancário', 20], ['Serviços', 28], 
                     ['Seguros', 31], ['Consumo Pessoal', 32], ['Financeiro', 37], 
                     ['Telecomunicações', 40], ['Transporte', 41], ['Itens para casa', 42],
                     ['Entretenimento', 43]]

setor_valor_multiplo = [['Agronegócio', 1, [1, 3]], 
                        ['Infraestrutura', 2, [2, 17]],
                        ['Medicina', 4, [4, 15]],
                        ['Fabrica', 5, [5, 18, 21, 22, 36, 38]],
                        ['Alimentos e farmácia', 8, [8, 25]],
                        ['TI', 9, [9, 33]],
                        ['Imobiliario', 10, [10, 16]]
                        ]

#1.1 mensagem de boas vindas e escolha do setor
print("""
      -------------------------------------------------------------------------------------
                        BEM VINDO AO PROGRAMA FAZ CARTEIRA DE AÇÕES !!!
      -------------------------------------------------------------------------------------
      PROCURE AS AÇÕES QUE VOCÊ DESEJA ADQUIRIR ATRAVÉS DOS SETORES EM QUE VOCÊ QUER
      INVESTIR E O PROGRAMA IRÁ SEPARAR AS MELHORES AÇÕES DE CADA SETOR
      -------------------------------------------------------------------------------------
      DIGITE A QUANTIDADE DE SETORES QUE VOCÊ DESEJA COMPRAR AÇÕES E LOGO APÓS DIGITE O 
      NUMERO DE CADA SETOR, QUE ESTÁ REPRESENTADO ABAIXO...
      -------------------------------------------------------------------------------------
      AGRONEGOCIO (1)
      INFRAESTRUTURA (2)
      MEDICINA (4)
      FÁBRICA (5)
      VAREJO (7)
      ALIMENTOS E FARMÁCIA (8)
      TI (9)
      IMOBILIARIO (10)
      CONSTRUÇÃO (11)
      EDUCAÇÃO (12)
      ENERGIA (14)
      HOTEL E RESTAURANTE (19)
      BANCÁRIO (20)
      SERVIÇOS (28)
      SEGUROS (31)
      CONSUMO PESSOAL (32)
      FINANCEIRO (37)
      TELECOMUNICAÇÕES (40)
      TRANSPORTE (41)
      ITENS PARA CASA (42)
      ENTRETENIMENTO (43)
      
      
      """)

#2 perguntar quantos setores terá a carteira
a = True
while a == True:
    num_setores = input("Digite quantas repartições diferentes sua carteira terá: ")
    
    if num_setores.isnumeric():
        print('Ok, sua carteira terá {} setores'.format(num_setores))
        a = False
        
    else:    
        print("Você não digitou um número, por favor digite um número inteiro")
    
#2.1 para cada repartição abre roda o codigo
for r in range(0, int(num_setores)):
    print("""
          Setores:
              AGRONEGOCIO (1)
              INFRAESTRUTURA (2)
              MEDICINA (4)
              FÁBRICA (5)
              VAREJO (7)
              ALIMENTOS E FARMÁCIA (8)
              TI (9)
              IMOBILIARIO (10)
              CONSTRUÇÃO (11)
              EDUCAÇÃO (12)
              ENERGIA (14)
              HOTEL E RESTAURANTE (19)
              BANCÁRIO (20)
              SERVIÇOS (28)
              SEGUROS (31)
              CONSUMO PESSOAL (32)
              FINANCEIRO (37)
              TELECOMUNICAÇÕES (40)
              TRANSPORTE (41)
              ITENS PARA CASA (42)
              ENTRETENIMENTO (43)
              -----------------------""")
              
    numset = int(input("Digite o número do setor que você deseja: "))
    print("O setor foi selecionado")
    print("Espere um pouco para selecionar o outro setor")
    
    acoes_list = []
    
    #para cada valor na lista valor unico
    for setor in setor_valor_unico:
        
        #se o valor for igual ao valor da lista
        if numset == setor[1]:
            acoes = fundamentus.list_papel_setor(setor[1])
            
            for acao in acoes:
                acoes_list.append(acao)
    
    #para cada valor na lista valor multiplo            
    for setor in setor_valor_multiplo:
        
        #se o valor for igual ao valor da lista:
            if numset == setor[1]:
                for num in setor[2]:
                    acoes = fundamentus.list_papel_setor(num)
                    
                    for acao in acoes:
                        codigo_adaptado = acao + '.SA'
                        sleep(0.2)
                        acoes_list.append(codigo_adaptado)
                        
print("Espere um pouco, os setores já foram escolhidos")

dados = pdr.get_data_yahoo(symbols= acoes_list)

fechamento = dados['Adj Close']

retorno_diario = fechamento.resample("Y").last().pct_change().fillna(0)

print(retorno_diario)

lista_codigos = []
lista_retorno_5anos = []
lista_roe = []

for acao in retorno_diario.columns:
    codigo = acao[0:5]
    retorno_5anos = retorno_diario[acao].sum()
    
    lista_codigos.append(codigo)
    lista_retorno_5anos.append(retorno_5anos)
    
    fund = fundamentus.get_papel(codigo)
    
    try:
        roe = fund['ROE'][0]
        lista_roe.append(float(roe.rstrip('%')))
    
    except:
        lista_roe.append(0)
    
    
df = pd.DataFrame(zip(lista_codigos, lista_retorno_5anos, lista_roe),
                  columns=['Codigos', 'Retorno Ultimos 5 Anos', 'ROE'])  

df = df.sort_values(by = 'Retorno Ultimos 5 Anos')
df['Ranking Retorno Ultimos 5 Anos'] = df['Retorno Ultimos 5 Anos'].rank()

df = df.sort_values(by = 'ROE')
df['Ranking ROE'] = df['ROE'].rank()

df['Ranking Total'] = df['Ranking Retorno Ultimos 5 Anos'] + df['Ranking ROE']
df = df.sort_values(by = 'Ranking Total')

num = int(len(df.index)/2)
num = int(num/2)

dffinal = df.tail(num)
dffinal = dffinal.drop(['Ranking ROE'], axis=1).drop(['Ranking Total'], axis=1).drop(['Ranking Retorno Ultimos 5 Anos'], axis=1)

print("-------------------------------------")
print("Lista final de ações para investir: ")
print('-------------------------------------')
print(dffinal)

