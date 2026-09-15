# MiniDB - Teste da Página 2
Cada página do arquivo possui exatamente 4096 bytes.
Os bytes que não possuem dados são preenchidos com byte de
valor nulo (0x00).
O cabeçalho da página possui 16 bytes e cada registro possui 8 bytes.
Foi gravado o registro:

JOAO1234

no slot 0 da página 2.
A página 2 começa no byte:
2 × 4096 = 8192
Como o cabeçalho possui 16 bytes:
8192 + 16 = 8208
Portanto, o registro começa no byte 8208.
Como o registro possui 8 bytes, ele ocupa os bytes:
8208 até 8215.

Os bytes restantes da página permanecem preenchidos com byte de
valor nulo (0x00), até completar os 4096 bytes da página.

Depois de encerrar o processo e executar novamente o arquivo ler.py,
o registro JOAO1234 foi recuperado corretamente.
