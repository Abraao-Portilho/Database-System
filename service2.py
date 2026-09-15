import os
def gravador(local_arquivo, page_id, slot_id, dados: bytes):
    tamanho_pag = 4096
    tamanho_cabecalho = 16
    tamanho_registro = 8

    if len(dados) > tamanho_registro:
        print("Tamanho dos dados excede o tamanho máximo de um registro")
        return

    tamanho_necessario = tamanho_pag * (page_id + 1)

    if not os.path.exists(local_arquivo):

        with open(local_arquivo, "wb") as arquivo:
            arquivo.write(b"\x00" * tamanho_necessario)
    else:

        tamanho_atual = os.path.getsize(local_arquivo)
        if tamanho_atual < tamanho_necessario:
            with open(local_arquivo, "ab") as arquivo:
                arquivo.write(b"\x00" * (tamanho_necessario - tamanho_atual))

    inicio_gravacao = (
        tamanho_pag * page_id
        + tamanho_cabecalho
        + tamanho_registro * slot_id
    )
    dados_slot = dados + b"\x00" * (tamanho_registro - len(dados))

    with open(local_arquivo, "r+b") as arquivo:
        arquivo.seek(inicio_gravacao)
        arquivo.write(dados_slot)
def leitor(local_arquivo, page_id):
    tamanho_pag = 4096
    with open(local_arquivo, "rb") as arquivo:
        inicio_leitura = tamanho_pag * page_id
        arquivo.seek(inicio_leitura)
        dados_pagina = arquivo.read(tamanho_pag)

        return dados_pagina
