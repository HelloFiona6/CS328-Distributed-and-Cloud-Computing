from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReportStatsRequest(_message.Message):
    __slots__ = ("user_name", "institution", "values")
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTITUTION_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    user_name: str
    institution: str
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, user_name: _Optional[str] = ..., institution: _Optional[str] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class ReportStatsResponse(_message.Message):
    __slots__ = ("min_value", "max_value", "avg_value", "message")
    MIN_VALUE_FIELD_NUMBER: _ClassVar[int]
    MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
    AVG_VALUE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    min_value: float
    max_value: float
    avg_value: float
    message: str
    def __init__(self, min_value: _Optional[float] = ..., max_value: _Optional[float] = ..., avg_value: _Optional[float] = ..., message: _Optional[str] = ...) -> None: ...
