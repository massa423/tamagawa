from typing import List


class Get_all():
    """
    Get_all class
    """
    def __init__(self, buffered_args: List):
        self.buffered_args = buffered_args

    def execute(self) -> bytes:
        """
        execute
        """

        if not self.buffered_args:
            response = b"502 Bad Parameter"
        else:
            self.__validate()
            response = b"200 OK!"

        return response

    def __validate(self):
        """
        validate
        """
        pass
