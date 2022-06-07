#-----------------------------------------------------------------------------
# trackedroto.py
#
# Tim BOWMAN [tim@hellothisistim.com]
#

"""A tool to aid tracked roto. Creates a Roto node that has its root
transform controls linked to the selected Tracker or Transform node.
"""

import nuke



def trackedroto():

    error_message = "Please select either a Transform or Tracker as the source for your tracked Roto."

    sel = nuke.selectedNodes()
    if len(sel) != 1:
        nuke.message(error_message)
        return

    if sel[0].Class() not in ["Transform", "Tracker4"]:
        nuke.message(error_message)
        return

    trans = sel[0]
    trans.setSelected(False)
    roto = nuke.createNode('Roto')

    roto.setName('TrackedRoto')

    # print("Tracker:", trans.name())
    # print("Roto:", roto.name())


    curves = roto['curves']
    root = curves.rootLayer
    xform = root.getTransform()

    # Find all the things you can do with this object with
    #print(help(xform))


    # To set an expression on our curve we have to set the expressionString and useExpression to True
    tx = xform.getTranslationAnimCurve(0)
    tx.expressionString = 'parent.' + trans.name() + '.translate'
    tx.useExpression = True
    ty = xform.getTranslationAnimCurve(1)
    ty.expressionString = 'parent.' + trans.name() + '.translate'
    ty.useExpression = True
    # Index value of setRotationAnimCurve is 2 even though there is only 1 parameter...
    # http://www.mail-archive.com/nuke-python@support.thefoundry.co.uk/msg02295.html
    r = xform.getRotationAnimCurve(2)
    r.expressionString = 'parent.' + trans.name() + '.rotate'
    r.useExpression = True
    sw = xform.getScaleAnimCurve(0)
    sw.expressionString = 'parent.' + trans.name() + '.scale'
    sw.useExpression = True
    sh = xform.getScaleAnimCurve(1)
    sh.expressionString = 'parent.' + trans.name() + '.scale'
    sh.useExpression = True
    cx = xform.getPivotPointAnimCurve(0)
    cx.expressionString = 'parent.' + trans.name() + '.center'
    cx.useExpression = True
    cy = xform.getPivotPointAnimCurve(1)
    cy.expressionString = 'parent.' + trans.name() + '.center'
    cy.useExpression = True


#link_roto_layer()
