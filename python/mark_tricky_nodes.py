#-----------------------------------------------------------------------------
# mark_tricky_nodes.py
#
# Tim BOWMAN [puffy@netherlogic.com]
# 
# updated 30 January 2013

"""Sometimes, when we drive nodes using expressions or hide the inputs to 
nodes, Nuke scripts can behave oddly or be difficult to read. The tools in 
this module mark those nodes to make such troublemakers more obvious.

"""

import nuke

#-----------------------------------------------------------------------------
## Globals

# List of expressions that can cause us trouble. Add more as you wish.
dangerous_expressions = ['$gui', 'proxy']
warning_color = 0xff000000 # Really quite red

#-----------------------------------------------------------------------------
## Methods

def allKnobsWithExpressions():
    """Returns a list of all the knobs in this script that are driven by 
    expressions.
    
    """

    knobs_with_expressions = []
    for node in nuke.allNodes(recurseGroups=True):
        for knob in node.knobs():
            if node.knob(knob).hasExpression():
                knobs_with_expressions.append(node.knob(knob))
    return knobs_with_expressions

def allNodesWithHiddenInputs():
    """Returns a list of all the nodes in this script with the hide_input knob activated.
    """

    nodes_with_hidden_inputs = []
    for node in nuke.allNodes(recurseGroups=True):
        if node.knob('hide_input').value() is True:
            nodes_with_hidden_inputs.append(node)

    return nodes_with_hidden_inputs

def markThisNode(node, expr):
    """Mark the given node in an obvoius way so any potential problem is 
    obvoius. That means make it red and put a warning in the node's label.
    
    TODO: Genericize this for other markings besides expressions. Hidden 
    inputs are another good application.

    node is the target node
    expr is the offending expression
    
    """

    if node.knob('tile_color').value() != warning_color:
        node.knob('tile_color').setValue(warning_color)
    label_text = '*** expression-driven ***\n*** ' + expr + ' ***'
    # Escape $
    label_text = label_text.replace('$', '\$')
    label_contents = node.knob('label').toScript()
    if label_text not in label_contents:
        nuke.tprint("Marking " + node.fullName() + " as potentially dangerous.")             
        node.knob('label').fromScript( label_contents + '\n' + label_text)

def markNodesWithDangerousExpressions():
    """For any expression-driven knob that has a potentially confusing 
    expression in it, mark it's node orange and put a warning in the label.
    
    """

    # List of expressions that can cause us trouble. Add more as you wish.
    dangerous_expressions = ['$gui', 'proxy']

    knobs=allKnobsWithExpressions()

    for knob in knobs:
        for expr in dangerous_expressions:
            if expr in knob.toScript():
                # Mark this one
                markThisNode(knob.node(), str(expr))


def markNodesWithHiddenInputs():
    """For any node with a hidden input, mark it and put a warning in the label.
    """

    for node in allNodesWithHiddenInputs():
        markThisNode(node, 'hiddden input')



nuke.addOnScriptLoad(markNodesWithDangerousExpressions)
# TODO: Test this, then turn it on.
#nuke.addOnScriptLoad(markNodesWithHiddenInputs)
