# Ricer

This is a theme / rice builder for linux systems. Have you ever wanted to try different settings or colorschemes but didn't want to copy over all the other default keybindings? This is the tool for you.

# Structure

There are 5 paths to consider when setting up ricer:

- template_path: directory where everything that is common between all themes should live
- scripts_root: path to use-defined scripts
  - We need a scripts directory to hold startup / management scripts for a few tools, such as polybar
- dotfiles_path: where to store the dotfiles after being built by ricer. I suggest you point this at your dotfiles repo.
- themes_path: path to theme configurations
- wallpaper_path: where wallpapers live

# Quickstart

## Install

### Nix

add ricer.nix to you overlays

### Non-nix

Install via pipx:

`pipx install git+https://github.com/apalermo01/rices.git`

## Configuting and changing themes

See `examples/example-dotfiles-repo` for an example of how ricer expects the dotfiles repo to be set up by default.

### Setting up templates

The first thing you'll have to do is set up a folder of templates. This is where you put everything that you want to be included in all themes. For example, the template i3 config will have all your keybindings, etc EXCEPT for the colors / gaps / animations. That will be defined on a per-theme basis. The templates directory should have a structure like this:

```zsh

templates
├── dunst
│   └── dunstrc
├── i3
│   ├── config
├── kitty
│   └── kitty.conf
├── nvim
│   ├── init.lua
│   └── lua
│       └── config
│           ├── cmds.lua
│           ├── init.lua
│           └── ... anything you want 
├── okular
│   └── okularrc
├── picom
│   └── picom.conf
├── polybar
│   └── config.ini
├── rofi
│   └── config.rasi
├── tmux
│   └── tmux.conf
├── yazi
│   ├── theme.toml
│   └── yazi.toml
└── zsh
    └── .zshrc
```

### Setting up a theme

Each theme gets its own folder inside the themes directory\*. It should have a structure like this:

```zsh
theme_name
├── colors
│   └── colorscheme.json
├── fastfetch
│   └── config.jsonc
├── fish
│   └── config.fish
├── i3
│   └── config
├── kitty
│   ├── current-theme.conf
│   └── kitty.conf
├── nvim
│   └── theme.lua
├── picom
│   └── picom.conf
├── polybar
│   └── config.ini
├── rofi
│   ├── colors.rasi
│   └── config.rasi
├── scripts
│   ├── 01_installs.sh
│   └── 02_configure_theme.sh
├── theme.yaml
├── tmux
│   └── tmux.conf
└── zsh
    ├── additions.zsh
    └── p10k.zsh
```

**The most important file in this directory is `theme.yaml`**. This defines the tools that ricer sets up for you. For a full definition of what you can put in `theme.yaml`, see the \[[Theme Schema]\] section below.

Everything else in this directory are small snippets that are either appended to the template configs or completely overwrite the template configuration. For example, here is what I have in `i3/config` for my i3_dracula theme:

```

#                        border             background          text            indicator       child bdr
client.focused	         {{ green }}        {{ background }}    {{ comment }}  {{ green }}	    {{ green }}
client.focused_inactive	 {{ purple }}       {{ background }}    {{ comment }}  {{ purple }}	    {{ purple }}
client.unfocused	     {{ purple }}       {{ background }}    {{ comment }}  {{ purple }}	    {{ purple }}
client.urgent	         {{ red }}          {{ background }}    {{ comment }}  {{ red }}        {{ red }}
client.placeholder	     {{ purple }}       {{ background }}    {{ comment }}  {{ purple }}	    {{ purple }}

client.background	{{ background }}

# Gaps
gaps inner 10
gaps top 35 
new_window pixel 5
new_float normal

floating_modifier $mod

focus_follows_mouse no
```

\*you define where the themes directory is when configuring ricer.

### Running the theme switcher

run `ricer switch` to list the themes in themes_path and pick which one to apply.
running `ricer switch` will list all the directories in the designated `themes` folder. Select the theme you want and the app will build the theme following these steps:

1. Generate the theme config files in `<theme_directory>/<theme_name>/build`
1. Move the files from the build directory to the `dotfiles_path` defined in `~/.config/ricer/ricer.yaml`

