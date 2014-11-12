# labelDots.py
# A tool to auto label dots for script management
#
# Written by Howard Jones [www.whitebeamvfx.com]
# Sourced from http://www.nukepedia.com/python/nodegraph/labeldots

import nuke

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
            nuke.message('Please select a dot')
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
