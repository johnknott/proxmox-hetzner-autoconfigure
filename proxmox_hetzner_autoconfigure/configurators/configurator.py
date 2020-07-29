"""Configurator Abstract Base Class"""
from typing import NamedTuple
from abc import ABC, abstractmethod
from proxmox_hetzner_autoconfigure.util import util


class Configurator(ABC):
    """Derive from this and implement the abstract methods to create a configurator."""

    def __init__(self):
        self.short_description = self.description = ""

    def to_script(self):
        """Called to collect input from the user then return a shell script snippet"""
        util.dialog.set_background_title(self.description)
        return self.generate_script(self.gather_input())

    @abstractmethod
    def gather_input(self) -> NamedTuple:
        """Implement in derived class to gather input from the user.

        Returns:
            Textual description of the module
        """

    @abstractmethod
    def generate_script(self, data: NamedTuple) -> str:
        """Implement in derived class to gather input from the user.

        Returns:
            Textual description of the module
        """
