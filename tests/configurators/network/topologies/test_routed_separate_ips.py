"""Test the Network Configurator"""
from unittest.mock import MagicMock
from proxmox_hetzner_autoconfigure import util
from proxmox_hetzner_autoconfigure.configurators.network.topologies import routed_separate_ips


def test_description():
    network_config = routed_separate_ips.Config()
    assert (
        network_config.description
        == "(BETA) Traffic routed through host system and you have additional separate IPs"
    )


def test_gather_input_correct():
    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", "192.168.0.1"],
        ["ok", "192.168.0.254"],
        ["ok", "10.0.0.0/24"],
        ["ok", "123.123.123.123"],
    ]

    network_config = routed_separate_ips.Config()

    routed_separate_ips.util.dialog = dialog
    assert network_config.gather_input() == routed_separate_ips.Data(
        hetzner_ip="192.168.0.1",
        gateway_ip="192.168.0.254",
        private_subnet="10.0.0.0/24",
        additional_ip="123.123.123.123",
    )


def test_gather_input_cancelled():
    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", "192.168.0.1"],
        ["ok", "192.168.0.254"],
        ["cancel", ""],
    ]

    network_config = routed_separate_ips.Config()
    routed_separate_ips.util.dialog = dialog
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
        ["ok", "pies"],
        ["ok", "123.123.123.123"],
    ]

    network_config = routed_separate_ips.Config()
    routed_separate_ips.util.dialog = dialog
    assert network_config.gather_input() == routed_separate_ips.Data(
        hetzner_ip="192.168.0.7",
        gateway_ip="192.168.0.254",
        private_subnet="10.0.0.0/24",
        additional_ip="123.123.123.123",
    )


def test_generate_script():

    config = routed_separate_ips.Config()
    data = routed_separate_ips.Data(
        hetzner_ip="192.168.0.1",
        gateway_ip="192.168.0.254",
        private_subnet="10.0.0.0/24",
        additional_ip="123.123.123.123",
    )

    script = config.generate_script(data)
    assert "address 192.168.0.1" in script
    assert "pointopoint 192.168.0.254" in script
    assert "gateway 192.168.0.254" in script
    assert "address 10.0.0.0/24" in script
    assert "up ip route add 123.123.123.123/32 dev vmbr0" in script
    assert (
        "post-up iptables -t nat -A POSTROUTING -s '10.0.0.0/24' -o enp2s0 -j MASQUERADE" in script
    )
    assert (
        "post-up iptables -t nat -A POSTROUTING -s '10.0.0.0/24' -o enp2s0 -j MASQUERADE" in script
    )
