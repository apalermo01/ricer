import os
from typing import Iterable
import json
from jinja2 import Template


def merge_dicts(a: dict, b: dict) -> dict:
    """Override keys in dictionary a with those in dictionary b"""
    for k in b:
        if k in a:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                a[k] = merge_dicts(a[k], b[k])
            else:
                a[k] = b[k]
        else:
            a[k] = b[k]
    return a


def overwrite_or_append_line(pattern: str, replace_text: str, dest: str):
    config_text = read_file(dest)
    new_text = []

    config_text, new_text = iterate_until_text(
        iter(config_text), new_text, pattern, append_target=False
    )
    new_text.append(f"{replace_text}\n")
    for t in config_text:
        new_text.append(t)

    write_file(new_text, dest)


def read_file(tmp_path: str) -> list:
    with open(tmp_path, "r") as f:
        lines = f.readlines()
    return lines


def write_file(text: list[str], tmp_path: str):
    with open(tmp_path, "w") as f:
        f.writelines(text)


def iterate_until_text(
    text: Iterable[str],
    new_text: list[str],
    target_text: str,
    append_target: bool = True,
) -> tuple[Iterable[str], list[str]]:
    for t in text:
        if target_text in t:
            if append_target:
                new_text.append(t)
            break
        new_text.append(t)
    return text, new_text


def append_if_not_present(text: str, dest: str):

    config_text = read_file(dest)

    text_found = False
    for line in config_text:
        if text in line:
            text_found = True

    if not text_found:
        config_text.append(text)
        write_file(config_text, dest)


def configure_colors(theme_path: str):

    colorscheme_path = os.path.join("./", theme_path, "colors", "colorscheme.json")

    if not os.path.exists(colorscheme_path):
        return

    with open(colorscheme_path, "r") as f:
        colorscheme = json.load(f)

    build_path = os.path.join(theme_path, "build")

    for root, dirs, files in os.walk(build_path):
        subfolder = root.replace(build_path, "")

        # subfolder[1:] ensures that it's not mistakenly taken for
        # an absolute path
        folder = os.path.join(build_path, subfolder[1:])

        for file in files:
            if "json" in file or "jsonc" in file or ".zsh" in file:
                continue

            full_path = os.path.join(folder, file)

            with open(full_path, "r") as f:
                template_content = f.read()

            template = Template(template_content)
            rendered = template.render(colorscheme)

            with open(full_path, "w") as f:
                f.write(rendered)


def append_text(src: str, text: str):

    with open(src, "a") as f:
        f.write(text)
