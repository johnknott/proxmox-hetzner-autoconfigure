"""Test the Network Configurator"""
from unittest.mock import MagicMock
from proxmox_hetzner_autoconfigure import util
from proxmox_hetzner_autoconfigure.configurators import tls


def test_description():
    config = tls.Config()
    assert config.description == "Configure TLS (Lets Encrypt)"


def test_gather_input_correct():

    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", "test.user@example.com"],
        ["ok", "host.example.com"],
    ]

    config = tls.Config()

    tls.util.dialog = dialog

    assert config.gather_input() == tls.Data(
        email="test.user@example.com", domain="host.example.com"
    )


def test_gather_input_cancelled():
    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", "test.user@example.com"],
        ["cancel", ""],
    ]

    config = tls.Config()
    tls.util.dialog = dialog
    assert config.gather_input() is None


def test_gather_input_bad_data():
    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", "not_an_email"],
        ["ok", "123123"],
        ["ok", "test.user@example.com"],
        ["ok", "notadomain"],
        ["ok", "host.example.com"],
    ]

    config = tls.Config()

    tls.util.dialog = dialog
    assert config.gather_input() == tls.Data(
        email="test.user@example.com", domain="host.example.com"
    )


def test_generate_script():

    config = tls.Config()
    data = tls.Data(email="test.user@example.com", domain="host.example.com")

    script = config.generate_script(data)
    assert "pvenode acme account register default test.user@example.com" in script
    assert "pvenode config set --acme domains=host.example.com" in script
    assert "pvenode acme cert order" in script
