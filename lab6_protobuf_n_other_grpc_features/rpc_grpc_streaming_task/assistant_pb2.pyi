from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CountRequest(_message.Message):
    __slots__ = ("from_val", "step_sec")
    FROM_VAL_FIELD_NUMBER: _ClassVar[int]
    STEP_SEC_FIELD_NUMBER: _ClassVar[int]
    from_val: int
    step_sec: int
    def __init__(self, from_val: _Optional[int] = ..., step_sec: _Optional[int] = ...) -> None: ...

class CountResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
