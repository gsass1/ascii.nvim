# ascii.nvim

A plugin to help spice up your text documentation, for NeoVim using the [remote plugin feature](https://pynvim.readthedocs.io/en/latest/usage/remote-plugins.html).

![Demonstration](https://user-images.githubusercontent.com/4589491/138596209-8888fb93-d5f9-4222-a58f-c4b6dda351c3.gif)

**Disclaimer:** very WIP! Expect things to break and stuff not to work flawlessly until I can release a stable version.

# Features
- [x] Boxes with variable padding
- [ ] Arrows
- [ ] Circles?
- [ ] Triangles?

# Requirements

- NeoVim
- Python3

# Installation

If you're using vim-plug:
```
Plug 'gsass1/ascii.nvim'
```

After installing execute `:UpdateRemotePlugins` to register the Python3 plugin files.

# Configuration

## Variables
Put this somewhere in your config:

```VimL
let g:ascii_default_hpadding = 1
let g:ascii_default_vpadding = 1
let g:ascii_hline_char = "-"
let g:ascii_vline_char = "|"
let g:ascii_corner_char = "+"
```

## Commands
### Box
Pput an ASCII box around a selection.

Usage: `:Box --hpadding=HPADDING --vpadding=VPADDING`

Bind it: `vnoremap <F3> :Box<CR>`
