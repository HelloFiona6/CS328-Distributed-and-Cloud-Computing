from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GuessIntRequest(_message.Message):
    __slots__ = ("guess",)
    GUESS_FIELD_NUMBER: _ClassVar[int]
    guess: int
    def __init__(self, guess: _Optional[int] = ...) -> None: ...

class GuessIntResponse(_message.Message):
    __slots__ = ("message", "guess", "symbol")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GUESS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    message: str
    guess: int
    symbol: str
    def __init__(self, message: _Optional[str] = ..., guess: _Optional[int] = ..., symbol: _Optional[str] = ...) -> None: ...
