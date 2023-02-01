class BugReport:
    def __init__(self, msg, id, status):
        self.msg = msg
        self.id = id
        self.status = status

    def __str__(self):
        return f"{self.msg} {self.id} {self.status}"


def str_to_bug(str):
    msg, id, status = str.replace('\n', '').split(' ')
    return BugReport(msg, id, status)