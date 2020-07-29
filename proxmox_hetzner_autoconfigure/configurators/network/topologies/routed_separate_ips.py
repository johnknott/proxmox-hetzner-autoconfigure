"""Network Configurator"""

from typing import NamedTuple
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Data structure that gets emitted from gather_input and passed into transform_to_commands"""

    hetzner_ip: str
    gateway_ip: str
    private_network: str
    additional_ip: str


class Config(cfg.Configurator):
    """Implementation of the Network Configurator"""

    def __init__(self):
        super().__init__()
        self.short_description = "routed_separate_ips"
        self.description = (
            "(BETA) Traffic routed through host system and you have additional separate IPs"
        )

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a NetworkData"""

        hetzner_ip = gateway_ip = private_network = additional_ip = ""

        if util.is_proxmox_machine():
            hetzner_ip = util.main_ip()
            gateway_ip = util.gateway_ip()

        hetzner_ip = util.input_ip(
            "Please enter your servers main public facing IP address at Hetzner", init=hetzner_ip,
        )

        if hetzner_ip is None:
            return None

        gateway_ip = util.input_ip(
            "Please enter your servers Gateway IP address at Hetzner", init=gateway_ip,
        )

        if gateway_ip is None:
            return None

        private_network = util.input_network(
            "Please enter desired private network in CIDR notation", init="10.0.1.0/24",
        )

        if private_network is None:
            return None

        additional_ip = util.input_ip(
            "Please enter one of your additional IPs", init=additional_ip,
        )

        if additional_ip is None:
            return None

        return Data(
            hetzner_ip=hetzner_ip,
            gateway_ip=gateway_ip,
            private_network=private_network,
            additional_ip=additional_ip,
        )

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""
        interfaces = util.render_template(__file__, "routed_separate_ips", data)
        heredoc = util.wrap_as_heredoc(interfaces, "/etc/network/interfaces")
        return util.render_template(__file__, "routed_wrapper", {"heredoc": heredoc})
