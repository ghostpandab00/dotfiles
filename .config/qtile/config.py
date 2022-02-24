
import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import qtile
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer


mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "firefox"     # My browser of choice
betterlockscreen = "betterlockscreen"

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm+" -e zsh"),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "l",
             lazy.spawn(betterlockscreen + "-l"),
             desc = "Lock screen"
             ),
         Key([mod], "w",
            lazy.spawn("rofi -show window"),
            ),
         Key([mod], "r",
            lazy.spawn("rofi -show drun"),
            ),
         Key([mod], "e",
            lazy.spawn("rofi -show emoji"),
            ),
         Key([mod], "c",
            lazy.spawn("rofi -show calc"),
            ),         
         Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='Qutebrowser'
             ),
         Key([mod], "Tab",
             lazy.screen.next_group(),
             desc='Toggle through groups'
             ),
         Key([mod], "a",
             lazy.screen.toggle_group(),
             desc='Move to last visited group'
             ),
         Key([mod], "z",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod], "q",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         ### Treetab controls
          Key([mod, "shift"], "h",
             lazy.layout.move_left(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "shift"], "l",
             lazy.layout.move_right(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         ### Screenshot controls
         Key([], "Print",
             lazy.spawn("scrot /home/vyshnavlal/Pictures/screenshots/%Y-%m-%d-%T-screenshot.png"),
             desc='Screenshot of screen'
             ),
         Key([mod], "Print",
             lazy.spawn("scrot /home/vyshnavlal/Pictures/screenshots/%Y-%m-%d-%T-screenshot.png --select --line mode=edge"),
             desc='Selected screenshot'
             ),
         Key([mod, "shift"], "Print",
             lazy.spawn("scrot /home/vyshnavlal/Pictures/screenshots/%Y-%m-%d-%T-screenshot.png --focused --border"),
             desc='Screenshot of a window'
             ),

]


##### GROUP SETTINGS #####
groups = [Group("1", label="", layout='monadtall'),
          Group("2", label="", layout='monadtall'),
          Group("3", label="", layout='monadtall'),
          Group("4", label="", layout='monadtall'),
          Group("5", label="", layout='monadtall'),
          Group("6", label="", layout='monadtall'),
          Group("7", label="", layout='floating')]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


##### LAYOUT SETTINGS #####
layout_theme = {"border_width": 1,
                "margin": 8,
                "border_focus": "2F343F",
                "border_normal": "2F343F"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.TreeTab(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]

##### COLOR SETTINGS #####
colors =    [
            ["#2F343F", "#2F343F"], # color 0  #Very dark grayish blue
            ["#A3BE8C", "#A3BE8C"], # color 1  #desaturated lime green.
            ["#EBCB8B", "#EBCB8B"], # color 2  #soft yellow
            ["#BF616A", "#BF616A"], # color 3  #bright red
            ["#B48EAD", "#B48EAD"], # color 4  #desaturated violet
            ["#88C0D0", "#88C0D0"], # color 5  #dark shade of cyan
            ["#DD0004", "#DD0004"]  # color 6  #glossy red
            ]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())    

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font = "Ubuntu",
    fontsize = 10,
    padding = 2,
    background = colors[0]
)
extension_defaults = widget_defaults.copy()


def my_window(text):
            for string in [" - Sublime", " - Firefox"]:
                text = text.replace(string, "")
            return text

