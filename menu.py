# ~/.nuke/menu.py
nuke.tprint('START: '+ os.path.realpath(__file__))





##
## Methods
##

# Find Knobs With Expressions
def findKnobsWithExpressions():
    out = []
    for n in nuke.allNodes(recurseGroups=True):
        for k in n.knobs():
            knob = n.knob(k)
            if knob.hasExpression():
                knobinfo = knob.toScript() + '\t' + n.fullName() + '\t' + knob.name()
                out.append(knobinfo)

    formatted_out = "\n".join(sorted(out))
    print(formatted_out)

    nuke.message(formatted_out)


# Read: local caching
def setReadCache(mode='always'):
    """Switch any selected read's local cahing to the specified mode. If no
    read nodes are selected, switch all the read nodes."""
    nodes = nuke.selectedNodes('Read')
    if len(nodes) == 0:
        nodes = nuke.allNodes('Read')
    for n in nodes:
        if mode in n.knob('cacheLocal').values():
            n.knob('cacheLocal').setValue(mode)

# AOV Merge
def aovMerge():
    aovs = nuke.selectedNodes()
    m = nuke.createNode('Merge2', "Achannels none Bchannels none output none also_merge all", inpanel=False)
    m.setName('MergeAOVs')



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
    n.knob('label').setValue(order)

# TODO: Also make a labeling callback for Shuffle2 reorders.

# AutoBackdrop
def tb_autobackdrop():
    '''
    Automatically puts a backdrop behind the selected nodes.

    The backdrop will be just big enough to fit all the select nodes in, with room
    at the top for some text in a large font.
    '''

    selNodes = nuke.selectedNodes()


    if not selNodes:
        return nuke.nodes.BackdropNode(note_font_size = int(nuke.knobDefault("BackdropNode.note_font_size")),
                                       note_font = nuke.knobDefault("BackdropNode.note_font"),
                                       note_font_color = nuke.knobDefault("BackdropNode.note_font_color"),
                                       )

    # Calculate bounds for the backdrop node.
    bdX = min([node.xpos() for node in selNodes])
    bdY = min([node.ypos() for node in selNodes])
    bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
    bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY

    # Expand the bounds to leave a little border. Elements are offsets for
    # left, top, right and bottom edges respectively
    left, top, right, bottom = (-32, -140, 32, 32)
    bdX += left
    bdY += top
    bdW += (right - left)
    bdH += (bottom - top)

    n = nuke.nodes.BackdropNode(xpos = bdX,
                                bdwidth = bdW,
                                ypos = bdY,
                                bdheight = bdH,
                                note_font_size = int(nuke.knobDefault("BackdropNode.note_font_size")),
                                note_font = nuke.knobDefault("BackdropNode.note_font"),
                                note_font_color = nuke.knobDefault("BackdropNode.note_font_color"),
                                )
    # revert to previous selection
    n['selected'].setValue(False)
    for node in selNodes:
        node['selected'].setValue(True)

    return n




# Remove Proxy from Reads
def removeProxyFromReads(nodes=nuke.selectedNodes()):
    """Clear the proxy field on all selected read nodes."""

    assert type(nodes) == list

    # Filter out non-read nodes.
    nodes = [node for node in nodes if node.Class() == 'Read']

    for node in nodes:
        node.knob('proxy').setValue('')
        # Force refresh
        node.forceValidate()

# Edit Label
def editLabel():
    """Pop up a dialog allowing the user to edit the contents of the selected node's label."""

    # selectedNodes() is much easier to work with than selectedNode()
    nodes = nuke.selectedNodes()

    if len(nodes) < 1:
        return
    elif len(nodes) > 1:
        nuke.message('Edit Label: Too many nodes selected. One at a time, please.')
        return

    node = nodes[0]
    label = node.knob('label')
    contents = label.value()
    new_contents = nuke.getInput('Edit label', contents)
    if new_contents is None:
        return
    if contents != new_contents:
        label.setValue(new_contents)


