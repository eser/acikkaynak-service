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


class ProfileAchievementTypes(str, Enum):
    CLASS_ATTEND = "class attend"
    OPEN_SOUCE_CONTRIBUTION = "open source contribution"
    PUBLISHED_ARTICLE = "published article"
    PRESENTATION = "presentation"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
