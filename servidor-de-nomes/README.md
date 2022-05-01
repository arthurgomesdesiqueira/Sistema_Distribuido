# Servidor de Nomes

Nesse trabalho implementamos um exemplo do DCE ou Distributed Computing Environment. Basicamente, no DCE temos um servidor diretório que tem a função de registrar o serviço, no caso o servidor. Nele são armazenados o nome do servidor, o host e a porta. Além dessa função, temos outra que é quando o cliente faz uma busca dentro do servidor diretório procurando o host e a porta de um certo servidor e a função do servidor diretório é servir o cliente com esse host e porta do servidor em questão. 


## Cliente

No código `client.py`, temos uma classe chamada `Cliente`, nele temos duas funções:

```
def getServerAddress(self, name):
    conn = rpyc.connect(const.DIRECTORY_SERVER_ADDRESS, const.DIRECTORY_SERVER_PORT)
    host, port = conn.root.query(name)
    return host, port
```

Nessa função, ela recebe como parâmetro o nome do servidor. O primeiro comando que essa função executa é buscar uma conexão no servidor diretório. Caso consiga uma conexão, ele vai para o próximo comando que é executar uma função que está dentro do servidor diretório chamado `query`, o cliente passa para o servidor diretório o nome do servidor que o cliente quer. Após a execução dessa função query, o servidor diretório retorna pro cliente o host e a porta desse servidor em questão. Depois de adquirir essas variáveis, ele retorna as duas.


```
def pingServer(self, host, port):
    conn = rpyc.connect(host, port)
    conn.root.ping()
    conn.root.ping()
    conn.root.ping()
    conn.root.ping()
```

Nessa função, ela recebe como parâmetro o host e o port do servidor que foi adquirido e tenta uma conexão com esse servidor. Caso consiga, ele chama uma função dentro do servidor chamado `ping`, que conta a quantidade de vezes que foi chamado essa função, ou seja, ele é como se fosse um contador.


Além da classe `Cliente`, temos a `main` onde será atribuida numa varíavel a classe `Cliente` e essa varíavel chama a função `getServerAddress` e `pingServer`, as quais foram explicadas anteriormente.


## Servidor

No código `server.py`, temos uma classe chamada `Servidor`, nele temos uma função:

```
def exposed_ping(self):
    print("Request Number:", self.count)
    self.count = self.count + 1
```

Nessa função, ela basicamente conta a quantidade de vezes que foi chamado essa função, ou seja, ele é como se fosse um contador. A variável que criar essa classe `Servidor`, começa com o `count = 0`.


Além da classe `Servidor`, temos a `main` onde será atribuida numa varíavel a classe `Servidor`que foi criada usando o `ThreadServer`, essa função recebe como paramêtro a classe e a porta. Em seguida, criamos uma conexão com o servidor diretório e executamos a função dentro dele que é `register`. Então o servidor passa para o servidor diretório o nome do servidor, a port e o host do servidor para registro. Após o servidor diretório registrar o servidor em questão, temos por último a execução do `start`, para executar o servidor.


## Servidor Diretório

No código `serverDiretorio.py`, temos uma classe chamada `DirectoryServer`, nele temos duas funções:

```
def exposed_register(self, name, host, port):
    print("Adicionado o servidor", name, "com endereco:", host, ":", port)
    self.ServerNames[name] = [host, port]
```

Nessa função, ela recebe como parâmetro o nome, o host e a port do servidor, para registrar a port e o host do servidor. Registramos esses valores numa varíavel dicionário com a chave sendo o nome do servidor e os valores como sendo o host e o port. 

```
def exposed_query(self, name):
    print(self.ServerNames)
    return self.ServerNames[name]
```

Nessa função, recebemos como parâmetro o nome do servidor, buscamos o nome do servidor e caso ache, retornamos o host e a port desse servidor em questão.


Além da classe `DirectoryServer`, temos a `main` onde será atribuida numa varíavel a classe `DirectoryServer` que foi criada usando o `ThreadServer`, essa função recebe como paramêtro a classe e a porta. Em seguida, ocorre a execução do `start`, para executar o servidor.
















