from service import gravador
arquivo = "teste.txt"
tamanho_pagina = 4096
cabecalho = 16
tamanho_registro = 8

with open(arquivo, "wb") as f:
    f.write(b"\x00" * (tamanho_pagina * 3))

registro = b"JOAO1234"

gravador(arquivo, 2, 0, registro)

inicio_pagina = tamanho_pagina * 2
byte_registro = inicio_pagina + cabecalho

print("Registro gravado com sucesso!")
print("Página:", 2)
print("Slot:", 0)
print("Registro:", registro.decode())
print("Tamanho da página:", tamanho_pagina, "bytes")
print("Registro começa no byte:", byte_registro)
print(
    "Registro ocupa os bytes:",
    byte_registro,
    "até",
    byte_registro + tamanho_registro - 1
)
