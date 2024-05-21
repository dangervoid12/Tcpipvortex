from tcpipvortex import tcpipvortex

# Configuration
version = "0.5"
LISTEN_HOST = '127.0.0.1'  # MITM machine IP
LISTEN_PORT = 50001       # Port to listen on (MITM port)
SERVER_HOST = '127.0.0.1'  # Target server IP or domain
SERVER_PORT = 50000         # Target server port

def display_info():
    print("TCPIPvortex")
    print(version)
    print("20240521")
    print("lpkkk")
    print("###################################################################################")
    print("####                                                                           ####")
    print("####     This program work as a tcpip simple window manager                    ####")
    print("####                 for Windows operating systems                             ####")
    print("####                                                                           ####")
    print("####                 by Lpkkk                                                  ####")
    print("####                                                                           ####")
    print("###################################################################################")
    print("Init...")


if __name__ == '__main__':
    display_info()
    app = tcpipvortex()
    app.start_mitm(LISTEN_HOST, LISTEN_PORT, SERVER_HOST, SERVER_PORT)
