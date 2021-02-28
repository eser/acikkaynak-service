from enum import Enum


class CurrencyTypes(str, Enum):
    TRY = "turkish lira"
    EUR = "euro"
    USD = "us dollar"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Genders(str, Enum):
    FEMALE = "female"
    MALE = "male"
    OTHER = "other"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
