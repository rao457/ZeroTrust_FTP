from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from config import USERNAME, PASSWORD, PORT

connect_clients = {}
ftp_server_instance = None

class MyHandler(FTPHandler):
    def on_connect(self):
        connect_clients[self.remote_ip] = self
        print(f"Connected: {self.remote_ip}")
        
    def on_disconnect(self):
        connect_clients.pop(self.remote_ip, None)
    
    def close_connection(self):
        self.close_when_done()


def START_SERVER():
    authorizer = DummyAuthorizer()
    authorizer.add_user(USERNAME, PASSWORD, ".", perm="elradfmw")
    handler = MyHandler
    handler.authorizer = authorizer
    ftp_server_instance = FTPServer(("0.0.0.0", PORT), handler)
    ftp_server_instance.serve_forever()
def stop_server():
    global ftp_server_instance
    if ftp_server_instance:
        ftp_server_instance.close_all()