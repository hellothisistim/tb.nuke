#-----------------------------------------------------------------------------
# color_change.py
#
# Tim BOWMAN [tim@hellothisistim.com]
#

"""Sometimes it's handy to be able to color certain nodes in a script. Maybe
it means, "these are the ones I touched," or, "this is important." Or maybe 
you're building a setup to hand off to someone else and those colors mean, 
"these are the one's you'll have to tweak for your shot."

Whatever the reason, this is the tool for it.

Special thanks to Spencer Hecox from whom I stole this great idea.
"""

import nuke

colors = {
	'blue': 727646207,
	'cyan': 653328383,
	'green': 335484159,
	'grey': 2593823487,
	'magenta': 4279756287,
	'orange': 4285202687,
	'pink': 4285575167,
	'red': 4280487167,
	'yellow': 4294902015,
	}

def node_color_to_default(nodes):
	"""Return node color to default for provided nodes."""
	for n in nodes:
		n['tile_color'].setValue(nuke.defaultNodeColor(n.Class()))

def node_color(nodes, color):
	"""Set the specified color on provided nodes."""
	for n in nodes:
		n['tile_color'].setValue(colors[color])
		print(color, colors[color])

def green_to_orange(nodes):
	"""If any of the provided nodes are green (as in, this module's specific 
	green), change them to orange. If no nodes have been provided, change all 
	nodes in the script.
	"""
	if len(nodes) == 0:
		nodes = nuke.allNodes()
	for n in nodes:
		if n['tile_color'].getValue() == colors['green']:
			n['tile_color'].setValue(colors['orange'])

def help():
	help = """"cc_colorName" changes the color of any selected node.

Available colors:
	"""
	help += '\n    '.join(sorted(colors.keys()))
	help += """

Color meanings:
	orange = This is at default value, but will need to be adjusted.
	green = This has been adjusted for this shot.
	yellow = This needs attention.

"cc_default" = Return to the node's default color.

"cc_greenToOrange" = Set all greens back to orange. This is used when copying used setups into new shots.

"cc_help" = Display this help message.
	"""

	nuke.message(help)


def add_menu(target=None):
	"""Add "Color Change" options to specified target menu. If no target is
	supplied, put it in the root of the Nodes menu."""

	m = nuke.menu('Nodes')
	if target is not None:
		m = target
	m.addCommand('cc Blue', lambda: node_color(nuke.selectedNodes(), 'blue'))
	m.addCommand('cc Cyan', lambda: node_color(nuke.selectedNodes(), 'cyan'))
	m.addCommand('cc Green', lambda: node_color(nuke.selectedNodes(), 'green'))
	m.addCommand('cc Grey', lambda: node_color(nuke.selectedNodes(), 'grey'))
	m.addCommand('cc Magenta', lambda: node_color(nuke.selectedNodes(), 'magenta'))
	m.addCommand('cc Orange', lambda: node_color(nuke.selectedNodes(), 'orange'))
	m.addCommand('cc Pink', lambda: node_color(nuke.selectedNodes(), 'pink'))
	m.addCommand('cc Red', lambda: node_color(nuke.selectedNodes(), 'red'))
	m.addCommand('cc Yellow', lambda: node_color(nuke.selectedNodes(), 'yellow'))
	m.addCommand('cc Default', lambda: node_color_to_default(nuke.selectedNodes()))
	m.addCommand('cc Green to Orange', lambda: green_to_orange(nuke.selectedNodes()))
	m.addCommand('cc Help', lambda: help())

