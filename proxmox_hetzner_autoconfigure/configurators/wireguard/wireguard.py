"""Network Configurator"""

import random
from typing import NamedTuple
from ipaddress import IPv4Network
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Data structure that gets emitted from gather_input and passed into transform_to_commands"""

    wireguard_address_base: str
    wireguard_cidr_netmask: str
    dns_server: str
    port: int


class Config(cfg.Configurator):
    """Implementation of the Network Configurator"""

    def __init__(self):
        super().__init__()
        self.short_description = "wireguard"
        self.description = "Configure Wireguard VPN"

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a NetworkData"""

        wireguard_subnet = util.input_network(
            "Please enter desired VPN details in CIDR notation", init="10.0.10.0/24",
        )

        if wireguard_subnet is None:
            return None

        net_wireguard = IPv4Network(wireguard_subnet)
        first_host = str(list(net_wireguard.hosts())[0])
        ip, wireguard_cidr_netmask = wireguard_subnet.split("/")
        wireguard_address_base = ip[: ip.rfind(".") + 1]
        dns_server = first_host if util.shared_globals.get("DNSMasq") else "8.8.8.8"

        port = random.randint(50000, 60000)
        util.shared_globals["wireguard_port"] = port
        util.shared_globals["wireguard"] = True
        util.shared_globals["wireguard_subnet"] = wireguard_subnet

        return Data(
            wireguard_address_base=wireguard_address_base,
            wireguard_cidr_netmask=wireguard_cidr_netmask,
            dns_server=dns_server,
            port=port,
        )

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""
        return util.render_template(__file__, "template", data)
