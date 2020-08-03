"""Test the Network Configurator"""
from unittest.mock import MagicMock
from proxmox_hetzner_autoconfigure import util
from proxmox_hetzner_autoconfigure.configurators import snippets


def test_description():
    config = snippets.Config()
    assert config.description == "Configure Snippets"


def test_gather_input_correct():

    dialog = MagicMock()
    dialog.checklist.side_effect = [["ok", ["test_desc"]]]

    config = snippets.Config()
    snippets.util.dialog = dialog
    assert config.gather_input() == snippets.Data(snippets=[])


def test_generate_script():

    print("asdasdasd")
    config = snippets.Config()
    data = snippets.Data(
        snippets=[
            {
                "filename": "filename",
                "content": "content",
                "short_description": "test_short_desc",
                "description": "test_desc",
            }
        ]
    )

    script = config.generate_script(data=data)
    assert "Configuring Snippets: filename" in script
