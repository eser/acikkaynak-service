from enum import Enum


class CertificateTypes(str, Enum):
    PROGRAM = "program"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
