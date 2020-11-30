import socket

from typing import List, Any
from config import IP, PORT, LISTEN_NUM, BUFFER_SIZE


class CMD():
    """
    command class
    """
    GET_ALL: str = 'GET_ALL'
    QUIT: str = 'QUIT'


class TCP_Server():
    """
    tcp server
    """
    def __init__(self):
        # IPv4/TCP
        self.tcp_server: socket = socket.socket(socket.AF_INET,
                                                socket.SOCK_STREAM)
        self.tcp_server.bind((IP, PORT))
        self.tcp_server.listen(LISTEN_NUM)

    def get_all(self, buffered_args: List) -> bytes:
        """
        get_all
        """
        print("GET_ALL: " + ' '.join(buffered_args))
        if not buffered_args:
            response = b"502 Bad Parameter"
        else:
            response = b"200 OK!"

        return response

    def process(self, cmd: CMD, buffered_args: List):
        """
        process
        """
        if cmd == CMD.GET_ALL:
            response = self.get_all(buffered_args)

        return response

    def __loop_and_wait(self, client, address):
        """
        loop and wait
        """
        wait_for_dot: bool = False
        cmd: CMD = None
        buffered_args: List = []

        while True:
            break_flag: bool = False
            response: bytes = b""
            input: bytes = client.recv(BUFFER_SIZE)

            if input == b"\xff\xf4\xff\xfd\x06":
                print("SIGTERM is received.")
                client.close()
                break

            data: bytes = input.strip(b'\r\n')
            print(b"[*] Received Data: " + data)

            if wait_for_dot:
                if data != b'.':
                    response = b"522 Bad Request!"
                    break_flag = True
                else:
                    wait_for_dot = False
                    break_flag = True

                    response = self.process(cmd, buffered_args)

            else:
                cmd, *buffered_args = data.decode('ascii').split(' ')

                if cmd == CMD.GET_ALL:
                    wait_for_dot = True
                    continue

                elif cmd == CMD.QUIT:
                    response = b"QUIT"
                    break_flag = True

                else:
                    response = b"command is invalid"

            client.send(response + b'\n')

            if break_flag:
                client.close()
                break

    def run(self):
        """
        run
        """
        client: socket = None
        address: Any

        while True:
            try:
                client, address = self.tcp_server.accept()
                print("[*] Connectioned from : {}".format(address))

                self.__loop_and_wait(client, address)
            except KeyboardInterrupt:
                if client is not None:
                    print("Keyboad Interrupt. socket will close.")
                    client.close()
                break


t = TCP_Server()
t.run()
