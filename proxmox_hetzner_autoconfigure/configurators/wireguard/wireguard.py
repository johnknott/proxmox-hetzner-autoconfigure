"""Network Configurator"""

from typing import NamedTuple
from ipaddress import IPv4Network
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Data structure that gets emitted from gather_input and passed into transform_to_commands"""

    vpn_network: str
    vpn_cidr_netmask: str
    vpn_first_ip: str
    vpn_second_ip: str


class Config(cfg.Configurator):
    """Implementation of the Network Configurator"""

    def __init__(self):
        super().__init__()
        self.short_description = "wireguard"
        self.description = "Configure Wireguard VPN"

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a NetworkData"""

        vpn_network = util.input_network(
            "Please enter desired VPN details in CIDR notation", init="10.0.10.0/24",
        )

        if vpn_network is None:
            return None

        net_vpn = IPv4Network(vpn_network)
        vpn_first_ip = str(list(net_vpn.hosts())[0])
        vpn_second_ip = str(list(net_vpn.hosts())[1])
        vpn_cidr_netmask = net_vpn.prefixlen

        return Data(
            vpn_network=vpn_network,
            vpn_cidr_netmask=vpn_cidr_netmask,
            vpn_first_ip=vpn_first_ip,
            vpn_second_ip=vpn_second_ip,
        )

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""
        return util.render_template(__file__, "template", data)
