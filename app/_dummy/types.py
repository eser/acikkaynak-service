from enum import Enum


class AchievementTypes(str, Enum):
    CLASS_ATTEND = "class attend"
    CONTRIBUTION = "contribution"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
