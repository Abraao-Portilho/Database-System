# Módulo 1
Na escrita das funções iniciais (gravador e leitor) as maiores dificuldades foram: nos confundimos com os modos de abertura da função open, esquecemos do cabeçalho e registro de tamanho fixo no primeiro commit, mas a principal dificuldade foi preencher a páginas com bytes de valores nulo.

-Resposta do exercício: O registro foi parar no byte 8208 (ou no 17º byte da página 2)

-17/09/2026: maior desafio foi refatorar o que já haviamos feito e implementar todos os testes. 

# Módulo 2
-01/10/2026: foi criada a classe Cache que servirá para diminuir o número de acessos ao disco e consequentemente aumentar o desempenho do banco de dados. Foram testadas todas as funcionalidades. Sentimos dificuldade na implementação da classe, por isso usamos integralmente o esqueleto disponibilizado. O maior desafio foi a realização do teste de modificação dentro de um frame e teste do método solta quando sujou=true, pois englobou todos os conceitos desse módulo. Muitas dúvidas foram esclarecidas(adequações no pager com a exclusão do método sync de dentro de alguns métodos e início de uma visão mais concreta em relação ao projeto)

