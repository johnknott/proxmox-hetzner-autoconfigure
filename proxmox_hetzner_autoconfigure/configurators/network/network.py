"""Network Configurator"""

from typing import NamedTuple
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg
from proxmox_hetzner_autoconfigure.configurators.network.topologies import (
    routed_subnet,
    routed_separate_ips,
)


class Data(NamedTuple):
    """Data structure that gets emitted from gather_input and passed into transform_to_commands"""

    generated_script: str


class Config(cfg.Configurator):
    """Implementation of the Network Configurator"""

    def __init__(self):
        super().__init__()
        self.description = "Configure Network"

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a NetworkData"""

        topologies = [routed_subnet, routed_separate_ips]
        topology_configs = list(map(lambda t: t.Config(), topologies))

        code, choice = util.dialog.radiolist(
            "Please choose a network topology",
            choices=map(lambda c: (c.short_description, c.description, 1), topology_configs),
        )

        if code != "ok":
            return None

        chosen_config = next(filter(lambda x: x.short_description == choice, topology_configs))
        script = chosen_config.generate_script(chosen_config.gather_input())

        return Data(generated_script=script)

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""
        return data.generated_script if data else ""
