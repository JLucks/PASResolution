#!/usr/bin/env python
# coding: utf-8
#Implementação: [Python]

#Importação dos módulos do Gurobi e outros necessários para a aplicação.

import gurobipy as gp
from gurobipy import GRB
import csv
from csv import writer 
from IPython.display import HTML, display
import pandas as pd 
import numpy as np
import os.path


#Importação dos arquivos de entrada
filename_times = open('./Input/Horarios.csv', encoding="utf8")
file_times = csv.DictReader(filename_times)
filename_classrooms = open('./Input/Salas.csv', encoding="utf8")
file_classrooms = csv.DictReader(filename_classrooms)
filename_disciplines = open('./Input/Disciplinas.csv', encoding="utf8")
file_disciplines = csv.DictReader(filename_disciplines)

#Definição dos parâmetros
#Times (T: conjunto de horários): T[cod, disciplinas]
Times = []
for col in file_times:
    t = []
    t.append(col['CodName'])
    t.append([])
    t.append(col['Horarios'])
    t.append(col['Dia'])
    Times.append(t)

#Rooms (S: conjunto de salas): S[cod, capacidade, laboratorio, andar]
Rooms = []
for col in file_classrooms:
    r = []
    r.append(col['CodName'])
    r.append(int(col['Capacidade']))
    r.append(col['Laborotario'] == 'TRUE')
    r.append(int(col['Andar']))
    r.append(col['Sala'])
    r.append(col['Bloco'])
    r.append(col['Predio'])
    Rooms.append(r)

#Disciplines (D: conjunto de disciplinas): D[cod, exigeLAB, existePCD, horarios, qntAlunos, horario]
Disciplines = []
for col in file_disciplines:
    d = []
    d.append(col['CodName'])
    d.append(col['Laboratorio'] == 'TRUE')
    d.append(col['PCD'] == 'TRUE')
    d.append(col['CodHorario'].split("-"))
    d.append(int(col['Alunos']))
    d.append(col['Horario'])
    d.append(col['Codigo'])
    d.append(col['Nome'])
    d.append(col['Professor'])
    Disciplines.append(d)

#Alocando as Disciplinas aos horários
for t in Times:
    for d in Disciplines:
        for h in d[3]:
            if t[0] == h:
                t[1].append(d[0])

#Função que verifica a possibilidade da disciplina na sala por capacidade ou infra-estrutura
def check_room(room, discipline):
    if room[1] >= discipline[4]:
        if discipline[1]:
            if room[2]:
                return True
        else:
            if not room[2]:
                return True
    return False            

#C (c_jk: Parâmetro recebe valor 1 se a disciplina j pode ser lecionada na sala k, e 0 caso contrário)
C = []
i = 0
for d in Disciplines:
    C.append([])
    for r in Rooms:
        if check_room(r,d):
            C[i].append(1)
        else:
            C[i].append(0)
    i += 1

#Dicionarios para exibição do resultado
dic_times = {}
for t in Times:
    data = []
    data.append(t[2])
    data.append(t[3])
    dic_times[t[0]] = data
dic_rooms = {}
for r in Rooms:
    data = []
    data.append(r[4])
    data.append(r[5])
    data.append(r[6])
    dic_rooms[r[0]] = data
dic_disciplines = {}
for d in Disciplines:
    data = []
    data.append(d[6])
    data.append(d[7])
    data.append(d[8])
    dic_disciplines[d[0]] = data

#Função que retorna um array de resultado pronto para exibição
def transform_result(result):
    new_result = []
    for row in result:
        r = []
        r.append(dic_disciplines[row[0]][0])
        r.append(dic_disciplines[row[0]][1])
        r.append(dic_disciplines[row[0]][2])
        r.append(dic_times[row[1]][1])
        r.append(dic_times[row[1]][0])
        r.append(dic_rooms[row[2]][0])
        r.append(dic_rooms[row[2]][1])
        r.append(dic_rooms[row[2]][2])
        new_result.append(r)
    return new_result

# Função que transforma o array para uma tabela visual.
def display_table(header, data):
    html = "<table>"
    if header:
        html += "<tr>"
        for head in header:
             html += "<th><h4>%s</h4></th>"%(head)
        html += "</tr>"
    for row in data:
        html += "<tr>"
        for field in row:
            html += "<td><h4>%s</h4></td>"%(field)
        html += "</tr>"
    html += "</table>"
    display(HTML(html))

#Definição do modelo
model = gp.Model("Problema Alocação Salas")

#Definição dos dicionários
#Salas
S = {}
for s in Rooms:
    S[s[0]] = s[1]

#Disciplinas
D = {}
for d in Disciplines:
    D[d[0]] = len(d[3])

#Horários
T = {}
for t in Times:
    if t[1]:
        T[t[0]] = t[1]

#Combinação das Disciplinas, Horários e Salas permitidas
DTS = []
i = 0
for d in Disciplines:
    j = 0
    for r in Rooms:
        if C[i][j] == 1:
            for t in d[3]:
                DTS.append((d[0],t,r[0]))
        j += 1
    i += 1

#Salas Ocupadas
Y = []
i = 0
for r in Rooms:
    for c in C:
        if c[i] == 1:
            Y.append(r[0])
            break
    i += 1

#PCD (PCD{0,1}: indica se a disciplina d possui (1) ou não (0) uma pessoa com necessidade especial matriculada nela)
PDC = {}
for d in Disciplines:
    if d[2]:
        PDC[d[0]] = 1
    else:
        PDC[d[0]] = 0

