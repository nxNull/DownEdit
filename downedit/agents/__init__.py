r"""
This package contains the agents for the DownEdit tool.

Modules:
    _factory: Contains the AIFactory class which is responsible for creating AI instances.
    __sima: Contains the SIMA class, which is a single instruction for multiple agents.

Classes:
    AIFactory: A factory class for creating AI instances.
    SIMA: Single Instruction Multiple Agents.

Usage:
    from downedit.agents import AIFactory, SIMA, Agent
"""

from .agent import Agent
from .prompts import SYSTEM_PROMPTS
from ._factory import AIFactory
from .__sima import SIMA

from downedit.agents.providers import (
    Provider,
    CLOUD_FACTORY,
    LOCAL_FACTORY,

    Role,
    Message,
    Chat,

    AIConfig,
)


__all__ = [
    "SIMA",
    "AIFactory",
    "Agent",

    "Role",
    "Message",
    "Chat",

    "Provider",
    "CLOUD_FACTORY",
    "LOCAL_FACTORY",

    "AIConfig",
    "SYSTEM_PROMPTS",
]
