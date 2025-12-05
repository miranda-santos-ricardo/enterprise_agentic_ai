# src/agents/base.py
from abc import ABC, abstractmethod


class Agent(ABC):
    @abstractmethod
    def name(self) -> str:
        ...

