import rpyc
import const
from rpyc.utils.server import ThreadedServer

SERVER_ADDRESS = "localhost"
SERVER_PORT = 1234

# Servidor simples que recebe um ping e incrementa count toda vez que é chamado.
class Server(rpyc.Service):
    count = 0

    def exposed_ping(self):
        print("Request Number:", self.count)
        self.count = self.count + 1

if __name__ == "__main__":
    # Em vez de chamar Server, chamo Server(). O motivo é que na documentacao https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html
    # Diz que se não passar assim, toda conexão vai ter a sua própria instância do servidor
    # Usando assim, a mesma instância será utilizada por todas as conexões e permite incrementar a váriavel count sempre.
    # Estranhamente, o servidor de diretorios não precisa disso.
    server = ThreadedServer(Server(), port = SERVER_PORT)

    # Conectando ao servidor de diretorio e adicionando o host e a porta ao nome.
    conn = rpyc.connect(const.DIRECTORY_SERVER_ADDRESS, const.DIRECTORY_SERVER_PORT)
    conn.root.register(const.SERVER_NAME, SERVER_ADDRESS, SERVER_PORT)

    # Inicializando o Servidor
    server.start()