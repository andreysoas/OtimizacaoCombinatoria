# -*- coding: utf-8 -*-
"""FSP via HP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oWYDlqzrxJ-MxFRBx_STJxzo4LczRw9e
"""

import numpy as np
from math import floor
import math
import functools
import itertools

def convert_arq(path:str)->list:
  matriz = []
  ant =''
  with open(path,'r') as arqv:
    num=0
    for i in arqv:
      line = []
      for j in i:
        if (j=='\n' or j==' ') and ant!=' ':
          ant = j
          line.append(num)
          num=0
        elif '0'<=j<='9':
          ant = j
          num = num*10 + int(j)
      matriz.append(line)
  arqv.close()

  Matriz = []

  for i in matriz:
    new_lines = []
    for j in range(0,len(i)):
      if j%2 != 0:
        new_lines.append(i[j])
    Matriz.append(new_lines)

  return Matriz

def subviz(s):
  a=[]
  scopy2=np.array(s)
  a.append(scopy2)
  for i in range(1,len(s)-1):
    for j in range(i+1,len(s)):
      s[i],s[j]=s[j],s[i]
      a.append(s)
      s=np.copy(scopy2)
  return a

def espelhado(s):
  k = floor(len(s)/2)
  for i in range(1,k+1):
    s[i],s[len(s)-i] = s[len(s)-i],s[i]
    
def trocas(s):
  for i in range(1,len(s)-1,2):
    s[i],s[i+1]=s[i+1],s[i]


def HP(s):
  permutacoes=[]
  scopy = np.array(s)
  for i in range(0,len(s)):
    s=np.copy(scopy)
    s[0],s[i]=s[i],s[0]
    scopy2=np.copy(s)

    #Gerar as trocas dois a dois 
    permutacoes+=subviz(s)
    s=np.copy(scopy2)
    
    espelhado(s)
    permutacoes+=subviz(s)
    s=np.copy(scopy2)
    
    trocas(s)
    scopy3=np.copy(s)
    permutacoes+=subviz(s)
    s=np.copy(scopy3)

    espelhado(s)
    permutacoes+=subviz(s)
  
  return permutacoes

def makesPan(seq:list,M):
  m = len(M)
  antSeq = np.zeros(m)
  newSeq = np.zeros(m)

  for j in seq: # j = 1,2,3,4 ...
    for i in range(m):

      if i == 0:
        newSeq[0] = antSeq[0] + M[i][j-1]

      else:
        if newSeq[i-1] > antSeq[i]:
          newSeq[i] = newSeq[i-1] + M[i][j-1]
        else:
          newSeq[i] = antSeq[i] + M[i][j-1]
    
    antSeq = newSeq
    #print(antSeq)

  return antSeq[-1]

def defineOtimo(S:list,M:list):
  listMakespans = []
  min = 0

  for i in range(len(S)):
    atual = makesPan(S[i],M)
    solucao = list(S[i])

    if i == 0:
      min = atual
      listMakespans.append(solucao)
    
    else:
      if atual < min:
        listMakespans.clear()
        listMakespans.append(solucao)
        min = atual
      
      elif atual == min:
        if solucao not in listMakespans:
          listMakespans.append(solucao)

  print('\nSolução: ',listMakespans,end='\n')
  print('Mínimo: ',min)

def interfaceProgram():
  path = input('Path: ')
  if path == 'end':
    return True

  M = np.array(convert_arq(path))
  M = M.transpose()
  print("Matriz(tempo na máquina / tarefa): ")
  for i in M:
    print(i,end='\n')

  tarefas = list(np.arange(1,len(M[0])+1))
  print("Tarefas: ",tarefas)

  lista = HP(tarefas)
  print('quantidade de soluções: ',len(lista))

  defineOtimo(lista,M)
  print('\n')

while True:
  if interfaceProgram():
    print('\nTERMINANDO...',end='\n')
    break