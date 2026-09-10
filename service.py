def gravador(local_arquivo, page_id, dados):
    tamanho_pag = 4096
    with open(local_arquivo , "w+b") as arquivo:
        inicio_gravacao = tamanho_pag * page_id
        arquivo.seek(inicio_gravacao)
        bytes = dados.encode("utf-8")
        arquivo.write(bytes)
                   
def leitor(local_arquivo , page_id):
    tamanho_pag = 4096
    with open(local_arquivo , "rb") as arquivo:
        inicio_leitura = tamanho_pag * page_id
        arquivo.seek(inicio_leitura) #seek serve para indicar onde será o inicio da leitura

        dados_pagina = arquivo.read(tamanho_pag)
        dados_em_int = int.from_bytes(dados_pagina)
        return dados_em_int





