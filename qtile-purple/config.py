# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, hook, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.dgroups import simple_key_binder
from time import sleep

import os
import subprocess
import colors

mod = "mod4"
terminal = "alacritty"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([home])




    
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
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
    Key([mod], "d", lazy.spawn("rofi -show drun -show-icons"), desc="Spawn Rofi"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in [""," "," "," "," ",""," "," ",""," " ]]
group_hotkeys = "123456789"


for g, k in zip(groups, group_hotkeys):
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                k,
                lazy.group[g.name].toscreen(),
                desc=f"Switch to group {g.name}",
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                k,
                lazy.window.togroup(g.name, switch_group=False),
                desc=f"Switch to & move focused window to group {g.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


colors = colors.qtilecustom

layout_theme = {
        "margin":14, 
        "border_width":2,
        "border_focus":colors[4],
        "border_normal":colors[0],
    }  
layouts = [
      layout.MonadTall(**layout_theme),
      layout.Max(**layout_theme),
      layout.RatioTile(**layout_theme),
      layout.MonadThreeCol(**layout_theme),
      layout.MonadWide(**layout_theme),
      layout.Spiral(**layout_theme),
      layout.Floating(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Stack(num_stacks=5),
    # layout.Matrix(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
     # Try more layouts by unleashing below layouts.
     #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
]

widget_defaults = dict(
    font="SpaceMono",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                 fontsize = 11,
                 margin_y = 5,
                 margin_x = 5,
                 padding_y = 0,
                 padding_x = 1,
                 borderwidth = 3,
                 active = colors[4],
                 inactive = "#7A808E",
                 rounded = False,
                 highlight_color = "#282738",
                 highlight_method = "line",
                 this_current_screen_border = colors[4],
                 this_screen_border = colors[4],
                 other_current_screen_border = colors[2],
                 other_screen_border = colors[5],
                 background="#282738",
                ),
                widget.Spacer(
                    length=8,
                    background='#282738', 
                ),
                widget.Image(
                    filename='~/.config/qtile/Assets/6.png',
                ),

                widget.WindowName(
                    foreground= colors [4],
                     font='JetBrains Mono Bold',
                   fontsize=11,
                 ),
                 widget.Systray(
                    background=colors[0],
                    fontsize=2,
                ),
                 widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),

                widget.TextBox(
                    text="",
                    fontsize=11,
                    padding=1,
                    background=colors[0],
                    foreground=colors[4]
                ),

                widget.Net(
                   format='{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}',
                   padding=3,
                   background=colors[0],
                   foreground=colors[4],
                   font='JetBrains Mono Bold',
                   fontsize=10
                ),
                 widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),

                widget.TextBox(
                   text="",
                   fontsize=12,
                   padding=2,    
                    #font="JetBrainsMono Nerd Font",
                   background=colors[0],
                   foreground=colors[4],
                ),
                widget.CPU(
                    format= '{load_percent}%',
                    foreground=colors[4],
                    padding=7,
                    background=colors[0],
                    font='JetBrains Mono Bold',
                    fontsize=10
                ),
                
                 widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),
                 widget.TextBox(
                    text="",
                    fontsize=12,
                    font='JetBrains Mono',
                    padding=2,
                    background=colors[0],
                    foreground=colors[4],
                ),
                widget.Memory(
                    foreground=colors[4],
                    background=colors[0],
                    #padding=4,
                    font='JetBrains Mono Bold',
                    fontsize=10
                ),
                widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),

                widget.Spacer(
                    length=8,
                    background=colors[0],
                ),


                widget.BatteryIcon(
                    theme_path='~/.config/qtile/Assets/Battery/',
                    background=colors[0],
                    scale=1,
                    margin_x=8,
                    margin_y=2
                ),


                widget.Battery(
                    font='JetBrains Mono Bold',
                    background=colors[0],
                    foreground=colors[4],
                    format='{percent:2.0%}',
                    fontsize=10,
                ),
                  widget.Image(
                    filename='~/.config/qtile/Assets/5.png',
                    background="#282738",
                ),
                
                widget.TextBox(
                    text="",
                    fontsize=11,
                    padding=3,
                    background="#282738",
                    foreground=colors[4]
                ),
            
                widget.Clock(
                    format="%a %H:%M",
                    foreground=colors[4],
                    background="#282738",
                    font="JetBrains Mono Bold",
                    fontsize=13,
                ),


                widget.Spacer(
                    length=8,
                    background='#282738',
                ),
                
            ],
            24,
            background = colors[0]
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
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
wmname = "qtile"
