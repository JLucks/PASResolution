# PAS: Resolution
PROBLEMA DE ALOCAÇÃO DE SALAS: MODELAGEM E APLICAÇÃO NA UFMA

Projeto para Monografia apresentada ao curso de Ciência da Computação da Universidade Federal do Maranhão, para aprovação no componente curricular Monografia II. 

Author: Jorge Lucas Silva Cavalcante

Orientador(a): Prof. Francisco Glaubos Nunes Clímaco

Desenvolvido no Jupyter-Notebook e em Python 3.8

Requer licença do Solver Gurobi

O arquivo pas_resolution.ipynb requer o jupyter-notebook para ser executado

O arquivo pas_resolution.py pode ser executa com a chamada ao Python 3.8 com os argumentos:

-d or --Disciplines : Comando necessários para especificar o arquivo das disciplinas.

-t or --Times : Comando necessários para especificar o arquivo dos horários.

-c or --Classrooms : Comando necessários para especificar o arquivo das salas.

-a or --Alfa : Comando caso deseje especificar o valor de alfa para a função objetivo, tem como valor padrão 1.

-r or --Relax : Comando caso deseje especificar se pode ser realizado o relaxamento das restrições do modelo, tem como valor padrão False.

-h ou --Help : Comando que exibe menu de opções

O arquivo analise_generation.py serve para execução em massa de um intervalo de alfa (coeficiente de ponderação) requer o arquivo pas_resolution.py e pode ser executa com a chamada ao Python 3.8 com os mesmos argumentos do arquivo pas_resolution.py com a troca do -a ou -Alfa pela definição de intervalo:

-m or --MAXAlfa : Comando caso deseje especificar o valor max de alfa para o ciclo da função objetivo, tem como valor padrão 1.

-n or --MINAlfa : Comando caso deseje especificar o valor min de alfa para o ciclo da função objetivo, tem como valor padrão 0.
