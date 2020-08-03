"""Collection of utility methods"""
import os
import re
import platform
from pathlib import Path
from ipaddress import IPv4Network, IPv4Address
from dialog import Dialog
from jinja2 import Environment, FileSystemLoader


IP_REGEX = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
CIDR_REGEX = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}\b"
EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
DOMAIN_REGEX = r".*\.\w+"
NOT_EMPTY = r"^(?!\s*$).+"


ANSI_RED = r"\Zb\Z1"
ANSI_GREEN = r"\Zb\Z3"
ANSI_WHITE = r"\Zb\Z2"
ANSI_RESET = r"\Zn"

dialog = Dialog(dialog="dialog", autowidgetsize=True)
all_binds = {}


def is_proxmox_machine():
    """Is this a Linux machine with Proxmox installed?"""
    return platform.system() == "Linux" and os.popen("which pveversion").read().strip()


def main_ip():
    """Returns the detected main IP of this machine"""
    return os.popen("hostname -i | awk '{print $1}'").read().strip()


def gateway_ip():
    """Returns the detected gateway IP of this machine"""
    return os.popen("ip route | grep default | awk '{print $3}'").read().strip()


def render_template(file, template_name, binds):
    """Renders a jinja2 template and returns it as a string"""
    dir_path = os.path.dirname(os.path.realpath(file))
    env = Environment(loader=FileSystemLoader(dir_path))
    template = env.get_template(f"{template_name}.jinja2")

    if hasattr(binds, "_asdict"):
        binds = binds._asdict()

    # Store the dbinds in a global so that we can access the data from elsewhere
    all_binds[template_name] = binds

    return template.render(binds)


def wrap_as_heredoc(content, filename):
    """Wraps a string in a heredoc and adds code to write it to a file"""
    return render_template(__file__, "heredoc", {"content": content, "filename": filename})


def build_script(configurators):
    """
    Loops over configurators, calling to_script on them and then renders the script sections
    in a template.
    """

    def build_params(configurator):
        cfg = configurator.Config()
        return {"name": cfg.description, "content": cfg.to_script()}

    sections = map(build_params, configurators)
    return render_template(__file__, "install", {"sections": sections})


def input_regex(message, regex, regex_fail, **kwargs):
    """Helper method to ask the user for input and only proceed if the input matches a regex"""
    text_value = error = ""
    kwargs = kwargs if kwargs else {}
    kwargs["colors"] = True
    while not re.match(regex, text_value):
        message_with_error = f"{message}\n{ANSI_RED}{error}{ANSI_RESET}" if error else message
        code, text_value = dialog.inputbox(message_with_error, **kwargs)
        error = regex_fail

        if code != "ok":
            return None
    return text_value


def input_network(message, **kwargs):
    """Helper method to ask the user for input and only proceed if the input matches a regex"""
    net_addr = error = ""
    kwargs = kwargs if kwargs else {}
    kwargs["colors"] = True

    while True:
        try:
            message_with_error = f"{message}\n{ANSI_RED}{error}{ANSI_RESET}" if error else message
            code, net_addr = dialog.inputbox(message_with_error, **kwargs)

            if code != "ok":
                return None

            if not re.match(CIDR_REGEX, net_addr):
                raise Exception("Please enter in the format x.x.x.x/x")

            return str(IPv4Network(net_addr))
        except Exception as err:
            error = str(err)


def input_ip(message, **kwargs):
    """Helper method to ask the user for input and only proceed if the input matches a regex"""
    ip_addr = error = ""
    kwargs = kwargs if kwargs else {}
    kwargs["colors"] = True

    while True:
        try:
            message_with_error = f"{message}\n{ANSI_RED}{error}{ANSI_RESET}" if error else message
            code, ip_addr = dialog.inputbox(message_with_error, **kwargs)

            if code != "ok":
                return None

            return str(IPv4Address(ip_addr))
        except Exception as err:
            error = str(err)
