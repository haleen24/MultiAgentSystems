import datetime
from uuid import uuid4 as uuid


class EventLog:
    def __init__(self, who, net):
        self.id = uuid()
        self.who = who
        self.timestamp = datetime.datetime.now()
        self.net = net

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return "; ".join(map(str, vars(self).values()))

    @classmethod
    def header(cls):
        return "; ".join(vars(EventLog(None, None)).keys())
