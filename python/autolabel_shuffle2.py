#-----------------------------------------------------------------------------
# autolabel_shuffle2.py
#
# Tim BOWMAN [tim@hellothisistim.com]
#

"""Label Shuffle2 nodes with mapping info in certain cases.

"""

import nuke
from pprint import pprint

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
		print('inputs_in_mappings', inputs_in_mappings(node))
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

		return label


nuke.addAutolabel(autolabel_shuffle2)

