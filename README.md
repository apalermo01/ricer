# Ricer

This is a theme / rice builder for linux systems. Have you ever wanted to try different settings or colorschemes but didn't want to copy over all the other default keybindings? This is the tool for you.

# Structure

There are 5 paths to consider when setting up ricer:

- template_path: directory where everything that is common between all themes should live 
- scripts_root: path to use-defined scripts
    - TODO: do we need this?
- dotfiles_path: where to store the dotfiles after being built by ricer. I suggest you point this at your dotfiles repo.
- themes_path: path to theme configurations
- wallpaper_path: where wallpapers live

# Quickstart 

## Nix
add ricer.nix to you overlays

## Non-nix
install via pip (WIP)

## Changing themes 
run `ricer switch` to list the themes in themes_path and pick which one to apply.

# Configuration

`ricer` generates 2 files in `~/.config/ricer`

`ricer.yml`: this defines the paths (see the structure section above) and settings for each tool.
`config_path` is the path to the tool's config relative to the home directory (e.g. i3 would be `.config/i3`). `jinja` is a boolean value stating whether or not to use a jinja template to add colors.

`ricer-global.yml'`: this is a file that overrides all settings for any theme. This is particularly useful for quickly trying out new settings without updating every theme.

# Defining a theme

See `examples` to view the structure for defining a theme. All settings are defined in a theme.yml file. Any snippets that append to / overwrite template files are stored in folders named for each tool


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
 

These are the options available for **all tools**

- append: list of files that should be appended to the template. Each entry in the list has a src (relative to <theme_name>/<tool_name>) and a dst (relative to the build directory). For example, with the `i3` entry above, we are appending the contents of `config` (located at `theme/root/example-theme/i3/config`) to the template config file (located at `theme/root/example-theme/build/i3/config`)
- overwrite: same logic as append, but completely overwrites the template file.
- template_path: this lets you overwrite the template config for the given tool. `$THIS_THEME` is a placeholder that will get substituted with the path to the tool files for the given theme. For example, instead of the normal template path, we're pulling all the config files for picom from `theme/root/example-theme/picom`

**Tool specific settings**
To quickly access the additional settings available for each tool, see the tool modules in `src/ricer/tools` - each file has a TypedDict that extends the base configuration options with the additional settings that are available.


