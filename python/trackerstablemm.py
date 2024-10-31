#-----------------------------------------------------------------------------
# trackerstablemm.py
#
# Tim BOWMAN [tim@hellothisistim.com]
#

"""Create expression-linked stabilize and matchmove Transforms from a Tracker
in one step.

When I'm setting up a Tracker, I like to keep the transform set to 'none' Any
time I set it to something else it always causes me problems later. But, to
check if my track is working, I need to see the stablilized thing I'm tracking.
Expression-linked stabilize to the rescue! And if you have the stabilize
working, you know the matchmove is working. A two-fer, woo! And if the
matchmoved stable plate matches the plate, you know they're inverting each
other correctly.

If you plan ahead and name your Tracker something like 'Tracker_shoe', you'll
get a stabilize named 'stable_shoe' and a matchmove named 'mm_shoe'. Otherwise
you're stuck with the Tracker's name and you'll have to change it manually.
Manual sucks. Plan ahead.
"""

import nuke

def trackerstablemm(node):

    error_message = "Please select a Tracker."

    if node.Class() != "Tracker4":
        nuke.message(error_message)
        return

    track = node
    cpo = track['cornerPinOptions']
    ccp = track['createCornerPin']

    #help(cpo)
    #print(cpo.values())

    # Make that stabilise.
    cpo.setValue('Transform (stabilize)')
    ccp.execute()

    # Find that node we just made.
    all = nuke.allNodes('Transform')
    # Name starts with 'Transform_Stabilize'
    trans = [node for node in all if node.name().startswith('Transform_Stabilize')]
    # Not connected to anything
    noconnect = [node for node in trans if node.inputs() == 0]
    # Take the highest numbered node
    sort_names = sorted([node.name() for node in noconnect])
    stable = nuke.toNode(sort_names[-1])

    stable.setInput(0, track)
    stable['shutteroffset'].setValue('centered')

    # Well done. Now make that matchmove.
    cpo.setValue('Transform (match-move)')
    ccp.execute()

    # Find that node we just made.
    all = nuke.allNodes('Transform')
    # Name starts with 'Transform_MatchMove'
    trans = [node for node in all if node.name().startswith('Transform_MatchMove')]
    # Not connected to anything
    noconnect = [node for node in trans if node.inputs() == 0]
    # Take the highest numbered node
    sort_names = sorted([node.name() for node in noconnect])
    mm = nuke.toNode(sort_names[-1])

    # Name them
    name = track.name()
    if '_' in name:
        name = name.split('_')[-1]
    stable.setName('stable_' + name)
    mm.setName('mm_' + name)

    mm.setInput(0, stable)
    mm['shutteroffset'].setValue('centered')

    # Arrange neatly
    stable.autoplace()
    mm.autoplace()

    # Set the Tracker transform mode to "none" because sometimes I forget to do that
    track['transform'].setValue('none')



def add_menu(target=None):
    """Add "Tracker Stable MM" option to specified target menu. If no target is
    supplied, put it in the root of the Nodes menu."""

    # Build Tracked Bezier menu
    m = nuke.menu('Nodes')
    if target is not None:
        m = target
    m.addCommand('Tracker Stable MM',
        lambda: trackerstablemm(nuke.selectedNode()))
