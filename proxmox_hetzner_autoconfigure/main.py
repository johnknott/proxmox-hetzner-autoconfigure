"""Main entrypoint"""
import locale
import sys
import os
from proxmox_hetzner_autoconfigure.configurators import (
    network,
    tls,
    storage_box,
    snippets,
    wireguard,
)
from proxmox_hetzner_autoconfigure.util import util


def run():
    """Main entrypoint"""
    configurators = [network, tls, storage_box, snippets, wireguard]

    if not os.environ.get("LC_ALL"):
        os.environ["LC_ALL"] = "C"

    locale.setlocale(locale.LC_ALL, "")

    util.dialog.msgbox(
        "This script will help configure your Network, Wireguard VPN, Security, "
        "TLS keys, DNS and Storage on your Hetzner based Proxmox Host Node.\n\n"
        "It will not make any changes to your system.\n\n"
        "It outputs a single script file with no dependencies you can "
        "inspect and then run manually. "
        "You can then add this script file to source control.",
        title="Welcome!",
        colors=True,
    )

    code, chosen = util.dialog.checklist(
        "Please choose which components you would like to configure.",
        choices=map(lambda x: [x.Config().description, "", 1], configurators),
    )

    if code != "ok":
        return None

    chosen_configurators = filter(lambda x: x.Config().description in chosen, configurators)

    script = util.build_script(chosen_configurators)

    if "pytest" not in sys.modules:
        bootstrap_file = "bootstrap.sh"
        text_file = open(bootstrap_file, "w")
        text_file.write(script)
        text_file.close()
        os.chmod(bootstrap_file, 0o744)
        print(f"Completed! {bootstrap_file} has been written to the working directory.")
