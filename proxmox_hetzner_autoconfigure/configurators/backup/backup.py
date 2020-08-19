"""TLS Configurator"""

from typing import NamedTuple
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Tuple that gets emitted from gather_input and passed into transform_to_commands"""

    destination: str
    schedule_backups: bool


class Config(cfg.Configurator):
    """Implementation of an example Configurator"""

    def __init__(self):
        super().__init__()
        self.description = "Proxmox Host System Backup"

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a Data"""

        destination = ""

        destination = util.input_regex(
            "Please enter your backup destination path",
            util.NOT_EMPTY,
            "Please enter backup path",
            init="/mnt/storage/storage",
        )
        if destination is None:
            return None

        schedule_backups = util.dialog.yesno("Do you want to schedule backups using Cron?") == "ok"

        return Data(destination=destination, schedule_backups=schedule_backups,)

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""

        return util.render_template(
            __file__,
            "template",
            {"destination": data.destination, "schedule_backups": data.schedule_backups,},
        )