# Smart Roto
def smartBezier():
    """If a node with some transform data (for example a Tracker or
    Transform node with translate, rotate, scale, and center knobs)
    is selected when this method is called, a bezier will be created with
    it's transform tab bits expression-linked to the transform node.
    Otherwise, a regular bezier will be created.

    Deprecated.

    """

    # TODO: Oh, bother... I really should be deselecting all the selected
    # nodes before I make the expression-linked bezier. But not before I
    # make a regular one.

    nodes = nuke.selectedNodes()
    # Remove nodes that aren't linkable
    nodes = [node for node in nodes if nodeHasTransformKnobs(node)]
    # No link nodes selected?
    if len(nodes) < 1:
        nuke.createNode('Bezier')
        return

    node = nodes[-1]

    trackedBezier(node)



# Frame Range to Viewer
def frameRangeToViewer(node=None):
    """Set the custom frame range for all viewers to match the frame range
    at the selected node.

    Returns None
    """

    if node is None:
        try:
            node = nuke.selectedNode()
        except ValueError:
            node = nuke.root()
    first = node.firstFrame()
    last = node.lastFrame()

    print(first, last)

    viewers = nuke.allNodes('Viewer')
    for viewer in viewers:
        viewer.knob('frame_range').setValue(str(first) + '-' + str(last))
        viewer.knob('frame_range_lock').setValue(True)


# Self-Labeling Dot
def selfLabellingDot(name=None):
    dot = nuke.createNode('Dot', inpanel=False)
    dot['label'].setValue('[value name]')
    if name:
        dot.setName(name)
    return dot

# Labeled Dot Organizer
def labledDotOrganizer():
    items = ['Previous version', 'Plate', 'Last to client', 'Layout', 'Animation', 'Light', 'FX', 'Edit ref']
    for i in items:
        selfLabellingDot(i)
    # TODO: fancy placement at bottom of script, below lowest write node.

# Run AutoCrop
# Special thanks to Jack Hughes [https://magicbeansvfx.wordpress.com/2015/07/27/nukes-hidden-autocrop-script/]
def runAutoCrop():
    nukescripts.autocrop(first=None, last=None, inc=None, layer="rgba")


# Reset viewer gain and gamma controls
# Sourced from: https://www.hiramgifford.com/nuke-tools-and-scripts/nuke-python-code-snippets Many thanks!
def reset_viewers_gain_gamma():
    for node in nuke.allNodes():
        if node.Class() == 'Viewer':
            node.knob('gain').setValue(1)
            node.knob('gamma').setValue(1)

# Apply my default labels
def apply_default_label(nodes, append=False):
    """Applies the current default label text to all selected nodes. 
    Will replace any existing label by default! Use 'append=True' to 
    place the default label text after any existing label text."""
    for node in nodes:
        label_text = nuke.knobDefault(node.Class()+'.label')
        if append:
            label_text = node.knob('label').getValue() + '\n' + label_text
        node.knob('label').setValue(label_text)

# Sort inputs, by Hugh Macdonald
# https://discord.com/channels/1207369533254406247/1239977318580092959/1239977318580092959
def sort_inputs():
    """Useful for nodes like ContactSheet where you might have multiple 
    inputs. If you have a load of nodes to connect in, and a disconnected 
    ContactSheet node, and connect them all at once using "y", the inputs 
    often end up in a relatively arbitrary order.

    Selecting the ContactSheet node and running this code will re-order 
    the inputs based on the x position of the input node."""

    n = nuke.selectedNode()
    n.inputs()
    input_nodes = [n.input(i) for i in range(n.inputs())]
    input_nodes.sort(key = lambda a: a['xpos'].getValue())
    for i, input_node in enumerate(input_nodes):
        n.setInput(i, input_node)

# Multi paste, by Hugh Macdonald
# # https://discord.com/channels/1207369533254406247/1239977318580092959/1239977318580092959
def multi_paste():
    """Paste the same nodes under a number of other nodes. You could copy 
    and then select, paste, select, paste, select, paste, etc, but that's 
    painful.

    This scriptlet will allow you to select all of the nodes you want to 
    paste under, and then have it do this all in one go."""
    
    nodes = nuke.selectedNodes()
    for n in nodes:
        for selected in nuke.selectedNodes():
            selected["selected"].setValue(False)
        n["selected"].setValue(True)
        nuke.nodePaste("%clipboard%")
    for selected in nuke.selectedNodes():
        selected["selected"].setValue(False)


##
## Main
##

