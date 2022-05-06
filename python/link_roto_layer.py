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
        print("Node class is", node.Class())
        if node.Class() == "Roto":
            roto = node
        if node.Class() in ["Transform", "Tracker4"]:
            trans = node
    if roto == None or trans == None:
        nuke.message(error_message)
        return

    print("Tracker:", trans.name())
    print("Roto:", roto.name())






    #n = nuke.nodes.Roto()
    #
    #curves = n['curves']
    #root = curves.rootLayer
    #
    #print(root, dir(root))
    #for shape in root:
    #    print(shape.name)
    #

link_roto_layer()