Ricer will also generate a script `~/.config/install_theme.sh` which will run any additional commands necessary to install a theme.

### Post build hooks

After the theme is built, ricer will execute the scripts in the `hook_path` entry in `theme.yaml`. Here is mine as an example:

```yaml
hook_path:
  - "~/Documents/git/dotfiles/scripts/switch_theme.sh $THEME_NAME"
  - "~/Documents/git/dotfiles/scripts/switch_kb_layout.sh q"
```

My [switch_theme.sh](https://github.com/apalermo01/dotfiles/blob/main/scripts/switch_theme.sh) script calls stow to symlink the dotfiles in the built themes folder to my real ~/.config folder, then calls `~/.config/install_theme.sh` **By default, ricer does not install the themes for you, unless you set `dotfiles_path` to your home directory, which is not recommended**.

# Configuration

`ricer` generates 2 files in `~/.config/ricer`

`ricer.yml`: this defines the paths (see the structure section above) and settings for each tool.

`config_path` is the path to the tool's config relative to the home directory (e.g. i3 would be `.config/i3`). `jinja` is a boolean value stating whether or not to use a jinja template to add colors.

`ricer-global-before.yml'`: This is the default theme file. Each theme may overwrite the keys in this file. Put the options that you want common among all themes in here. For example, I define my `hood_path` entry in this file.

`ricer-global-after.yml`: Entries in this file overwrite what you define in each theme. I don't use this for anything in my own setup, but it's there in case anyone finds it useful.

# Theme Schema

**Example of a theme configuration:**

```yaml
# theme/root/example-theme/theme.yml

wallpaper:
    method: feh 
    file: wallpaper.png

colors:
    method: manual 

i3:
    append:
        - src: config 
          dst: i3/config

picom:
    template_path: $THIS_THEME

nvim:
    colorscheme: colorscheme_name
```

See `examples` to view the structure for defining a theme. All settings are defined in a theme.yml file. Any snippets that append to / overwrite template files are stored in folders named for each tool

## Available tools

## Options that are available for every tool

- append: list of files that should be appended to the template. Each entry in the list has a src (relative to \<theme_name>/\<tool_name>) and a dst (relative to the build directory). For example, with the `i3` entry above, we are appending the contents of `config` (located at `theme/root/example-theme/i3/config`) to the template config file (located at `theme/root/example-theme/build/i3/config`)
- overwrite: same logic as append, but completely overwrites the template file.
- template_path: this lets you overwrite the template config for the given tool. `$THIS_THEME` is a placeholder that will get substituted with the path to the tool files for the given theme. For example, instead of the normal template path, we're pulling all the config files for picom from `theme/root/example-theme/picom`

## Tool specific settings

To access the most up-to-date options available for each tool, see `./src/ricer/utils/theme_data.py`

- Alacritty

  - takes only options that are already available for every tool

- Apps

  - `provides`
  - `requires`
  - `name`
  - this module is still in development

- Bash

  - `feats`: list
    - Pick from: cowsay_fortune, fastfetch, run_pywal, git_onefetch
    - this is a list of commands added to .bashrc

- Colors

  - `method`: "manual" or "pywal"
    - if "manual", define your own colorscheme in `<theme_folder>/colors/colorscheme.json`
    - if "pywal", run pywal on the wallpaper. If this option is selected you MUST have an entry for wallpaper.

- Dunst

  - `font_size`: optional integer.

- Fastfetch

  - takes only options that are already available for every tool

- Fish

  - same options as bash

- Global

  - Takes only options that are already available for every tool
  - This allows you to have ~/.profile managed by ricer. The template file is `<template_path>/global/.profile`

- GTK

  - `gtk_theme`: required - name of the gtk theme to use.
  - `mode`: optional - theme mode (e.g. 'dark')
  - `gtk_install_script`: optional - name of custom script to install a theme. Must be in `<theme_path>/gtk`
  - For more details, see [gtk](#gtk).
  - You can set a gtk theme by either having ricer compile a supported theme for you or provide an install script for a theme.
  - Compile with ricer:
    - If gtk_theme is a supported theme (only `adw-gtk3` as of writing), then ricer will download the theme's source, allow you to overwrite a css or scss file, and then compile the theme. This allows you to overwrite the colors for a theme.
  - needs gsettings, gtk3, gtk4, and gsettings-desktop-schemas
  - TODO: set XDG_DATA_DIR in ~/.profile on nix
  - requirements: dart-sass, meson, ninja
  - got something togglable working in gtk:
    - 1. make a script to download a base theme
    - 2. Define overrides for the theme's css
    - 3. add GTK_THEME env var to ~/.profile

- i3

  - `font`
  - `font_size`

- kitty

  - takes only options that are already available for every tool

- Neovim

  - `colorscheme`: str or dict: name of the colorscheme to apply.
    - If a string, then colorscheme will be written to `~/.config/nvim/init.lua`
    - It is possible to specify the file that the colorcheme command gets written to by passing colorscheme as a dictionary:
    ```yml
    nvim:
        colorscheme:
            colorscheme: "name-of-your-colorscheme"
            file: "path/to/your/file.lua"
    ```
    - The file path specified here is relative to `~/.config/nvim`

- picom

  - takes only options that are already available for every tool

- polybar

  - `bars`: this is a list of the names of the individual polybar bars.

- QT

  - `method`: 'default' or 'manual'
    - If 'default', set `kv_theme` to one of the default themes [supplied by kvantum](https://github.com/tsujan/Kvantum/tree/master/Kvantum/themes/kvthemes). You may define overrides for the default theme in `<theme_dir>/qt/any-file-name.kvconfig`
    - If 'manual', fully define the kvantum config inside `<theme_dir>/qt/`. For example, setting the catppuccin theme from [this repo](https://github.com/catppuccin/kvantum) would have this structure inside `<theme_dir>/qt`

```
        .
        ├── catppuccin-mocha-yellow
        │   ├── catppuccin-mocha-yellow.kvconfig
        │   └── catppuccin-mocha-yellow.svg
        └── kvantum.kvconfig

```

    - `kv_theme`: default theme name. Required if `method` is 'default'.

- rofi

  - takes only options that are already available for every tool

- sioyek

  - takes only options that are already available for every tool

- tmux

  - takes only options that are already available for every tool

- wallpaper

- yazi

- zsh

## Other options

- font

- font_size

- hook_path

# <a name="gtk">\<\\a>GTK Themes

## Compiling a theme with ricer

Ricer provides a utility to download and compile the `adw-gtk3` theme. It will replace [\_defaults.scss](https://github.com/lassekongo83/adw-gtk3/blob/main/src/sass/_defaults.scss) with what is defined in your template. Support for additional themes are planned.

Compiling a theme requires `dart-sass`, `meson`, and `ninja` to be installed in on your system. See [adw-gtk3's depencencies](https://github.com/lassekongo83/adw-gtk3/blob/main/src/README.md#Requirements) for more details.

## Providing a custom theme install script

It is also possible to bring your own install script. Set `gtk_install_script` to the name of your installer. It must be located in `<theme_path>/gtk`. For example: `/home/username/Documents/git/dotfiles/themes/your-theme/gtk/install_gtk_theme.sh`. The contents of the build script will be appended to `~/.config/install_theme.sh`.

## Theme install script behavior

Theme install commands (compiling through ricer or executing a user-provided script) will not execute when you run `ricer switch` without additional configuration. The installation script is appended to `~/.config/install_theme.sh`. To automatically compile and install the gtk theme when running `ricer switch`, either add `~/.config/install_theme.sh` to the `hooks` array in your theme config or call `install_theme.sh` from within a script in the `hooks` array.

# Development

To test in a clean environment, I recommend setting up distrobox with the following commands

```zsh
DOTPATH="/path/to/your/dotfiles/repo"

distrobox create \
    --name test \
    --init \
    --image ubuntu:latest \
    -H ~/Documents/ricer-test \
    --volume $DOTPATH:$DOTPATH:rw

```
