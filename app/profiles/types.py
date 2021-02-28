from enum import Enum


class ProfileStatuses(str, Enum):
    DISABLED = "disabled"
    ACTIVE = "active"
    VERIFIED = "verified"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ProfileTypes(str, Enum):
    INDIVIDUAL = "individual"
    ORGANIZATION = "organization"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
