#-----------------------------------------------------------------------------
# link_roto_layer.py
#
# Tim BOWMAN [tim@hellothisistim.com]
#

"""A tool to aid tracked roto. Creates a new layer in a Roto node and links its
transform controls to a separate Tracker or Transform node.

"""

import nuke


def link_roto_layer():

    error_message = "Please select a Roto node and either a Transform or Tracker node to create a linked roto layer."

    sel = nuke.selectedNodes()
    if len(sel) != 2:
        nuke.message(error_message)
        return

    roto = None
    trans = None
    for node in sel:
        # print("Node class is", node.Class())
        if node.Class() == "Roto":
            roto = node
        if node.Class() in ["Transform", "Tracker4"]:
            trans = node
    if roto == None or trans == None:
        nuke.message(error_message)
        return

    print("Tracker:", trans.name())
    print("Roto:", roto.name())

    # Add a new layer to Roto. Use the source's name in its name.
    # print(roto, '\n\n')

    curves = roto['curves']
    root = curves.rootLayer

    # print(root, dir(root))
    print("Curves:", curves, '\nRoot: ', root)
    # Adding new layer. Sourced from https://community.foundry.com/discuss/post/989127
    layer_name = 'Linked to: ' + trans.name() + ' :'
    new_layer = nuke.rotopaint.Layer(curves, name=layer_name)
    # print("New layer:", type(new_layer), '\n', new_layer)
    # print(dir(new_layer))
    root.append(new_layer)


    # some examples for setting expressions in the python api for the nuke rotopaint system
    # https://gist.github.com/jedypod/52cf750e02ee2cee2e407b16e1616540
    # get a specific shape
    layer = curves.toElement(layer_name)
    print(layer.name, layer) # TODO: Why is this returning NoneType?

    # We will set an expression on the translate, rotate, and scale for this shape
    xform = layer.getTransform()

    # Find all the things you can do with this object with
    #print(help(xform))

    # First we have to create an _curvelib.AnimCurve object to hold our animation curve.
    translation_curve_x = nuke._curvelib.AnimCurve()
    translation_curve_y = nuke._curvelib.AnimCurve()
    rotation_curve = nuke._curvelib.AnimCurve()
    scale_curve = nuke._curvelib.AnimCurve()

    # To set an expression on our curve we have to set the expressionString and useExpression to True
    translation_curve_x.expressionString = 'frame'
    translation_curve_y.expressionString = 'frame%2'
    rotation_curve.expressionString = 'frame'
    scale_curve.expressionString = 'frame/100+0.5'

    # set useExpression=True for all curves
    for curve in [translation_curve_x, translation_curve_y, rotation_curve, scale_curve]:
        curve.useExpression = True

    # Now we overwrite the animcurves on the shape
    xform.setTranslationAnimCurve(0, translation_curve_x)
    xform.setTranslationAnimCurve(1, translation_curve_y)
    # Index value of setRotationAnimCurve is 2 even though there is only 1 parameter...
    # http://www.mail-archive.com/nuke-python@support.thefoundry.co.uk/msg02295.html
    xform.setRotationAnimCurve(2, rotation_curve)
    xform.setScaleAnimCurve(0, scale_curve)
    xform.setScaleAnimCurve(1, scale_curve)



link_roto_layer()
