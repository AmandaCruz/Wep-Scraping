'''*********************************************************
Web Scraping para busca de CEP's. Python 3.8. 

O programa envia ao site do correios de busca de CEP uma busca escolhendo uma UF. A resposta do servidor então é tratada e a tabela com CEP é exportada em JSONL

Por: Amanda Alina da Cruz Silva, 2020.
*********************************************************'''

from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json
#É necessário instalar as bibliotecas acima

#Requisição HTLM no servidor
session = HTMLSession()

#lista contendo os estados para passar como parâmetros
estado = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']

i = 0 #contador para iterar a busca em cada estado
with open('CEPS.json', 'w') as outfile: #abertura de arquivo json
  while estado[i] in estado: #loop das buscas
    params = "UF="+ estado[i]
    header = {'Content-Type': 'application/x-www-form-urlencoded',
              'Origin': 'http://www.buscacep.correios.com.br',
              'Referer': 'http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCEP.cfm'}
    url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'
    
    #Requisição no site dando os parâmetros
    a = session.post(url, data=params, headers=header)
    
    #transforma em estrutura trabalhável o html
    soup = BeautifulSoup(a.text, 'lxml') 
    
    #encontra as tabelas
    table = soup.find_all('table',{"class":"tmptabela"}) 
    
    ba = {} #dicionário para conter as linhas da tabela
    for line in table[1].find_all('tr'): #encontra tag tr das linhas e mantem no loop enquanto houver linha
        count = 0 #contador para descartar as duas últimas colunas da tabela
        for l in line.findAll('td'): #encontra td, colunas da tabela
          ba['Estado'] = estado[i] #pega o estado e salva no dicionário para escrevê-lo a cada linha no arquivo jsonl
          if count==0:#coluna 1
            ba['Localidade'] = l.get_text() #pega texto da coluna 1 e salva no dic
            print (l.getText(),'|') #escreve texto na tela
          if count==1: #coluna 2
            ba['Faixa de CEP'] = l.get_text() #pega texto da coluna 2 e salva no dic
            print (l.getText(),'|') #escreve texto na tela
          if count == 3 :
             json.dump(ba, outfile, ensure_ascii=False) #escreve linha no arquivo json
             json.dump('\n', outfile, ensure_ascii=False)  #salta linha 
             count = 0 #zera o contador de coluna
          count = count + 1 #itera o contador de coluna
    
    i = i + 1 #itera o contador de estados
        
    if i == len(estado): # para o programa
      break;
