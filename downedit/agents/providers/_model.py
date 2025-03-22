from enum       import Enum
from typing     import List
from pydantic   import BaseModel


__alll__ = [
    "Role",
    "Message",
    "Chat",
]


class Role(Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    role: Role
    content: str


class Chat(BaseModel):
    model: str
    messages: List[Message] = []

    def add_input(
        self, role: Role,
        message: str
    ) -> None:
        self.messages.append(
            Message(role=role.value, content=message)
        )

    def add_answer(
        self, role: Role,
        message: str
    ) -> None:
        self.messages.append(
            Message(role=role.value, content=message)
        )

    def model_dump(self):
        return {
            "model": self.model,
            "messages": [
                {"role": msg.role.value, "content": msg.content} for msg in self.messages
            ]
        }