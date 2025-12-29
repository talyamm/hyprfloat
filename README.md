# Hyprfloat

[Hyprfloat](https://github.com/nevimmu/hyprfloat) didnt work for me, so i wrote my own version of it

### Clone the repo

```bash
git clone https://github.com/talyamm/hyprfloat
mv hyprfloat ~/.local/share/bin
```

### Then add it to autostart

```bash
exec-once = python ~/.local/share/bin/hyprfloat/hyprfloat.py &
```

## Config example

```bash
{
  "window_classes": ["Alacritty"],
  "float_size": {
    "width": 1200,
    "height": 800
  }
}
```

( whole thing uses about 14MB btw)