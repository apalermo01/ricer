ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"

if [ ! -d "$ZINIT_HOME" ]; then
    mkdir -p "$(dirname $ZINIT_HOME)"
    git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
fi

source "${ZINIT_HOME}/zinit.zsh"

zinit light zsh-users/zsh-completions
zinit light zsh-users/zsh-autosuggestions
zinit light Aloxaf/fzf-tab
zinit light zsh-users/zsh-syntax-highlighting


autoload -Uz compinit
if [ "$(date +'%j')" != "$(stat -f '%Sm' -t '%j' ~/.zcompdump 2>/dev/null)" ]; then
    compinit
else
    compinit -C
fi

zinit cdreplay -q

function y() {
	local tmp="$(mktemp -t "yazi-cwd.XXXXXX")" cwd
	yazi "$@" --cwd-file="$tmp"
	IFS= read -r -d '' cwd < "$tmp"
	[ -n "$cwd" ] && [ "$cwd" != "$PWD" ] && builtin cd -- "$cwd"
	rm -f -- "$tmp"
}

export MANPAGER="nvim +Man!"
export EDITOR="nvim"

HISTSIZE=5000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups

# keybindings
bindkey -v
bindkey '^p' history-search-backward
bindkey '^n' history-search-forward

# completion styling
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'ls --color $realpath'

if command -v z >/dev/null 2>&1
then
    zstyle ':fzf-tab:complete:__zoxide_z:*' fzf-preview 'ls --color $realpath'
fi

alias ls='ls --color'

alias vim='nvim'
alias vi='nvim'
alias nivm='nvim'
alias v='nvim'


if command -v yazi >/dev/null 2>&1
then
    alias lf="y"
    alias l="y"
    alias y="yazi"
    alias ya="y"
    alias yazi="y"
fi

if command -v bat >/dev/null 2>&1
then
    alias cat="bat --no-pager"
elif command -v batcat >/dev/null 2>&1
then
    alias cat="batcat --no-pager"
fi

if command -v eza >/dev/null 2>&1
then
    alias ls="eza"
fi

if command -v fnm >/dev/null 2>&1; then
  eval "$(fnm env --use-on-cd --shell zsh)"
fi

if command -v zoxide >/dev/null 2>&1; then
    eval "$(zoxide init zsh)"
    alias cd="z" 
fi

if command -v direnv >/dev/null 2>&1; then
    eval "$(direnv hook zsh)"
fi
