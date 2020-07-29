"""Test the Network Configurator"""
from unittest.mock import MagicMock
from proxmox_hetzner_autoconfigure import util
from proxmox_hetzner_autoconfigure.configurators import storage_box


def test_description():
    config = storage_box.Config()
    assert config.description == "Hetzner Storage Box"


def test_gather_input_correct():

    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", "u123456"],
        ["ok", "password123"],
        ["ok", "u123456.your-storagebox.de"],
    ]

    config = storage_box.Config()

    storage_box.util.dialog = dialog

    assert config.gather_input() == storage_box.Data(
        username="u123456", password="password123", server="u123456.your-storagebox.de",
    )


def test_gather_input_cancelled():
    dialog = MagicMock()
    dialog.inputbox.side_effect = [
        ["ok", "u123456"],
        ["cancel", ""],
    ]

    config = storage_box.Config()
    storage_box.util.dialog = dialog
    assert config.gather_input() is None


def test_generate_script():

    config = storage_box.Config()
    data = storage_box.Data(
        username="u123456", password="password123", server="u123456.your-storagebox.de",
    )

    script = config.generate_script(data)
    assert (
        "//u123456.your-storagebox.de/backup /mnt/storage cifs _netdev,username=u123456,password=$STORAGE_BOX_PASSWORD,uid=101001,gid=101001 0 0"
        in script
    )
