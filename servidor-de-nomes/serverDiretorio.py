import rpyc
import const
from rpyc.utils.server import ThreadedServer

# Classe simples que registra host e porta a um nome especifico quando chamamos exposed_register
# O cliente chama exposed_query para obter o host e porta de um nome especifico.
class DirectoryServer(rpyc.Service):
    ServerNames = {}

    def exposed_register(self, name, host, port):
        print("Adicionado o servidor", name, "com endereco:", host, ":", port)
        self.ServerNames[name] = [host, port]

    def exposed_query(self, name):
        print(self.ServerNames)
        return self.ServerNames[name]


if __name__ == "__main__":
    # Inicializacao simples do diretorio.
    server = ThreadedServer(DirectoryServer(), port = const.DIRECTORY_SERVER_PORT)
    server.start()