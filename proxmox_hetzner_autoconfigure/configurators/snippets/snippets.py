"""Snippets Configurator"""

import glob
import os
import toml
from pathlib import Path
from typing import NamedTuple, List
from proxmox_hetzner_autoconfigure.util import util
from proxmox_hetzner_autoconfigure.configurators import configurator as cfg


class Data(NamedTuple):
    """Tuple that gets emitted from gather_input and passed into transform_to_commands"""

    snippets: List


class Config(cfg.Configurator):
    """Implementation of an example Configurator"""

    def __init__(self):
        super().__init__()
        self.description = "Configure Snippets"

    def gather_input(self) -> Data:
        """Gathers input from the user and returns a Data"""

        def load_toml(tml):
            t = toml.load(tml)
            t["filename"] = Path(tml).stem
            return t

        current_dir = os.path.dirname(os.path.realpath(__file__))
        tomls = glob.iglob(f"{current_dir}/*.toml")
        snippets = [load_toml(tml) for tml in tomls]

        code, chosen = util.dialog.checklist(
            "Please choose which snippets you would like to include.",
            choices=[
                [snippet["short_description"], snippet["description"], 1] for snippet in snippets
            ],
        )

        if code != "ok":
            return None

        def save_in_globals(snippet):
            util.shared_globals[snippet["short_description"].lower()] = True
            return snippet

        chosen_snippets = [save_in_globals(s) for s in snippets if s["short_description"] in chosen]

        return Data(snippets=chosen_snippets)

    def generate_script(self, data: Data) -> str:
        """transforms a Data into a shell script segment"""

        def render_snippet(snippet):

            snippet["content"] = util.render_template(
                __file__, snippet["filename"], {"shared_globals": util.shared_globals}
            )
            return snippet

        return util.render_template(
            __file__, "template", Data(snippets=[render_snippet(s) for s in data.snippets])
        )
