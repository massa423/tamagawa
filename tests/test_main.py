class TestGetAll:
    def test_valid_command(self, tamagawa):
        assert tamagawa.send(b"GET_ALL TEST\r\n.\r\n") == b"200 OK! TEST\r\n"

    def test_valid_command2(self, tamagawa):
        assert tamagawa.send(b"GET_ALL tamagawa\r\n.\r\n") == b"200 OK! tamagawa\r\n"

    def test_invalid_parameter(self, tamagawa):
        assert tamagawa.send(b"GET_ALL\r\n.\r\n") == b"502 Bad Parameter\r\n"

    def test_without_dot(self, tamagawa):
        assert tamagawa.send(b"GET_ALL\r\na\r\n") == b"522 Bad Request.\r\n"


class TestQuit:
    def test_valid_command(self, tamagawa):
        assert tamagawa.send(b"QUIT\r\n") == b"QUIT\r\n"


class TestInvalidCommand:
    def test_invalid_command(self, tamagawa):
        assert tamagawa.send(b"TEST\r\n") == b"Command is invalid.\r\n"
