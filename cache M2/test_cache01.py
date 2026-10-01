from cache import Cache
from service_pager import Pager
import os

arquivo_db = "bancobanco1.db"
if os.path.exists(arquivo_db):
    os.remove(arquivo_db)

arquivo = Pager(arquivo_db)
arquivo.escreve(1,"A"*4096)
arquivo.escreve(5,"K"*4096)
arquivo.escreve(6,"g"*4096)
arquivo.escreve(9,"j"*4096)
arquivo.escreve(8,"p"*4096)
arquivo.escreve(2,"y"*4096)
arquivo.fecha()

#teste de expulsão de uma cache com capacidade de 5 páginas
cache_test = Cache(arquivo ,5)
cache_test.fixa(1)
cache_test.fixa(5)
cache_test.fixa(6)
cache_test.fixa(9)
cache_test.fixa(8)
cache_test.solta(5)
cache_test.solta(1)
cache_test.solta(6)
cache_test._expulsa()


print("É esperado que a página 1 seja expulsa, pois foi a primeira a entrar e não foi usada novamente")
print(cache_test.uso)
print(cache_test.fixada)

#teste de adequação dos frames ao conteúdo das páginas
print("\n",cache_test.frames[5] == arquivo.le(5))

