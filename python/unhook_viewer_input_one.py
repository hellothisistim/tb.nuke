#-----------------------------------------------------------------------------
# trackerstablemm.py
#
# Tim BOWMAN [tim@hellothisistim.com]
#

"""
By default, Nuke will open a script with the active Viewer showing its first input, even if that wasn't the active Viewer input when you saved the script. This has a strong potential to bum you out the next time you open the script if Viewer input 1 happened to be connected to something that updates very slowly.

unhook_viewer_input_one will sort through the script immediately after Nuke loads it and disconnect the first input of every Viewer in the script. It won't touch any of the other Viewer inputs. So, if you rely on always having certain Viewer inputs connected to the same things in each script you touch, this won't mess you up. (Unless input one is one of your faves. In that case, you're going to hate this Python script.)

How to install:

Put unhook_viewer_input_one.py in your .nuke folder.
Add the following snippet to your menu.py:

### Load unhook_viewer_input_one
nuke.tprint('Importing unhook_viewer_input_one')
try:
    import unhook_viewer_input_one
except Import Error as e:
    nuke.tprint('Skipping import of unhook_viewer_input_one. Error:', e)

Happy comping!
"""
import nuke

def unhook_viewer_input_one():
	file = nuke.scriptName()
	nuke.tprint(file, "calling unhook_viewer_input_one()")
	for n in nuke.allNodes(recurseGroups=True):
		if n.Class() == "Viewer":
			nuke.tprint(file, "disconnecting input 1 on", n.fullName())
			n.setInput(0,None)

nuke.addOnScriptLoad(unhook_viewer_input_one)