from libqtile import qtile, bar, layout, widget, extension, backend
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget import upower
from qtile_extras.widget.decorations import PowerLineDecoration
import os

mod = "mod4"
terminal = guess_terminal()

my_colors = {
    "dark": "#292A36",
    "light": "#c7f7ff",
    "blue": "#02b0d4",
    "gray": "#49494a",
    "orange": "#e87d1a",
    "red": "#cf1919",
}

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "z", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "up", lazy.layout.grow(), desc="Grow window"),
    Key([mod, "control"], "down", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod, "control"], "m", lazy.layout.maximize(),
        desc="Toogle between max and min size window"),
    Key([mod, "control"], "n", lazy.layout.reset(), desc="Reset window"),
    Key([mod], "Tab", lazy.next_screen(), desc="Toogle between screens"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "l", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "space", lazy.run_extension(extension.DmenuRun(
        dmenu_prompt=">_",
        background=my_colors["dark"],
        foreground=my_colors["light"],
        selected_background=my_colors["blue"],
        selected_foreground=my_colors["dark"],
        fontsize=12,
    )), desc="Spawn a command using a prompt widget"),
    
    # ----------- BRIGTHNESS ------------
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +1%"), desc="Increase brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 1%-"), desc="Decrease brightness"),
    
    # ----------- VOLUME -------------
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 1 --allow-boost --set-limit 150 -u"), desc="Increase volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 1 -u"), desc="Decrease volume"),
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t"), desc="Toogle mute/unmute"),
    
    # ---------- MOCP ------------
    Key([mod, "mod1"], "space", lazy.spawn("mocp -G"), desc="Toggle play/pause music player"),
    Key([mod, "mod1"], "right", lazy.spawn("mocp -f"), desc="Next song"),
    Key([mod, "mod1"], "left", lazy.spawn("mocp -r"), desc="Previous song"),
    Key([mod, "mod1"], "up", lazy.spawn("pamixer -i 1 --allow-boost --set-limit 150 -u"), desc="Increase volume"),
    Key([mod, "mod1"], "down", lazy.spawn("pamixer -d 1 -u"), desc="Decrease volume"),
    
    # ------------- LAUNCHERS ---------------
    Key([mod], "e", lazy.spawn("alacritty -e ranger")),
    Key([mod], "c", lazy.spawn("code")),
    Key([mod], "b", lazy.spawn("brave")),
    Key([mod], "t", lazy.spawn("telegram-desktop")),
    Key([mod], "m", lazy.spawn("alacritty -e mocp")),
    Key([mod, "control"], "l", lazy.spawn("slock")), #Lock Screen
    Key([mod, "control"], "s", lazy.spawn("shutdown now")), #Lock Screen
    Key([mod], "s", lazy.spawn("code .config/qtile/config.py")),
    Key([], "Print", lazy.spawn("flameshot gui")),     # Take Screenshots
]

# ------- WORKSPACES -----------
__groups = {
    1: Group("󰆍", matches=[Match(wm_class=["Alacritty"])]),
    2: Group("", matches=[Match(wm_class=["brave-browser"])]),
    3: Group("󰨞", matches=[Match(wm_class=["code"])]),
    4: Group("", matches=[Match(wm_class=["mpv"])]),
    5: Group("󱡂"),
}

groups = [__groups[i] for i in __groups]


def get_group_key(name):
    return [k for k, g in __groups.items() if g.name == name][0]


for i in groups:

    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(get_group_key(i.name)),
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(get_group_key(i.name)),
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(
                    i.name),
            )
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
        ],
    ),

# -------------- LAYOUTS --------------
layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(
        border_normal="#006276",
        border_focus="#77dbf4",
        border_width=4,
        margin=4,
        single_border_width=0,
        single_margin=0,
        max_ratio=0.75,
        min_ratio=0.25,
    ),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="ProFontIIx Nerd Font",
    fontsize=20,
    padding=4,
)
extension_defaults = widget_defaults.copy()

