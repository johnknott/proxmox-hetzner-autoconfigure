"""Test the Network Configurator"""
from unittest.mock import MagicMock

from proxmox_hetzner_autoconfigure.configurators.network.topologies import routed_subnet


def test_description():
    network_config = routed_subnet.Config()
    assert (
        network_config.description
        == "Traffic routed through host system and you have purchased a subnet"
    )


def test_gather_input_correct():
    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", "192.168.0.1"],
        ["ok", "192.168.0.254"],
        ["ok", "10.0.0.0/24"],
        ["ok", "123.123.123.0/29"],
    ]

    network_config = routed_subnet.Config()

    routed_subnet.util.dialog = dialog
    assert network_config.gather_input() == routed_subnet.Data(
        hetzner_ip="192.168.0.1",
        gateway_ip="192.168.0.254",
        private_network="10.0.0.0/24",
        private_network_first_ip="10.0.0.1",
        public_subnet="123.123.123.0/29",
        example_private_subnet_address="10.0.0.2",
        example_private_subnet_netmask="255.255.255.0",
        example_public_subnet_address="123.123.123.2",
        example_public_subnet_netmask="255.255.255.248",
    )


def test_gather_input_cancelled():
    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", "192.168.0.1"],
        ["ok", "192.168.0.254"],
        ["cancel", ""],
    ]

    network_config = routed_subnet.Config()
    routed_subnet.util.dialog = dialog
    assert network_config.gather_input() is None


def test_gather_input_bad_data():
    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", ""],
        ["ok", "asdfgh"],
        ["ok", "192.168.0.7"],
        ["ok", "xxx"],
        ["ok", "192.168.0.254"],
        ["ok", "10.0.0.1"],
        ["ok", "10.0.0.0/24"],
        ["ok", "123.123.123.123/2933"],
        ["ok", "123.123.123.0/29"],
    ]

    network_config = routed_subnet.Config()
    routed_subnet.util.dialog = dialog
    assert network_config.gather_input() == routed_subnet.Data(
        hetzner_ip="192.168.0.7",
        gateway_ip="192.168.0.254",
        private_network="10.0.0.0/24",
        private_network_first_ip="10.0.0.1",
        public_subnet="123.123.123.0/29",
        example_private_subnet_address="10.0.0.2",
        example_private_subnet_netmask="255.255.255.0",
        example_public_subnet_address="123.123.123.2",
        example_public_subnet_netmask="255.255.255.248",
    )


def test_generate_script():

    config = routed_subnet.Config()
    data = routed_subnet.Data(
        hetzner_ip="192.168.0.1",
        gateway_ip="192.168.0.254",
        private_network="10.0.0.0/24",
        private_network_first_ip="10.0.0.1",
        public_subnet="123.123.123.0/29",
        example_private_subnet_address="10.0.0.2",
        example_private_subnet_netmask="255.255.255.0",
        example_public_subnet_address="123.123.123.2",
        example_public_subnet_netmask="255.255.255.248",
    )

    script = config.generate_script(data)
    print(script)
    assert "address 192.168.0.1" in script
    assert "pointopoint 192.168.0.254" in script
    assert "gateway 192.168.0.254" in script
    assert "address 10.0.0.1" in script
    assert "address 123.123.123.0/29" in script
    assert (
        "post-up iptables -t nat -A POSTROUTING -s '10.0.0.0/24' -o enp2s0 -j MASQUERADE" in script
    )
    assert (
        "post-up iptables -t nat -A POSTROUTING -s '10.0.0.0/24' -o enp2s0 -j MASQUERADE" in script
    )
