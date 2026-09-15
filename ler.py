from service import leitor
arquivo = "teste.txt"
tamanho_pagina = 4096
cabecalho = 16
tamanho_registro = 8

pagina = leitor(arquivo, 2)

posicao = cabecalho

registro = pagina[posicao:posicao + tamanho_registro]
print("Registro lido:")
print(registro.decode())
