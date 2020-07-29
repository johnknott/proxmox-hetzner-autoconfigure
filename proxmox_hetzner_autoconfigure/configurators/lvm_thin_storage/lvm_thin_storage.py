"""TLS Configurator"""

from typing import NamedTuple
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Tuple that gets emitted from gather_input and passed into transform_to_commands"""

    vg_name: str
    lv_name: str


class Config(cfg.Configurator):
    """Implementation of an example Configurator"""

    def __init__(self):
        super().__init__()
        self.description = "Configure LVM Thin Storage"

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a Data"""

        return Data(vg_name="vg0", lv_name="data")

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""
        return util.render_template(__file__, "template", data)
