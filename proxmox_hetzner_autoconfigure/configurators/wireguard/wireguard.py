"""Network Configurator"""

from typing import NamedTuple
from ipaddress import IPv4Network
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Data structure that gets emitted from gather_input and passed into transform_to_commands"""

    vpn_address_base: str
    vpn_cidr_netmask: str
    dns_server: str


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
        first_host = str(list(net_vpn.hosts())[0])
        ip, vpn_cidr_netmask = vpn_network.split("/")
        vpn_address_base = ip[: ip.rfind(".") + 1]
        dns_server = first_host if util.shared_globals.get("DNSMasq") else "8.8.8.8"

        return Data(
            vpn_address_base=vpn_address_base,
            vpn_cidr_netmask=vpn_cidr_netmask,
            dns_server=dns_server,
        )

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""
        return util.render_template(__file__, "template", data)
