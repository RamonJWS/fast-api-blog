from dataclasses import dataclass


@dataclass
class FakeUser:
    username: str
    email: str
    password: str