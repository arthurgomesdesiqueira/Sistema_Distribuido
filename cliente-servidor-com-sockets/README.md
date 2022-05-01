# ClientServerBasics
Neste repositorio temos um exemplo de servidor e cliente. O servidor e uma calculadora remota que realiza quatro tipo de operacoes, como as seguintes:

add -> Adiciona dois numeros.
subtract -> Subtrai do primeiro numero o valor do segundo.
multiply -> Multiplica dois numeros.
divide -> Divide o primeiro numero pelo segundo.

Todas as operacoes resultam em um numero real, aceitam numeros reais, e sao case-insensitive. (Add, aDd, aDD sao a mesma operacao add).

O servidor se desliga depois de uma operacao do cliente e tambem consegue lidar com erros internamente. Caso o numero passado seja invalido ou a operacao seja invalida, o servidor ira reportar o erro.