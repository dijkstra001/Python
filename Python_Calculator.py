# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 07:44:21 2020

@author: Nathã Correia
"""
import os
import sys
os.system('cls') or None
print("--------------------------------- Calculadora em Python --------------------------------- ")
nome_user = input('Por favor informe o seu nome: ')
opcao = int(input('\nOlá, '+ nome_user+'! Por favor, escolha uma das opções abaixo:\n(1) Adição\n(2) Subtração\n(3) Divisão\n(4) Multiplicação\n(5) Potência\n\nOpção: '))
while opcao == 1 or opcao == 2 or opcao == 3 or opcao == 4 or opcao == 5:
    if opcao == 1:
        prim_num = float(input('Informe o primeiro número: '))
        seg_num = float(input('Informe o segundo número: '))
        soma = prim_num + seg_num
        print(str(prim_num)+" + "+str(seg_num)+ " = " + str(soma))
        escolha = int(input('Deseja realizar mais alguma operação? [1] SIM  [2] NÃO: '))
        if escolha == 1:
        	os.system('cls') or None
        	opcao = int(input('\nOlá, '+ nome_user+'! Por favor, escolha uma das opções abaixo:\n(1) Adição\n(2) Subtração\n(3) Divisão\n(4) Multiplicação\n(5) Potência\n\nOpção: '))
        else:
        	sys.exit()
    elif opcao == 2:
        prim_num = float(input('Informe o primeiro número: '))
        seg_num = float(input('Informe o segundo número: '))
        subtracao = prim_num - seg_num
        print(str(prim_num)+" - "+str(seg_num)+ " = " + str(subtracao)) 
        escolha = int(input('Deseja realizar mais alguma operação? [1] SIM  [2] NÃO: '))
        if escolha == 1:
        	os.system('cls') or None
        	opcao = int(input('\nOlá, '+ nome_user+'! Por favor, escolha uma das opções abaixo:\n(1) Adição\n(2) Subtração\n(3) Divisão\n(4) Multiplicação\n(5) Potência\n\nOpção: '))
        else:
        	sys.exit()
    elif opcao == 3:
        prim_num = float(input('Informe o primeiro número: '))
        seg_num = float(input('Informe o segundo número: '))
        divisao = round((prim_num / seg_num),3)
        print(str(prim_num)+" / "+str(seg_num)+ " = " + str(divisao))
        escolha = int(input('Deseja realizar mais alguma operação? [1] SIM  [2] NÃO: '))
        if escolha == 1:
        	os.system('cls') or None
        	opcao = int(input('\nOlá, '+ nome_user+'! Por favor, escolha uma das opções abaixo:\n(1) Adição\n(2) Subtração\n(3) Divisão\n(4) Multiplicação\n(5) Potência\n\nOpção: '))
        else:
        	sys.exit()
    elif opcao == 4:
        prim_num = float(input('Informe o primeiro número: '))
        seg_num = float(input('Informe o segundo número: '))
        multiplicacao = round((prim_num * seg_num),3)
        print(str(prim_num)+" * "+str(seg_num)+ " = " + str(multiplicacao))
        escolha = int(input('Deseja realizar mais alguma operação? [1] SIM  [2] NÃO: '))
        if escolha == 1:
        	os.system('cls') or None
        	opcao = int(input('\nOlá, '+ nome_user+'! Por favor, escolha uma das opções abaixo:\n(1) Adição\n(2) Subtração\n(3) Divisão\n(4) Multiplicação\n(5) Potência\n\nOpção: '))
        else:
        	sys.exit()
    elif opcao == 5:
        prim_num = float(input('Informe o primeiro número: '))
        seg_num = float(input('Informe o segundo número: '))
        potencia = prim_num ** seg_num
        print(str(prim_num)+" ^ "+str(seg_num)+ " = " + str(potencia))
        escolha = int(input('Deseja realizar mais alguma operação? [1] SIM  [2] NÃO: '))
        if escolha == 1:
        	os.system('cls') or None
        	opcao = int(input('\nOlá, '+ nome_user+'! Por favor, escolha uma das opções abaixo:\n(1) Adição\n(2) Subtração\n(3) Divisão\n(4) Multiplicação\n(5) Potência\n\nOpção: '))
        else:
        	sys.exit() 
else:
	os.system('cls') or None
	print("Opção inválida!\n\n")
	resposta = int(input('Deseja refazer a operação? [1] SIM [2] NÃO: '))
	if resposta ==1:
		os.system('cls') or None
		import Python_Calculator
	else:
		sys.exit()
    
