from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TellStoryRequest(_message.Message):
    __slots__ = ("user_name", "institution")
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTITUTION_FIELD_NUMBER: _ClassVar[int]
    user_name: str
    institution: str
    def __init__(self, user_name: _Optional[str] = ..., institution: _Optional[str] = ...) -> None: ...

class TellStoryResponse(_message.Message):
    __slots__ = ("text_chunk",)
    TEXT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    text_chunk: bytes
    def __init__(self, text_chunk: _Optional[bytes] = ...) -> None: ...
