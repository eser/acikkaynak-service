from enum import Enum


class CertificateStatuses(str, Enum):
    DISABLED = "disabled"
    ACTIVE = "active"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class CertificateTypes(str, Enum):
    PROGRAM = "program"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class CertificateClaimStatuses(str, Enum):
    REJECTED = "rejected"
    AWAITING_APPROVAL = "awaiting approval"
    ACCEPTED = "accepted"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
