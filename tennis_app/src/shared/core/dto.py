from dataclasses import asdict


class BaseDTO:
    def asdict(self):
        return asdict(self)
