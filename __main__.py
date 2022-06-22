import subprocess
import threading
import keyboard
import pyperclip
import yaml
import pystray
from PIL import Image
from dataclasses import dataclass
from pathlib import Path

import button_box


OPTIONS_PATH = "options.yaml"


@dataclass
class Option:
    send_before: str | None
    text: str | None
    send_after: str | None
    run_program: str | None

    @staticmethod
    def build_dict(path: str):
        shortcut_dict: dict[str, dict[str, str]] = get_conf_dict(path)[
            "shortcuts"
        ]
        build = {}
        for key, val in shortcut_dict.items():
            key: str
            val: dict
            build[key] = Option(
                send_before=val.get("send_before"),
                text=val.get("text"),
                run_program=val.get("run_program"),
                send_after=val.get("send_after"),
            )
        return build


def get_conf_dict(path: str):
    with open(Path(path), "r") as f:
        return yaml.safe_load(f)


def paste(content: str):
    pyperclip.copy(content)
    keyboard.send("ctrl+v")


def run_program(path):
    subprocess.Popen(path)


def do_choice(choice: str, options: dict[str, Option]):
    try:
        chosen = options[choice]
    except KeyError as _:
        return
    if chosen.send_before:
        keyboard.send(chosen.send_before)
    if chosen.text:
        paste(chosen.text)
    if chosen.send_after:
        keyboard.send(chosen.send_after)
    if chosen.run_program:
        run_program(chosen.run_program)


def show_options_msgbox(title: str):
    try:
        options = Option.build_dict(OPTIONS_PATH)
    except Exception as exc:
        print(f"Failed to parse options, check yaml formatting: {exc}")
        return

    choice = button_box.confirm(
        text="Choose a shortcut",
        title=title,
        buttons=[opt for opt in options.keys()],
    )

    do_choice(choice, options)


def close(icon: pystray.Icon, item: pystray.MenuItem):
    _, _ = icon, item
    icon.stop()
    keyboard.unhook_all()


def hotkey_wait(title: str):
    while True:
        hotkey: str = get_conf_dict(OPTIONS_PATH)["hotkey"]
        keyboard.wait(hotkey, suppress=True)
        show_options_msgbox(title)


def main():
    title = "Quick GUI Text Entry/Program Shortcuts"
    print(title)

    icon = pystray.Icon(
        title,
        title=title,
        icon=Image.open("img/icon.png"),
        menu=pystray.Menu(pystray.MenuItem(f"Exit", action=close)),
    )
    shortcut_thread = threading.Thread(
        target=hotkey_wait, args=(title,), daemon=True
    )
    shortcut_thread.start()

    icon.run()


if __name__ == "__main__":
    main()
