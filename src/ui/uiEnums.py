from enum import Enum, auto


class ValidityEnum(Enum):
    NoStatement = -1
    Valid = auto()
    Invalid = auto()


class AppStatusEnum(Enum):
    NotReady = auto()
    Ready = auto()
    Locked = auto()
    Unlocked = auto()
    Solving = auto()
    Solved = auto()


class SquareTypeEnum(Enum):
    Unset = -1
    InputUnlocked = auto()
    InputLocked = auto()
    UserSet = auto()
    Solved = auto()
