import socket
import threading
from SimpleWindowMgr import SimpleWindowMgr

class tcpipvortex:
    win_mgr = None
    last_msg = ""
    cur_msg = ""

    def handle_client(self, client_socket, remote_host, remote_port):

        # Connect to the remote host
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((remote_host, remote_port))

        # Start two threads to forward traffic in both directions
        client_to_server = threading.Thread(target=self.forward, args=(client_socket, server_socket))
        server_to_client = threading.Thread(target=self.forward, args=(server_socket, client_socket))

        client_to_server.start()
        server_to_client.start()

        client_to_server.join()
        server_to_client.join()

        client_socket.close()
        server_socket.close()

    def forward(self, source, destination):
        while True:
            data = source.recv(4096)
            if len(data) == 0:
                break
            self.handle_data(data)
            print(f"Forwarding data: {data}")
            destination.send(data)

    def handle_data(self, data):
        self.cur_msg = data
        if data == b'PFOptiscout.cnc;':
            self.win_mgr.minimize_startswith_name("OptiScout")
        print("Received data: " + str(data))

    def handle_two_data(self, data):
        self.last_msg = self.cur_msg
        self.cur_msg = data
        if self.cur_msg == b'1':
            if self.last_msg == "PFOptiscout.cnc;":
                self.win_mgr.minimize_startswith_name("OptiScout")
                self.win_mgr.maximize_startswith_name("KvIsoGui")
            print("receive 1 and last was: " + self.last_msg)

    def start_mitm(self, listen_host, listen_port, remote_host, remote_port):
        self.win_mgr = SimpleWindowMgr()
        # Set up listening socket
        mitm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mitm_socket.bind((listen_host, listen_port))
        mitm_socket.listen(5)
        print(f"Listening on {listen_host}:{listen_port}")

        while True:
            client_socket, addr = mitm_socket.accept()
            print(f"Accepted connection from {addr}")
            handle_thread = threading.Thread(target=self.handle_client, args=(client_socket, remote_host, remote_port))
            handle_thread.start()
