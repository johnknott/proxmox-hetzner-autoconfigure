"""Test the Network Configurator"""
from unittest.mock import MagicMock
from proxmox_hetzner_autoconfigure import util
from proxmox_hetzner_autoconfigure.configurators import network


def test_description():
    network_config = network.Config()
    assert network_config.description == "Configure Network"


def test_gather_input_correct():
    dialog = MagicMock()
    dialog.radiolist.side_effect = [
        ["ok", "routed_subnet"],
    ]
    dialog.inputbox.side_effect = [
        ["ok", "192.168.0.1"],
        ["ok", "192.168.0.254"],
        ["ok", "10.0.0.0/24"],
        ["ok", "123.123.123.0/29"],
    ]

    network_config = network.Config()
    network.util.dialog = dialog

    assert "/etc/network/interfaces" in network_config.gather_input().generated_script
