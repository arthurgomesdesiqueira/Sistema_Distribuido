import rpyc
import const

# Classe simples de cliente.
# getServerAddress retorna o host e porta de um servidor com nome=name
# pingServer conecta a um servidor com os host e port passados por parametros e faz ping no servidor.
class Cliente:
    def getServerAddress(self, name):
        conn = rpyc.connect(const.DIRECTORY_SERVER_ADDRESS, const.DIRECTORY_SERVER_PORT)
        host, port = conn.root.query(name)
        return host, port

    def pingServer(self, host, port):
        conn = rpyc.connect(host, port)
        conn.root.ping()
        conn.root.ping()
        conn.root.ping()
        conn.root.ping()

if __name__ == "__main__":
    cliente = Cliente()
    host, port = cliente.getServerAddress(const.SERVER_NAME)
    cliente.pingServer(host, port)