##### WIDGET SETTINGS #####
def init_widgets_list():
    widgets_list = [
              
            widget.Image(
                        filename = "~/.config/qtile/icons/arch-linux-icon.png",
                        scale = "False",
                        background = colors[0],
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)},
                        margin = 3
                        ),

            widget.GroupBox(                       
                        font = "Ubuntu Bold",
                        fontsize = 16,
                        margin_y = 4,
                        margin_x = 5,
                        padding_y = 15,
                        padding_x = 1,                  
                        active = colors[1],
                        inactive = colors[4],
                        this_current_screen_border = colors[2],
                        rounded = True,
                        highlight_method = "text",
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0]                   
                        ),         
    
            widget.WindowName(
                        font = "Ubuntu",
                        fontsize = 12,
                        foreground = colors[2],
                        background = colors[0],
                        for_current_screen = True,
                        empty_group_string = "Desktop",
                        max_chars = 15,
                        parse_text = my_window
                        ),    

            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0]                   
                        ),

            widget.CurrentLayout (
                        font = "Ubuntu",
                        fontsize = 12,
                        background = colors[0],
                        foreground = colors[4] 
                        ),   

            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0],                  
                        ),    

            widget.TextBox(
                        text = "直",
                        foreground = colors[1],
                        background = colors[0],
                        padding = 2,
                        fontsize = 16,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('wifimenu')}
                        ),                                 

            widget.Net(
                        font="Ubuntu",
                        fontsize=12,
                        interface="wlp8s0",
                        format = '{down} ↓↑ {up}',
                        foreground="#75b764",
                        background=colors[0],
                        padding = 0,
                        ),
              
            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.CheckUpdates(
                        background = colors[0],
                        colour_have_updates = colors[5],
                        colour_no_updates = colors[2],
                        update_interval = 60,
                        display_format = 'Updates: {updates}', 
                        distro = 'Arch',                          
                        font="Ubuntu",    
                        fontsize=12,                   
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                        padding = 2,                        
                        no_update_string = 'No Updates',
                        ),

            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.TextBox(
                        font = "Ubuntu",
                        text = "🖴",
                        foreground = colors[3],
                        background = colors[0],
                        padding = 0,
                        fontsize = 16
                        ),

            widget.DF(
                        background = colors[0],
                        font="Ubuntu",
                        foreground = colors[3],
                        format = '{uf}{m}:{r:.0f}%',
                        visible_on_warn = False,
                        fontsize = 12,
                        padding = 5,
                        warn_color = colors[6]
                        ),

            widget.Sep(
                        linewidth = 0,
                        padding = 2,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.TextBox(
                        font = "Ubuntu",
                        text = "",
                        foreground = colors[4],
                        background = colors[0],
                        padding = 0,
                        fontsize = 16
                        ),

            widget.CPU(
                         font="Ubuntu",
                         format = '{load_percent}%',
                         update_interval = 1,
                         fontsize = 12,
                         foreground = colors[4],
                         background = colors[0],
                         ),

            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.TextBox(
                        text = "",
                        foreground = colors[1],
                        background = colors[0],
                        padding = 0,
                        fontsize = 16
                        ),

            widget.Memory(
                        font="Ubuntu",
                        format = '{MemUsed:.0f}{mm}({MemPercent}%)',
                        update_interval = 1,
                        fontsize = 12,
                        foreground = colors[1],
                        background = colors[0],
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                        ),

            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.TextBox(
                        font="Ubuntu",
                        text="",
                        foreground='#e2db49',
                        background=colors[0],
                        padding = 1,
                        fontsize=16
                        ),

            widget.Volume(
                        font="Ubuntu",
                        fontsize = 12,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.TextBox(
                        text = "",
                        foreground = colors[3],
                        background = colors[0],
                        padding = 1,
                        fontsize = 16
                        ),

            widget.Backlight (
                        backlight_name = 'intel_backlight',
                        brightness_file = '/sys/class/backlight/intel_backlight/actual_brightness',
                        max_brightness_file = '/sys/class/backlight/intel_backlight/max_brightness',
                        font = "Ubuntu",
                        fontsize = 12,
                        foreground = colors[3],
                        background = colors[0]
                        ),

            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.TextBox(
                        text = "🌤",
                        foreground = colors[2],
                        background = colors[0],
                        padding = 1,
                        fontsize = 16
                        ),


            widget.OpenWeather(
                        api_key = 'a28b13ff838772c2fbf13a3061c7f625',
                        coordinates = {"longitude": "75.477173", "latitude": "11.826900"},
                        font="Ubuntu",
                        foreground = colors[2],
                        background = colors[0],
                        fontsize = 12,
                        format = '{main_temp}°{units_temperature}',
                        ),

            widget.Sep(
                        linewidth = 0,
                        padding = 7,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.TextBox(
                        text="",
                        foreground = colors[5],
                        background = colors[0],
                        padding = 0,
                        fontsize = 14
                        ),

            widget.Clock(
                        foreground = colors[5],
                        background = colors[0],
                        fontsize = 12,
                        format = "%a %b %d %I:%M:%S %Y",
                        font = "Ubuntu"
                        ),

            widget.Sep(
                        linewidth = 0,
                        padding = 0,
                        foreground = colors[2],
                        background = colors[0]
                        ),

            widget.Systray(
                        icon_size = 16,
                        padding = 5
                        ),

            widget.TextBox(
                        text="",
                        foreground = colors[3],
                        background = colors[0],
                        padding = 5,
                        fontsize = 16,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('powermenu')}
                        ),



              ]
    return widgets_list
                  
widgets_list = init_widgets_list()



##### SCREEN SETTINGS #####
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

widgets_screen1 = init_widgets_screen1()

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.8))]

screens = init_screens()


##### MOUSE SETTINGS #####
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]


auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "Qtile"
