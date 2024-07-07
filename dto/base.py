from dataclasses import asdict

class BaseDto:
    def as_dict(self):
        return asdict(self)
