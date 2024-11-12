#-----------------------------------------------------------------------------
# shuffle2_tools.py
#
# Tim BOWMAN [tim@hellothisistim.com]
#

"""Some tools that help with creating common Shuffle2 patches, and also an 
autolabel script that helps to see what's happening in Shuffle2 without 
opening the control panel.

The autolabel displays simple shuffles completely and provides useful 
indicators for complex or non-standard ones.

If a single channel is shuffled into all output channels, display that channel as "layer.name".

For all other situations, use Shake notation with a single character for each output channel in order. For example, a standard pass-through is notated as "rgba", putting black in the alpha becomes "rgb0". Any input channel names that are a single character get used as is (eg. "uv00" to shuffle UV components into red and green.) Input channel names with more than one character are all represented with an "X", indicating that you'd better open the Shuffle's panel and have a look for the specifics.

If input layers other than "rgba" or "rgb" are used, put the list of active input layers in parenthesis and add it to the beginning of the label.

Likewise with output layers, but put them at the end of the label.

If any input other than B is used, add the active input letters to the beginning of the label.

Examples:
	"rgba.red" = Shuffle red into all channels.
	"rgb1" = Keep red, green, and blue. Put white in the alpha.
	"(depth,rgba)rgbZ" = Keep red, green, and blue. Put depth into the alpha.
	"AB:(roto,diffuse)ZXXrb(mattes)" = Someone has done something complicated. 
"""

import nuke

def layers_in_mappings(mappings, input=True, output=True):
	"""Return a list of all the layers connected in the specified inputs and/or outputs."""
	dir = []
	if input:
		dir.append(1)
	if output:
		dir.append(2)
	layers = []
	for d in dir:
		for chan in mappings: 
			if '.' in chan[d]:
				layer = chan[d].split('.')[0]
				if layer not in layers:
					layers.append(layer)
	return layers

def channels_in_mappings(mappings, input=True, output=True, fullnames=True):
	"""Return a list of all the channels connected in the specified inputs and/or outputs."""
	dir = []
	if input:
		dir.append(1)
	if output:
		dir.append(2)
	chans = []
	for d in dir:
		for chan in mappings:
			input = chan[d]
			if not fullnames:
				if '.' in input:
					input = input.split('.')[1]
			if input not in chans:
				chans.append(input)
	return chans

def inputs_in_mappings(node):
	"""Return a list of the input names (eg. "A" and "B") used in all patched connections."""
	mappings = node['mappings'].getValue()
	inputs = []
	for chan in mappings:
		if chan[0] == 0:
			if node['fromInput1'].getValue() == 0:
				inputs.append('B')
			else:
				inputs.append('A')
		if chan[0] == 1:
			if node['fromInput2'].getValue() == 0:
				inputs.append('B')
			else:
				inputs.append('A')
	## eliminate duplicates
	inputs = list(dict.fromkeys(inputs))	
	return sorted(inputs)

def to_shake(mappings):
	"""Return Shake-style shuffle string for a given mapping. Red, green, blue, alpha, black, and white will be translated to rgba01. Any single-letter channel name will be used directly. Any multi-letter channel names will be replaced by X."""

	shuff = ''
	for chan in mappings:
		c = chan[1]
		if c == 'black':
			shuff += '0'
		elif c == 'white':
			shuff += '1'
		elif c.split('.')[1] in ['red', 'green', 'blue', 'alpha']:
			shuff += chan[1].split('.')[1][0]
		elif len(c.split('.')[1]) == 1:
			shuff += c.split('.')[1]
		else:
			shuff += 'X'
	# print('shuff:', shuff)
	return shuff

def mappings_channels_rgba01(mappings):
	"""Does this mapping only address channels that are red, green, blue, alpha, black, or white?"""
	for c in channels_in_mappings(mappings, fullnames=False):
		if c not in ["red", "green", "blue", "alpha", "black", "white"]:
			return False
	return True

