#-----------------------------------------------------------------------------
# link_roto_layer.py
#
# Tim BOWMAN [tim@hellothisistim.com]
#

"""A tool to aid tracked roto. Creates a new layer in a Roto node and links its
transform controls to a separate Tracker or Transform node.

"""

import nuke
import _curvelib



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
    # print("Curves:", curves, '\nRoot: ', root)
    # Adding new layer. Sourced from https://community.foundry.com/discuss/post/989127
    layer_name = 'Tracked to: ' + trans.name() + ' :'

    new_layer = nuke.rotopaint.Layer(curves, name=layer_name)
    # print("New layer:", type(new_layer), '\n', new_layer)
    root.append(new_layer)

    # Now, we need to find the layer again because it got a number appended to its name.
    # Nuke appends a sequential number, even if we end the name with a number.
    layer = None
    names = []
    for shape in root:
        print(shape.name)
        if shape.name.startswith(layer_name):
            names.append(shape.name)

    name = sorted(names)
    # print("Sorted layer names:", names)
    # print("Last one:", names[-1])
    layer_name = names[-1]

    # some examples for setting expressions in the python api for the nuke rotopaint system
    # https://gist.github.com/jedypod/52cf750e02ee2cee2e407b16e1616540
    # get a specific shape
    layer = curves.toElement(layer_name)
    print(layer.name, layer)

    # We will set an expression on the translate, rotate, and scale for this shape
    xform = layer.getTransform()
    # Let's try putting the transform on the root layer instead.
    xform = root.getTransform()

    # Find all the things you can do with this object with
    #print(help(xform))

    # First we have to create an _curvelib.AnimCurve object to hold our animation curve.
    translation_curve_x = _curvelib.AnimCurve()
    translation_curve_y = _curvelib.AnimCurve()
    rotation_curve = _curvelib.AnimCurve()
    scale_curve_w = _curvelib.AnimCurve()
    scale_curve_h = _curvelib.AnimCurve()
    center_curve_x = _curvelib.AnimCurve()
    center_curve_y = _curvelib.AnimCurve()

    # To set an expression on our curve we have to set the expressionString and useExpression to True
    translation_curve_x.expressionString = trans.name() + '.translate'
    translation_curve_y.expressionString = trans.name() + '.translate'
    rotation_curve.expressionString = trans.name() + '.rotate'
    scale_curve_w.expressionString = trans.name() + '.scale'
    scale_curve_h.expressionString = trans.name() + '.scale'
    center_curve_x.expressionString = trans.name() + '.center'
    center_curve_y.expressionString = trans.name() + '.center'

    # set useExpression=True for all curves
    for curve in [translation_curve_x, translation_curve_y, rotation_curve, scale_curve_w, scale_curve_h, center_curve_x, center_curve_y]:
        curve.useExpression = True

    # Now we overwrite the animcurves on the shape
    xform.setTranslationAnimCurve(0, translation_curve_x)
    xform.setTranslationAnimCurve(1, translation_curve_y)
    # Index value of setRotationAnimCurve is 2 even though there is only 1 parameter...
    # http://www.mail-archive.com/nuke-python@support.thefoundry.co.uk/msg02295.html
    xform.setRotationAnimCurve(2, rotation_curve)
    xform.setScaleAnimCurve(0, scale_curve_w)
    xform.setScaleAnimCurve(1, scale_curve_h)
    xform.setPivotPointAnimCurve(0, center_curve_x)
    xform.setPivotPointAnimCurve(1, center_curve_y)



#link_roto_layer()
