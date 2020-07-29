"""Test the Network Configurator"""
from unittest.mock import MagicMock
from proxmox_hetzner_autoconfigure import main
from proxmox_hetzner_autoconfigure.configurators import tls


def test_end_to_end():

    dialog = MagicMock()
    dialog.msgbox.side_effect = [
        ["ok"],
    ]
    dialog.checklist.side_effect = [["ok", []]]
    main.util.dialog = dialog

    result = main.run()