def autolabel_shuffle2():

	node = nuke.thisNode()
	if node.Class() == 'Shuffle2':
		mappings = node['mappings'].getValue()
		in_layers = ''
		out_layers = ''
		inputs = ''
		label = ''

		# If one channel in the source layer is connected to all of the output channels, use the source layer and channel name.
		chans = channels_in_mappings(mappings, input=True, output=False, fullnames=True)
		if len(chans) == 1 and len(inputs_in_mappings(node)) == 1:
			label = chans[0]
		else:
			# Use Shake-style notation for all patched connections.
			label = to_shake(mappings)

			# If the input layer is not "rgba" or there are more than one active input layers, add the input layer(s') name(s) to the front.
			rgba_only = True
			layers = layers_in_mappings(mappings, input=True, output=False)
			for layer in layers:
				if layer not in  ['rgba', 'rgb']:
					rgba_only = False
			if not rgba_only:
				in_layers = '(' + ','.join(layers) + ')'

			# If the output  layer is not "rgba", or there are more than one active input layers, add the output layer(s') name(s) to the end.
			rgba_only = True
			layers = layers_in_mappings(mappings, input=False, output=True)
			for layer in layers:
				if layer not in  ['rgba', 'rgb']:
					rgba_only = False
			if not rgba_only:
				out_layers = '(' + ','.join(layers) + ')'

		# Look for A inputs
		if inputs_in_mappings(node) != ['B']:
			inputs = ''.join(inputs_in_mappings(node))

		if in_layers != '':
			label = in_layers + label
		if out_layers != '':
			label += out_layers
		if inputs != '':
			label = inputs + ':' + label

		label = node.name() + '\n' + label
		if node['label'].getValue() != '':
			label += '\n' + node['label'].getValue()

		# -------------------------------------------------------------------
		# *** The following is quoted directly from Foundry's autolabel.py, 
		# which lives in the Nuke version's plugins folder.

		# do the icons:
		ind = nuke.expression("(keys?1:0)+(has_expression?2:0)+(clones?8:0)+(viewsplit?32:0)")

		if int(nuke.numvalue("maskChannelInput", 0)) :
			ind += 4
		if int(nuke.numvalue("this.mix", 1)) < 1:
			ind += 16
		nuke.knob("this.indicators", str(ind))

		# *** End of quote.
		# -------------------------------------------------------------------

		return label


def make_shuffle2_reorder(order='rgba'):
	"""Create a new-style Shuffle2 that's patched according to a Shake-style sequence of letters and numbers.

	'order' should be a four-character string containing something sensible
	like 'rgb1' or 'rrrr' or '0000'"""

	# Reality-check
	try:
		assert len(order) == 4
		for letter in order:
			assert letter in 'rgba01'
	except:
		nuke.message("Please use a four-character sequence, consisting of r, g, b, a, 1, and 0.")
		return

	char_to_chan = {'r': 'rgba.red',
					   'g': 'rgba.green',
					   'b': 'rgba.blue',
					   'a': 'rgba.alpha',
					   '0': 'black',
					   '1': 'white' }
	channels = ['rgba.red', 'rgba.green', 'rgba.blue', 'rgba.alpha']
	n = nuke.createNode('Shuffle2', inpanel=False)
	map = n.knob('mappings')
	for num, chan in enumerate(order[0:4]):
		#print(num, chan)
		if chan in '01':
			map.setValue(-1, char_to_chan[chan], channels[num])
		else:
			map.setValue(0, char_to_chan[chan], channels[num])




nuke.addAutolabel(autolabel_shuffle2)



def add_menu(target=None):
	"""Add "Connect Default Viewer Inputs" option to specified target menu. If no target is
	supplied, put it in the root of the Nodes menu."""

	# Build Tracked Bezier menu
	m = nuke.menu('Nodes')
	if target is not None:
		m = target
	tm = m.addMenu('Shuffle2 Tools')
	tm.addCommand('RGBA', "shuffle2_tools.make_shuffle2_reorder('rgba')")
	tm.addCommand('RGB1', "shuffle2_tools.make_shuffle2_reorder('rgb1')")
	tm.addCommand('RGB0', "shuffle2_tools.make_shuffle2_reorder('rgb0')")
	tm.addCommand('RRRR', "shuffle2_tools.make_shuffle2_reorder('rrrr')")
	tm.addCommand('GGGG', "shuffle2_tools.make_shuffle2_reorder('gggg')")
	tm.addCommand('BBBB', "shuffle2_tools.make_shuffle2_reorder('bbbb')")
	tm.addCommand('AAAA', "shuffle2_tools.make_shuffle2_reorder('aaaa')")
	tm.addCommand('1111', "shuffle2_tools.make_shuffle2_reorder('1111')")
	tm.addCommand('0000', "shuffle2_tools.make_shuffle2_reorder('0000')")
