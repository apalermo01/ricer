import logging
import os
import shutil
from typing import Callable

from ricer.utils.theme_data import FileAction, ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig

logger = logging.getLogger(__name__)


def tool_wrapper(tool: str):
    def func_wrapper(module: Callable):
        def inner(
            theme_data: ThemeData,
            theme_context: ThemeContext,
            user_config: UserConfig,
            install_script: str,
        ) -> ToolResult:

            tool_config = getattr(theme_data, tool)

            if tool_config.template_path:
                template_path = tool_config.template_path
            else:
                template_path = theme_context.template_path

            destination_path = os.path.join(theme_context.build_dir, tool)

            copy_files_from_template(
                os.path.join(template_path, tool), destination_path
            )

            if tool_config.append:
                copy_files_from_filelist(
                    tool_config.append,
                    theme_context.theme_path,
                    tool,
                    overwrite=False,
                )

            if tool_config.overwrite:
                copy_files_from_filelist(
                    tool_config.overwrite,
                    theme_context.theme_path,
                    tool,
                    overwrite=True,
                )

            # append and overwrite
            return module(
                theme_data=theme_data,
                theme_context=theme_context,
                user_config=user_config,
                install_script=install_script,
                destination_path=destination_path,
            )

        return inner

    return func_wrapper


def copy_files_from_template(template_path: str, build_path: str):
    """Copy files from the template folder directly into the build folder"""
    if not os.path.exists(template_path):
        raise RuntimeError(
            f"template path {template_path} does not exist. \n"
            "tip: tool name is automatically appended at the end of template path"
        )

    if not os.path.exists(build_path):
        logger.info(f"creating build folder: {build_path}")
        os.makedirs(build_path)

    # recursively walk through template folder
    logger.info(f"template path = {template_path}")

    strip_slash = lambda s: s.lstrip(os.path.sep)
    for root, _, files in os.walk(template_path):

        # /Documents/git/dotfiles/templates/i3 -> /i3
        subfolder = root.replace(template_path, "")
        # /.config/ricer/themes/theme_name/build/i3
        #                                    new ^^
        folder = os.path.join(build_path, strip_slash(subfolder))

        if not os.path.exists(folder):
            os.makedirs(folder)

        # now go through all the files in the i3 folder
        for file in files:
            src_file = os.path.join(root, strip_slash(file))
            dest_file = os.path.join(
                build_path, strip_slash(subfolder), strip_slash(file)
            )
            shutil.copy2(src_file, dest_file)
            logger.info(f"{src_file} -> {dest_file}")


def copy_files_from_filelist(
    file_list: list[FileAction], theme_path: str, tool_name: str, overwrite: bool
):
    for file_info in file_list:
        if "~" in file_info.src:
            from_path: str = os.path.expanduser(file_info.src)
        elif file_info.src.startswith("./"):
            from_path: str = file_info.src
        else:
            from_path: str = os.path.join(
                os.getcwd(), theme_path, tool_name, file_info.src
            )

        to_path: str = os.path.join(os.getcwd(), theme_path, "build", file_info.dst)

        basepath: str = "/".join(to_path.split("/")[:-1])
        if not os.path.exists(basepath):
            os.makedirs(basepath)

        if os.path.isfile(to_path) and not overwrite:
            logger.info(f"appending {from_path} to {to_path}")
            if "~" in from_path:
                from_path = os.path.expanduser(from_path)
            with open(from_path, "r") as f_from, open(to_path, "a") as f_to:
                for line in f_from.readlines():
                    f_to.write(line)
        else:
            logger.info(f"copying {from_path} to {to_path}")
            shutil.copy2(from_path, to_path)
