import nuke

# Node Has Transform Knobs
def nodeHasTransformKnobs(node):
    """Return true if node has all of the following knobs: translate, rotate, scale, skew, center.

    """

    required_knobs = ['translate', 'rotate', 'scale', 'skew', 'center']
    for knob in required_knobs:
        if knob not in node.knobs().keys():
            return False
    return True


# Tracked Bezier
def trackedBezier(node, translate=True, rotate=True, scale=True, center=True):
    """Given a node with appropriate transform knobs (see
    nodeHasTransformKnobs), create a new Bezier with it's Tranform
    tab knobs expression-linked to the source node.

    """

    if not nodeHasTransformKnobs(node):
        nuke.message("Sorry boss, can't link a bezier to this one.")

    # TODO: add skew
    # Build knob list
    knob_list = ['translate', 'rotate', 'scale', 'skew', 'center']

    node.setSelected(False)

    # Build bezier
    b = nuke.createNode('Bezier')
    for knob in knob_list:
        b.knob(knob).setExpression(node.name()+'.'+knob)

def smartRoto():
    """If a node with some transform data (for example a Tracker or
    Transform node with translate, rotate, scale, and center knobs)
    is selected when this method is called, a bezier will be created with
    it's transform tab bits expression-linked to the transform node.
    Otherwise, a regular bezier will be created.

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


def add_menu(target=None):
    """Add "Tracked Bezier" submenu to specified target menu. If no target is
    supplied, put it in the root of the Nodes menu."""

    # Build Tracked Bezier menu
    m = nuke.menu('Nodes')
    if target is not None:
        m = target
    tbm = m.addMenu("Tracked Bezier")
    # Add Tracked Bezier features
    tbm.addCommand('Linked Bezier from Tracker (all)',
        lambda: trackedBezier(nuke.selectedNode()))
    tbm.addCommand('Linked Bezier from Tracker (trans, center)',
        lambda: trackedBezier(nuke.selectedNode(), translate=True, rotate=False, scale=False, center=True))
    tbm.addCommand('Linked Bezier from Tracker (trans, rot, center)',
        lambda: trackedBezier(nuke.selectedNode(), translate=True, rotate=True, scale=False, center=True))