m = nuke.menu('Nodes')
user = 'tim'
icon = 'T-icon.png'
nuke.tprint('Adding "tim" menu.')
tm = m.addMenu(user, icon)


# Expression Reorder
tm.addCommand('RGBA', "make_shuffle2_reorder('rgba')")
tm.addCommand('RGB1', "make_shuffle2_reorder('rgb1')")
tm.addCommand('RGB0', "make_shuffle2_reorder('rgb0')")
tm.addCommand('RRRR', "make_shuffle2_reorder('rrrr')")
tm.addCommand('GGGG', "make_shuffle2_reorder('gggg')")
tm.addCommand('BBBB', "make_shuffle2_reorder('bbbb')")
tm.addCommand('AAAA', "make_shuffle2_reorder('aaaa')")
tm.addCommand('1111', "make_shuffle2_reorder('1111')")
tm.addCommand('0000', "make_shuffle2_reorder('0000')")
# Read: local caching (obsolete in Nuke10!)
if nuke.env['NukeVersionMajor'] <= 9:
	for mode in nuke.nodes.Read().knob('cacheLocal').values():
		tm.addCommand('Read: cache '+ mode, "setReadCache('"+mode+"')")
# AOV Merge
tm.addCommand('AOVMerge', "aovMerge()")

#tm.addCommand('findKnobsWithExpressions', lambda: findKnobsWithExpressions())
tm.addCommand('Remove proxy from Reads',
    lambda: removeProxyFromReads(nuke.selectedNodes()))
tm.addCommand('Frame Range to Viewer', lambda: frameRangeToViewer())
tm.addCommand('Labeled Dot Organizer', lambda: labledDotOrganizer())
tm.addCommand('AutoCrop', lambda: runAutoCrop())
tm.addCommand('Apply Default Label', lambda:apply_default_label(nuke.selectedNodes()))
tm.addCommand('Append Default Label', lambda:apply_default_label(nuke.selectedNodes(), append=True))
tm.addCommand('Sort Inputs', "sort_inputs()")
tm.addCommand('Multi Paste', "multi_paste()")

### Keyboard shortcuts
tm.addSeparator()
tm.addCommand('AutoBackdrop', "tb_autobackdrop()", shortcut='Alt+Shift+B')
tm.addCommand('Edit Label', "editLabel()", shortcut='Ctrl+L')
# It's time to let this go until I get smartRoto working for the Nuke7 world.
#tm.addCommand('Smart Roto', "smartBezier()", shortcut='p')
tm.addCommand('Reset Viewer Gain & Gamma', "reset_viewers_gain_gamma()", shortcut='Alt+V')

##
## Node defaults
##

# Global 
nuke.knobDefault('shutteroffset','centered')

# Pre-select alpha for "unpremult" knob on these nodes:
nodes = ['Grade', 'ColorCorrect', 'Add', 'Gamma', 'Multiply', 'HueCorrect', 'EXPTool', 'ColorLookup']
for node in nodes:
    nuke.knobDefault(node+'.unpremult', '-rgba.alpha')

#nuke.knobDefault("BackdropNode.tile_color", "0x777777ff")
nuke.knobDefault("BackdropNode.note_font_size", "128")
nuke.knobDefault("BackdropNode.note_font", "bold")
nuke.knobDefault("BackdropNode.note_font_color", "0xffffffff")
nuke.knobDefault("Blur.label", "[value size]")
nuke.knobDefault("Blur.channels","rgba")
nuke.knobDefault("Tracker.label", "[value transform]\nref: [value reference_frame]")
nuke.knobDefault('Keymix.bbox','B side')
nuke.knobDefault("Multiply.label", "[value value]")
nuke.knobDefault("Multiply.channels", "rgb")
nuke.knobDefault("Add.label", "[value value]")
nuke.knobDefault("Add.channels", "rgb")
nuke.knobDefault("Gamma.label", "[value value]")
nuke.knobDefault("Add.channels", "rgb")
nuke.knobDefault("Gamma.channels", "rgb")
nuke.knobDefault("Remove.channels", "rgba")
nuke.knobDefault("Remove.operation", "keep")
# nuke.knobDefault("Remove.label", "[value channels]") # Default in Nuke now.
nuke.knobDefault("Output.note_font_size", "18")
nuke.knobDefault("Output.note_font", "bold")
nuke.knobDefault("FrameRange.label", "x[value knob.first_frame]-[value knob.last_frame]")
# TODO: Figure out why this isn't working. It's probably because StickyNotes get created by a method in Nuke's menu.py.
nuke.knobDefault('Roto.toolbox','createBSpline')
nuke.knobDefault("RotoPaint.toolbox", "brush {{brush ltt 0} {clone ltt 0}}")
nuke.knobDefault("StickyNote.label", '<align left>')
nuke.knobDefault("Retime.before", "continue")
nuke.knobDefault("Retime.after", "continue")
nuke.knobDefault("Roto.output", 'rgba')
nuke.knobDefault('TimeOffset.label','[value time_offset] frames\nsource: x[expression [value frame]-[value time_offset]]')
nuke.knobDefault("Tracker4.label", """mode: [value transform]
    ref: x[value reference_frame]""")
