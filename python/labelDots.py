# labelDots.py
# A tool to auto label dots for script management
#
# Written by Howard Jones [www.whitebeamvfx.com]
# Sourced from http://www.nukepedia.com/python/nodegraph/labeldots

import nuke

message = """Please select a dot.

labelDots, by Howard Jones (<a href="http://www.nukepedia.com/python/nodegraph/labeldots/">Nukepedia</a>)

This will label any dots to the same as the first higher level dot, with a label, found. If you label the top of your pipe "Main Mattes" and have successive dots underneath, select all and run this, then all your dots are relabelled to match."""


def getParentNode(node):
    try:
        parentNode = node.input(0)

        if parentNode.Class() == 'Dot':
                if not parentNode['label'].getValue():
                    return getParentNode(parentNode)
                else:
                    return parentNode

    except AttributeError:
        return

def dotLabel():
        if not nuke.selectedNodes('Dot'):
            nuke.message(message)
            return
        else:
            nodes= nuke.selectedNodes('Dot')

        for i in nodes:
            try:
                pn=getParentNode(i)
                pnlabel=pn['label'].value()
                pnLabelSize=pn['note_font_size'].value()
                pnLabelColour=pn['note_font_color'].value()

                i['label'].setValue(pnlabel)
                i['note_font_size'].setValue(pnLabelSize)
                i['note_font_color'].setValue(int(pnLabelColour))
            except TypeError:
                pass