#Andar (Andar S : indica o andar da sala utilizada (1,2,3…))
Floors = {}
for r in Rooms:
    Floors[r[0]] = int(r[3])

#Definição das variáveis
salas, andar = gp.multidict(Floors)
disciplinas, ocupacao = gp.multidict(D)
horarios, horariosOcupados = gp.multidict(T)
portadores, pcd = gp.multidict(PDC)
disponibilidade = gp.tuplelist(DTS)

#x (x[d,t,s] = 1 se a disciplina d é alocada na sala s no horário t e 0 caso contrario)
x = model.addVars(disponibilidade, ub = 1, name = "x")

#y (y[s]: recebe valor 1 se a sala s será utilizada, e 0 caso contrário)
y = model.addVars(Y, ub = 1, name = "y")

#Restrições
#Restrições que garantem que cada disciplina é lecionada exatamente o número de vezes no horizonte de planejamento (por ex. 2 vezes em uma semana de 5 dias)
res1 = model.addConstrs(x.sum(d, '*', '*') == ocupacao[d] for d in disciplinas)

#Restrições que garantem que duas disciplinas não são lecionadas na mesma sala de aula, dia e horário.
res2 = model.addConstrs(x.sum('*', t, s) <= 1 for d, t, s in disponibilidade)

#Restrições que  garantem a elegibilidade das aulas, isto é, garantem que uma disciplina não seja atribuída a salas diferentes no mesmo horário.
res3 = model.addConstrs(x.sum(d, t, '*') <= 1 for d, t, s in disponibilidade)

#Restrições que definem que se alguma disciplina é atribuída para alguma sala s e horário t, então a sala s será utilizada, essa restrição se faz necessária para minimização de salas utilizadas na função objetivo
res4 = model.addConstrs(x[d , t, s] <= y[s] for d, t, s in disponibilidade)

#Função Objetivo
#A função objetivo minimiza duas parcelas. A primeira corresponde ao número de salas utilizadas, e a segunda se trata de uma penalidade em casos em que há PCD na disciplina d e a sala não se localiza no térreo (andar=0). Além disso, quanto maior o andar, maior a penalidade.
a = 1
obj1 = (1 - a) * gp.quicksum(y[s] for d, t, s in disponibilidade)
obj2 = a * gp.quicksum(x[d,t,s] * andar[s] * pcd[d] for d, t, s in disponibilidade)
model.setObjective(obj1 + obj2, GRB.MINIMIZE)
#A f.o. também possui um coeficiente de ponderação , que permite priorizar ou a minimização simplesmente o número de salas utilizadas ou minimizar o número de disciplinas com PCD que não são alocadas em salas do térreo.

#Execução
model.optimize()

#Status
status = model.status
if status == GRB.UNBOUNDED:
    print('The model cannot be solved because it is unbounded')
if status == GRB.OPTIMAL:
    print ('The optimal objective is %g' % model.objVal)
if status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
    print ('Optimization was stopped with status %d' % status )

#Relaxando restrições
print('The model is infeasible; relaxing the constraints')
orignumvars = model.NumVars
model.feasRelaxS(0, True , False , True)
model.optimize()

#Status após relaxamento
status = model.status
if status in (GRB.INF_OR_UNBD , GRB.INFEASIBLE , GRB.UNBOUNDED ):
    print ('The relaxed model cannot be solved because it is infeasible or unbounded')
if status != GRB.OPTIMAL :
    print ('Optimization was stopped with status %d' % status)
print ('Slack values :')
slacks = model.getVars()[orignumvars:]
for sv in slacks:
    if sv.X > 1e-6:
        print('%s = %g' % (sv.VarName , sv.X))

#Resultados
print('Variables values:')
result = []
for v in model.getVars():
        print('%s : %g' % (v.VarName, v.X))
        if 'x[' in v.VarName and v.X == 1:
            result.append(v.VarName.replace('x[','').replace(']','').split(','))

#Representação do resultado
print(result)
head_obj = ['Alfa','FO']
obj_res = []
obj_res.append(float(a))
obj_res.append(model.objVal)
table_obj = []
table_obj.append(obj_res)
head_result = ['Código', 'Disciplina','Professor','Dia','Horário','Sala','Bloco','Predio']
table_result = transform_result(result)
print('Tabela de Resultado')
if a >= 0.5:
    print('Priorizando o número de disciplinas com PCD')
else:
    print('Priorizando o número de salas utilizadas')
display_table(head_obj,table_obj)
display_table(head_result,table_result)

#Exportando resultado
arr_result = np.asarray(table_result)
filename_result = 'result'
if a >= 0.5:
    filename_result += '_priori_pcd'
else:
    filename_result += '_priori_num_salas'
i = ''
output_result = './Output/'+filename_result 
while os.path.isfile(output_result+ (' ('+str(i)+')' if i != '' else i )  +'.csv'):
    if i == '':
        i = 0
    i += 1
output_result += ' ('+str(i)+')' if i != '' else i 
pd.DataFrame(arr_result).to_csv(output_result+'.csv', header = head_result, index = False, sep = ';') 

output_obj = './Output/fos_result.csv'
if os.path.isfile(output_obj):
    with open(output_obj, 'a') as f_object: 
        writer_object = writer(f_object, delimiter = ';')     
        writer_object.writerow(obj_res) 
        f_object.close() 
else:
    arr_obj = np.asarray(table_obj)
    pd.DataFrame(arr_obj).to_csv(output_obj, header = head_obj, index = False, sep = ';') 

