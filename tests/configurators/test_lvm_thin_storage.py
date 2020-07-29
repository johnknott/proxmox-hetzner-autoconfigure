"""Test the Network Configurator"""
from unittest.mock import MagicMock
from proxmox_hetzner_autoconfigure import util
from proxmox_hetzner_autoconfigure.configurators import lvm_thin_storage


def test_description():
    config = lvm_thin_storage.Config()
    assert config.description == "Configure LVM Thin Storage"


def test_gather_input_correct():

    config = lvm_thin_storage.Config()
    assert config.gather_input() == lvm_thin_storage.Data(vg_name="vg0", lv_name="data")


def test_generate_script():

    config = lvm_thin_storage.Config()
    data = lvm_thin_storage.Data(vg_name="vg0", lv_name="data")

    script = config.generate_script(data)
    assert "lvcreate -l +99%FREE -n data vg0" in script
    assert "lvconvert --type thin-pool vg0/data" in script
    assert "pvesm add lvmthin thin-pool --thinpool data --vgname vg0" in script
