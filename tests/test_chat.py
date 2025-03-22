import os
import sys

__parent_dir = os.path.dirname(
    os.path.dirname(
        os.path.abspath(
            __file__
            )
        )
    )

if __parent_dir not in sys.path:
    sys.path.insert(
        0,
        __parent_dir
    )

from downedit.agents.providers import (
    Role,
    Chat
)


if __name__ == "__main__":
    history = Chat(
        model="gpt-9999",
        messages=[]
    )

    history.add_input(
        role=Role.system,
        message="You are a helpful assistant."
    )

    history.add_input(
        role=Role.user,
        message="What is Python?"
    )

    history.add_answer(
        role=Role.assistant,
        message="Python is a high-level, interpreted programming language..."
    )

    for msg in history.messages:
        print(f"{msg.role.value}: {msg.content}")

    print(
        history.model_dump_json(
            indent=4
        )
    )