#!/usr/bin/env python
# coding: utf-8
#Implementação: [Python]

#Importações
import os.path
import os
import getopt, sys
import numpy as np

#Lista dos Argumentos
argumentList = sys.argv[1:]

#Opções
options = "d:t:c:m:n:i:r:h"
long_options = ["Disciplines=", "Times=", "Classrooms=", "MAXAlfa=", "MINAlfa=", "Increment=", "Relax=", "Help"]

#Argumentos
script_name = 'pas_resolution.py'
path_disciplines = ''
path_times = ''
path_classrooms = ''
min_alfa = 0
max_alfa = 1
incremento = 0.1
relax = False

try:
    #Importando argumentos
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-d", "--Disciplines"):
            path_disciplines = currentValue
        elif currentArgument in ("-t", "--Times"):
            path_times = currentValue
        elif currentArgument in ("-c", "--Classrooms"):
            path_classrooms = currentValue
        elif currentArgument in ("-m", "--MAXAlfa"):
            max_alfa = float(currentValue)
        elif currentArgument in ("-n", "--MINAlfa"):
            min_alfa = float(currentValue)
        elif currentArgument in ("-i", "--Increment"):
            incremento = float(currentValue)
        elif currentArgument in ("-r", "--Relax"):
            relax = currentValue
        elif currentArgument in ("-h", "--Help"):
            print('-d or --Disciplines : Comando necessários para especificar o arquivo das disciplinas.')
            print('-t or --Times : Comando necessários para especificar o arquivo dos horários.')
            print('-c or --Classrooms : Comando necessários para especificar o arquivo das salas.')
            print('-m or --MAXAlfa : Comando caso deseje especificar o valor max de alfa para o ciclo da função objetivo, tem como valor padrão 1.')
            print('-n or --MINAlfa : Comando caso deseje especificar o valor min de alfa para o ciclo da função objetivo, tem como valor padrão 0.')
            print('-i or --MINAlfa : Comando caso deseje especificar o valor do incremento de alfa no ciclo da função objetivo, tem como valor padrão 0.1')
            print('-r or --Relax : Comando caso deseje especificar se pode ser realizado o relaxamento das restrições do modelo, tem como valor padrão False.')
            sys.exit('Para executar digite novamente o comando sem a instrução -h ou --Help.')
except getopt.error as err:
    print(str(err))

#Iniciando Execução
print('Iniciando a execução do script Generation:')
if not os.path.isfile('./'+script_name):
    sys.exit('Arquivo do script de execução principal não encontrado.')

string_params = ''
if os.path.isfile(path_times):
    string_params += ' -t '
    string_params += '"' + path_times + '"'
else:
    sys.exit('Arquivo com os horários não encontrado!')

if os.path.isfile(path_classrooms):
    string_params += ' -c '
    string_params += '"' + path_classrooms + '"'
else:
    sys.exit('Arquivo com as salas não encontrado!')

if os.path.isfile(path_disciplines):
    string_params += ' -d '
    string_params += '"' + path_disciplines + '"' 
else:
    sys.exit('Arquivo com as disciplinas não encontrado!')

if relax:
    string_params += ' -r True'

for alfa in np.arange(min_alfa, max_alfa + incremento, incremento):
    params = string_params + ' -a ' + str(round(alfa,1))
    print('Parametros: %s' % params)
    os.system(script_name+params)