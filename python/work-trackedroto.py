## Linking to the transform tab in a Roto node is more complicated than 
## doing it to an old-fashioned Bezier node. This is a work in progress.

import nuke

def nodeHasTransformKnobs(node):
    """THIS IS A FAKE METHOD! WOO, ANARCHY!"""
    return True

def trackedRoto(node):
    """Given a node with appropriate transform knobs (see nodeHasTransformKnobs), create a new Roto node with it's Root's tranform knobs expression-linked to the source node.
    
    """

    if not nodeHasTransformKnobs(node):
        nuke.message("Sorry boss, can't link a bezier to this one.")

    # Build knob list
    knob_list = ['translate', 'rotate', 'scale', 'skew', 'center']

    node.setSelected(False)
    
    # Build Roto node
    r = nuke.createNode('Roto')
    # This doesn't work for a Roto node, so we have to get all nasty with the curves knob.
    #for knob in knob_list:
    #    r.knob(knob).setExpression(node.name()+'.'+knob)

    # Create new layer and set it's transforms to be expression-driven by the source node.
    curves = r.knob('curves')
    tracked_layer = nuke.rotopaint.Layer(curves)
    tracked_layer.name = 'tracked_to_' + node.name()
    print tracked_layer, dir(tracked_layer)

    curves.rootLayer.append(tracked_layer)


from pprint import *
t = nuke.toNode('Tracker1')
r = nuke.toNode('Roto1')

trackedRoto(t)

"""
c = r.knob('curves')
root = c.rootLayer
print root
trans =  root.getTransform()

transAnimCurve = trans.getTranslationAnimCurve(0)
print transAnimCurve
#pprint(dir(transAnimCurve))

newLayer = nuke.rotopaint.Layer(c)
print newLayer
"""