# -------------- SCREENS/BAR/WIDGETS -------------------
screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(),
                widget.Sep(
                    foreground=my_colors["blue"],
                    linewidth=2,
                ),
                widget.Image(
                    filename="~/.config/qtile/Arch-linux-logo-150px.png",
                    scale=True,
                    # margin=,
                    mouse_callbacks={
                        'Button1': lazy.spawn('alacritty')
                    },
                ),
                widget.Sep(
                    foreground=my_colors["blue"],
                    linewidth=2,
                ),
                widget.GroupBox(
                    highlight_method='line',
                    background=my_colors["dark"],
                    inactive=my_colors["gray"],
                    block_highlight_text_color=my_colors["blue"],
                    rounded=True,
                ),
                widget.Sep(
                    foreground=my_colors["blue"],
                    linewidth=2,
                ),
                # widget.Prompt(),
                widget.WindowName(
                    format='{state}{name}',
                    padding=10,
                    fontsize=13,
                    background=my_colors["dark"],
                    foreground=my_colors["light"],
                ),

                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.TextBox(
                    background=my_colors["dark"],
                    foreground=my_colors["blue"],
                    decorations=[
                        PowerLineDecoration(path="arrow_right"),
                    ],
                ),
                widget.Net(
                    background=my_colors["dark"],
                    foreground=my_colors["blue"],
                    format='{down}   {up}',
                    fontsize=13,
                    decorations=[
                        PowerLineDecoration(path="arrow_right"),
                    ],
                ),
                widget.TextBox(
                    text='󰍛',
                    background=my_colors["blue"],
                    foreground=my_colors["dark"],
                    fontsize=20,
                ),
                widget.Memory(
                    background=my_colors["blue"],
                    foreground=my_colors["dark"],
                    fontsize=13,
                    format='{MemUsed: .0f}{mm}',
                    decorations=[
                        PowerLineDecoration(path="arrow_right"),
                    ],
                ),
                widget.TextBox(
                    text='󰻠',
                    background=my_colors["dark"],
                    foreground=my_colors["blue"],
                    fontsize=20,
                ),
                widget.CPU(
                    background=my_colors["dark"],
                    foreground=my_colors["blue"],
                    format='{load_percent}%',
                    fontsize=13,
                    decorations=[
                        PowerLineDecoration(path="arrow_right"),
                    ],
                ),
                widget.TextBox(
                    text='󱩅',
                    background=my_colors["blue"],
                    foreground=my_colors["dark"],
                    fontsize=18,
                ),
                widget.ThermalSensor(
                    background=my_colors["blue"],
                    foreground=my_colors["dark"],
                    fontsize=13,
                    decorations=[
                        PowerLineDecoration(path="arrow_right"),
                    ],
                    format='{temp:.1f}{unit}'
                ),
                widget.TextBox(
                    text='',
                    background=my_colors["dark"],
                    foreground=my_colors["blue"],
                    fontsize=18,
                ),
                widget.Volume(
                    foreground=my_colors["blue"],
                    fmt='{}',
                    fontsize=13,
                    decorations=[
                        PowerLineDecoration(path="arrow_right"),
                    ],
                ),
                widget.TextBox(
                    text='󰃠',
                    background=my_colors["blue"],
                    foreground=my_colors["dark"],
                    fontsize=18,
                ),
                widget.Backlight(
                    brightness_file="/sys/class/backlight/amdgpu_bl0/actual_brightness",
                    max_brightness_file="/sys/class/backlight/amdgpu_bl0/max_brightness",
                    format='{percent:2.0%}',
                    background=my_colors["blue"],
                    foreground=my_colors["dark"],
                    fontsize=13,
                    decorations=[
                        PowerLineDecoration(path="arrow_right"),
                    ],
                ),
                widget.UPowerWidget(
                    battery_height=11,
                    battery_width=18,
                    fill_low=my_colors["orange"],
                    fill_critical=my_colors["red"],
                    fill_normal=my_colors["blue"],
                    border_charge_colour=my_colors["blue"],
                    fontsize=13,
                    foreground=my_colors["blue"],
                ),
                widget.Battery(
                    notify_below=20,
                    format='{percent:2.0%}',
                    discharge_char='',
                    full_char='',
                    charge_char='',
                    low_foreground=my_colors["orange"],
                    low_percentage=0.2,
                    background=my_colors["dark"],
                    foreground=my_colors["blue"],
                    fontsize=13,
                    decorations=[
                        PowerLineDecoration(path="arrow_right"),
                    ],
                ),
                widget.Clock(
                    format=" %a,%d-%m-%Y  %I:%M %p",
                    background=my_colors["blue"],
                    foreground=my_colors["dark"],
                    fontsize=14,
                    decorations=[
                        PowerLineDecoration(path="arrow_right"),
                    ],
                ),
                widget.Systray(
                    icon_size=20,
                    background=my_colors["dark"],
                    padding=0,
                ),
            ],
            22,
            background=my_colors["dark"],
            opacity=1,
        ),
    ),
    Screen(),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
