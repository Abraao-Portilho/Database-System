from cache import Cache
from service_pager import Pager
import os
import hexdump

arquivo_db = "bancobanco.db"
if os.path.exists(arquivo_db):
    os.remove(arquivo_db)

arquivo = Pager(arquivo_db)
arquivo.aloca(1)
arquivo.escreve(1,"A"*4096)
arquivo.aloca(5)
arquivo.escreve(5,"K"*4096)
arquivo.escreve(6,"g"*4096)
arquivo.fecha()

cache_test = Cache(arquivo ,10)
cache_test.fixa(1)
cache_test.fixa(5)


print(cache_test.frames)




