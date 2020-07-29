"""TLS Configurator"""

from typing import NamedTuple
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Tuple that gets emitted from gather_input and passed into transform_to_commands"""

    email: str
    domain: str


class Config(cfg.Configurator):
    """Implementation of an example Configurator"""

    def __init__(self):
        super().__init__()
        self.description = "Configure TLS (Lets Encrypt)"

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a Data"""

        email = domain = ""

        email = util.input_regex(
            "Please enter your email address", util.EMAIL_REGEX, "Invalid Email",
        )
        if email is None:
            return None

        domain = util.input_regex(
            "Please enter your domain name (FQDN)." "Must be resolvable from the Internet.",
            util.DOMAIN_REGEX,
            "Invalid Domain",
        )
        if domain is None:
            return None

        return Data(email, domain)

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""
        return util.render_template(__file__, "template", data)
