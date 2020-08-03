"""Test the Network Configurator"""
from unittest.mock import MagicMock
from proxmox_hetzner_autoconfigure import main


def test_end_to_end():

    dialog = MagicMock()
    dialog.msgbox.side_effect = [
        ["ok"],
    ]
    dialog.checklist.side_effect = [["ok", []]]
    main.util.dialog = dialog

    main.run()

