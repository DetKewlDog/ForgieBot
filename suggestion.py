from interactions import *
from settings import *
from bugreport import *


class Suggestion:

    def __init__(self, msg, id):
        self.msg = msg
        self.id = id

    def __str__(self):
        return f"{self.msg} {self.id}"


def str_to_sug(str):
    msg, id = str.replace('\n', '').split(' ')
    return Suggestion(msg, id)
