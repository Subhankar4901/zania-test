import enum
class ResourceState(enum.IntEnum):
    InsufficientStock=0
    PartiallySufficientStock=1
    SufficientStock=2
    NonExistantProducts=3
    NewProduct=4
    DataBaseFailure=5