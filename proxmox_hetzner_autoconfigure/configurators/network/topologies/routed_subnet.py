"""Network Configurator"""

from typing import NamedTuple
from ipaddress import IPv4Network
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Data structure that gets emitted from gather_input and passed into transform_to_commands"""

    hetzner_ip: str
    gateway_ip: str
    private_network: str
    private_network_first_ip: str
    public_subnet: str
    public_subnet_first_ip: str
    public_subnet_netmask: str
    private_subnet_netmask: str
    example_public_subnet_address: str
    example_private_subnet_address: str


class Config(cfg.Configurator):
    """Implementation of the Network Configurator"""

    def __init__(self):
        super().__init__()
        self.short_description = "routed_subnet"
        self.description = "Traffic routed through host system and you have purchased a subnet"

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a NetworkData"""

        hetzner_ip = gateway_ip = private_network = public_subnet = ""

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

        public_subnet = util.input_network(
            "Please enter your Hetzner public subnet in CIDR notation, e.g. x.x.x.x/29",
            init=public_subnet,
        )

        if public_subnet is None:
            return None

        net_priv = IPv4Network(private_network)
        net_pub = IPv4Network(public_subnet)

        return Data(
            hetzner_ip=hetzner_ip,
            gateway_ip=gateway_ip,
            private_network=private_network,
            private_network_first_ip=str(list(net_priv.hosts())[0]),
            private_subnet_netmask=str(net_priv.netmask),
            public_subnet=public_subnet,
            public_subnet_first_ip=str(list(net_pub.hosts())[0]),
            public_subnet_netmask=str(net_pub.netmask),
            example_private_subnet_address=str(list(net_priv.hosts())[1]),
            example_public_subnet_address=str(list(net_pub.hosts())[1]),
        )

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""

        interfaces = util.render_template(__file__, "routed_subnet", data)
        heredoc = util.wrap_as_heredoc(interfaces, "/etc/network/interfaces")
        return util.render_template(__file__, "routed_wrapper", {"heredoc": heredoc})
