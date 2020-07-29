"""TLS Configurator"""

from typing import NamedTuple
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Tuple that gets emitted from gather_input and passed into transform_to_commands"""

    username: str
    password: str
    server: str


class Config(cfg.Configurator):
    """Implementation of an example Configurator"""

    def __init__(self):
        super().__init__()
        self.description = "Hetzner Storage Box"

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a Data"""

        username = password = server = ""

        username = util.input_regex(
            "Please enter your Storage Box username (e.g. u123456)",
            util.NOT_EMPTY,
            "Please enter username",
        )
        if username is None:
            return None

        code, password = util.dialog.inputbox(
            "Please enter your Storage Box password. Leave empty to be asked later, "
            "or to provide with env variables.",
            title="Please enter password",
        )
        if code != "ok":
            return None

        server = util.input_regex(
            "Please enter your Storage Box server",
            util.NOT_EMPTY,
            "Please enter server",
            init=f"{username}.your-storagebox.de",
        )
        if server is None:
            return None

        return Data(username=username, password=password, server=server)

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""
        fstab_line = f"//{data.server}/backup /mnt/storage cifs _netdev,username={data.username},password=$STORAGE_BOX_PASSWORD,uid=101001,gid=101001 0 0"  # pylint: disable=line-too-long
        return util.render_template(
            __file__, "template", {"fstab_line": fstab_line, "password": data.password}
        )
