#teste de modificação dentro de um frame e teste do método solta quando sujou=true
from cache import Cache
from service_pager import Pager
import os

arquivo_db = "bancobanco2.db"
if os.path.exists(arquivo_db):
    os.remove(arquivo_db)

arquivo = Pager(arquivo_db)
arquivo.escreve(1,"A"*4096)
arquivo.escreve(5,"K"*4096)
arquivo.escreve(6,"g"*4096)
arquivo.escreve(9,"j"*4096)
arquivo.fecha()

cache_test = Cache(arquivo ,2)
cache_test.fixa(1)


print("páginas fixadas inicialmente: ",cache_test.uso)
print("páginas sujas inicialmente: ",cache_test.suja)
dados = (b"X" * 4096)
cache_test.frames[1] = dados
cache_test.solta(1, sujou=True)

print("\npáginas fixadas depois do método solta com parametro sujou=true: ",cache_test.uso)
print("páginas sujas atualmente: ",cache_test.suja)

cache_test.fixa(5)
cache_test.fixa(6)
print("\npáginas sendo usadas: ",cache_test.uso) #página 1 foi expulsa
print("páginas sujas atualmente: ", cache_test.suja)
print("A página 1 não está mais em memória, portanto foi gravada no disco")