nuke.knobDefault("ContactSheet.width", '{"input.width * columns"}')
nuke.knobDefault("ContactSheet.height", '{"input.height * rows"}')
nuke.knobDefault("ContactSheet.roworder", 'TopBottom')
nuke.knobDefault("ContactSheet.colorder", 'LeftRight')
nuke.knobDefault("ContactSheet.rows", '{"splitinputs ? ceil((endframe-startframe+1)/columns) : ceil(inputs/columns)"}')
nuke.knobDefault("ContactSheet.columns", '{"splitinputs ? ceil(sqrt(endframe-startframe+1)) : ceil(sqrt(inputs))"}')
nuke.knobDefault("Dot.note_font_size","22")
nuke.knobDefault("EXPTool.mode", "Stops")
nuke.knobDefault("VectorBlur.uv","forward")


### Load Comp Island
try:
    import comp_island
except ImportError as e:
    nuke.tprint('*** Skipping import of comp_island. Error:', e)
else:
    comp_island.add_menu()

### Load labelDots
try:
    import labelDots
except ImportError as e:
    nuke.tprint('*** Skipping import of labelDots. Error:', e)
else:
	tm.addCommand('Label Dots',
        command = "labelDots.dotLabel()",
        shortcut = "Ctrl+Shift+L",
        tooltip = "This will label any dots to the same as the first higer level dot, with a label, found."
        )

### mark_tricky_nodes
nuke.tprint('Importing mark_tricky_nodes')
try:
    import mark_tricky_nodes
except ImportError as e:
    nuke.tprint('*** Skipping import of mark_tricky_nodes. Error:', e)
else:
    mark_tricky_nodes.add_menu(tm)

### Load trackedbezier
try:
    import trackedbezier
except ImportError as e:
    nuke.tprint('*** Skipping import of trackedbezier. Error:', e)
else:
    trackedbezier.add_menu(tm)

### Load trackedroto
try:
    import trackedroto
except ImportError as e:
    nuke.tprint('*** Skipping import of trackedroto. Error:', e)
else:
    trackedroto.add_menu(tm)

### Load trackerstablemm
try:
    import trackerstablemm
except ImportError as e:
    nuke.tprint('*** Skipping import of trackerstablemm. Error:', e)
else:
    trackerstablemm.add_menu(tm)

### Load unhook_viewer_input_one
nuke.tprint('Importing unhook_viewer_input_one')
try:
    import unhook_viewer_input_one
except ImportError as e:
    nuke.tprint('Skipping import of unhook_viewer_input_one. Error:', e)

### Load bgNukes
nuke.tprint('Importing bgNukes')
try:
    import bgNukes
except ImportError as e:
    nuke.tprint('Skipping import of bgNukes. Error:', e)

### Load viewer_connect_default_inputs
try:
    import viewer_connect_default_inputs
except ImportError as e:
    nuke.tprint('*** Skipping import of viewer_connect_default_inputs. Error:', e)
else:
    viewer_connect_default_inputs.add_menu(tm)

### Load color_change
try:
    import color_change
except ImportError as e:
    nuke.tprint('*** Skipping import of color_change. Error:', e)
else:
    color_change.add_menu(tm)

### Load color_change
try:
    import autolabel_shuffle2
except ImportError as e:
    nuke.tprint('*** Skipping import of autolabel_shuffle2. Error:', e)

nuke.tprint('  END: '+ os.path.realpath(__file__))
