import socket

from config import IP, PORT, LISTEN_NUM, BUFFER_SIZE


class CMD():
    """
    command class
    """
    GET_ALL: bytes = b'GET_ALL\r\n'
    QUIT: bytes = b'QUIT\r\n'


class TCP_Server():
    """
    tcp server
    """

    def __init__(self):
        # IPv4/TCP
        self.tcp_server: socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
            )
        self.tcp_server.bind((IP, PORT))
        self.tcp_server.listen(LISTEN_NUM)

    def __loop_and_wait(self, client, address):
        """
        loop and wait
        """
        while True:
            break_flag: bool = False
            response: bytes = b""
            data: bytes = client.recv(BUFFER_SIZE)

            if data == b"\xff\xf4\xff\xfd\x06":
                print("SIGTERM is received.")
                client.close()
                break

            print(b"[*] Received Data: " + data)

            print(CMD.GET_ALL)
            if data == CMD.GET_ALL:
                response = b"200 OK!\n"
                break_flag = True
            elif data == CMD.QUIT:
                response = b"QUIT\n"
                break_flag = True

            client.send(response)

            if break_flag:
                client.close()
                break

    def run(self):
        """
        run
        """
        try:
            while True:
                client, address = self.tcp_server.accept()
                print("[*] Connectioned from : {}".format(address))

                try:
                    self.__loop_and_wait(client, address)
                except KeyboardInterrupt:
                    print("Keyboad Interrupt. socket will close.")
                    client.close()
                    break
        except Exception as e:
            print(e)


t = TCP_Server()
t.run()
