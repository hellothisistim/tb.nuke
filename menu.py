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

##
## Node defaults
##

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
nuke.knobDefault("StickyNote.label", '<align left>')
nuke.knobDefault("Retime.before", "continue")
nuke.knobDefault("Retime.after", "continue")
nuke.knobDefault("Roto.output", 'rgba')
nuke.knobDefault("ContactSheet.width", '{"input.width * columns"}')
nuke.knobDefault("ContactSheet.height", '{"input.height * rows"}')
nuke.knobDefault("ContactSheet.roworder", 'TopBottom')
nuke.knobDefault("ContactSheet.colorder", 'LeftRight')
nuke.knobDefault("ContactSheet.rows", '{"splitinputs ? ceil((endframe-startframe+1)/columns) : ceil(inputs/columns)"}')
nuke.knobDefault("ContactSheet.columns", '{"splitinputs ? ceil(sqrt(endframe-startframe+1)) : ceil(sqrt(inputs))"}')
nuke.knobDefault("Dot.note_font_size","22")
nuke.knobDefault("EXPTool.mode", "Stops")
nuke.knobDefault("VectorBlur.uv","forward")

### My keyboard shortcuts
tm.addSeparator()
mkshort = tm.addMenu('(These are my special keyboard shortcuts)')
mkshort.addCommand('AutoBackdrop', "tb_autobackdrop()", shortcut='Alt+Shift+B')
mkshort.addCommand('Edit Label', "editLabel()", shortcut='Ctrl+L')
# It's time to let this go until I get smartRoto working for the Nuke7 world.
#mkshort.addCommand('Smart Roto', "smartBezier()", shortcut='p')


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




nuke.tprint('  END: '+ os.path.realpath(__file__))
