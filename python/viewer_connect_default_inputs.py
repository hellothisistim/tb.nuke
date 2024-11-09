#-----------------------------------------------------------------------------
# viewer_connect_default_inputs.py
#
# Tim BOWMAN [tim@hellothisistim.com]
#

"""I like to always have the same things connected to certain viewer inputs. 
But they always get disconnected accidentally. This tool re-patches them.
Call it from the tab-complete menu.
"""

import nuke

def viewer_connect_default_inputs():
    """Search the current node graph for nodes with these names and pipe 
    them to the specified input on every Viewer in the script.
    main_out: 10
    plate: 9
    current: 8
    previous: 7
    """

    plate = nuke.toNode('plate')
    previous = nuke.toNode('previous')
    current = nuke.toNode('current')
    out = nuke.toNode('main_out')

    for v in nuke.allNodes('Viewer'):
        v.setInput(9, out) # input 10 in the GUI
        v.setInput(6, previous) # input 7 in the GUI
        v.setInput(7, current) # input 8 in the GUI
        v.setInput(8, plate) # input 9 in the gui

def add_menu(target=None):
    """Add "Connect Default Viewer Inputs" option to specified target menu. If no target is
    supplied, put it in the root of the Nodes menu."""

    # Build Tracked Bezier menu
    m = nuke.menu('Nodes')
    if target is not None:
        m = target
    m.addCommand('Connect Default Viewer Inputs',
        lambda: viewer_connect_default_inputs())
