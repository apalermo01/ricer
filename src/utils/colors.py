import os
import json
from jinja2 import Template
import logging

from src.utils.types import UserConfig
logger = logging.getLogger(__name__)

def configure_colors(theme_path: str, user_config: UserConfig):
    logger.info("configuring jinja templates for colorschemes")
    colorscheme_path = os.path.join(theme_path, "colors", "colorscheme.json")

    if not os.path.exists(colorscheme_path):
        logger.error(f"{colorscheme_path} not found!")
        return

    with open(colorscheme_path, "r") as f:
        colorscheme = json.load(f)

    build_path = os.path.join(theme_path, "build")
    logger.info(f"build path = {build_path}")
    for tool in os.listdir(build_path):
        tool_path = os.path.join(build_path, tool)
        if not user_config['tools'][tool].get('jinja'):
            continue
        logger.info(f"applying jinja template for {tool}")
        for root, dirs, files in os.walk(tool_path):
            subfolder = root.replace(build_path, "")

            # subfolder[1:] ensures that it's not mistakenly taken for
            # an absolute path
            folder = os.path.join(build_path, subfolder[1:])

            for file in files:
                if "json" in file or "jsonc" in file:
                    continue
                full_path = os.path.join(folder, file)
                logger.info(f"running jinja on {full_path}")
                with open(full_path, "r") as f:
                    template_content = f.read()

                template = Template(template_content)
                rendered = template.render(colorscheme)

                with open(full_path, "w") as f:
                    f.write(rendered)
