import socket

from controllers.get_all_controller import Get_all
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

    def process(self, cmd: CMD, buffered_args: List):
        """
        process
        """
        if cmd == CMD.GET_ALL:
            get_all = Get_all(buffered_args)
            response = get_all.execute()

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
                    response = b"522 Bad Request."
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
                    response = b"Command is invalid."

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


if __name__ == "__main__":
    t = TCP_Server()
    t.run()
