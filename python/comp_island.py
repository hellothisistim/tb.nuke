# Comp Island
#
# Enable switching to a completely isolated "island mode" by completely ignoring the /asset tree and using only files in /mnt/scratch/localise_path
#
#

import nuke
from nukescripts import searchreplace

### Globals
local_root = nuke.toNode('preferences').knob('localCachePath').evaluate() + "/_asset"
remote_root = '/asset'
label_text = '***LOCALISED PATH***'        # This is jammed in the read's label to indicate the localization.
proxy_label_text = '***LOCALISED PROXY***' # This is jammed in the read's label to indicate the proxy localization.
warning_colour = '0xc0125dff'              # Change nodes with mangled file paths to this colour.
proxy_warning_colour = '0x52d2ff'          # Change nodes woth local proxy paths to this colour.
# Keyboard shortcuts
proxy_kbd = 'Alt+l'
deproxy_kbd = 'Alt+Shift+l'

### Utility Methods

def _file_knob_filter(knobs):
    """Return only the File_Knobs that actually contain a value in a list of knobs."""

    return [k for k in knobs if k.Class() == 'File_Knob' and k.value() != '']

def _file_knobs(nodes):
    """Return all the non-empty file knobs for all of the provided nodes."""

    file_knobs = []
    for node in nodes:
        for knob in _file_knob_filter(node.allKnobs()):
            file_knobs.append(knob)
    return file_knobs

def _all_nodes_in_groups(nodes):
    """Recursively find nodes inside groups."""

    for node in nodes:
        if node.Class() == 'Group':
            for new_node in _all_nodes_in_groups(node.nodes()):
                nodes.append(new_node)
    return nodes
    
def _smart_nodelist_expand(nodes=None):
    """Be smart about filling in a list of nodes. If no nodes are specified, 
    try the selected nodes. If no nodes are selected, use all nodes in the 
    script."""
    
    if nodes is None:
        if len(nuke.selectedNodes()) != 0: nodes = nuke.selectedNodes()
        else: nodes = nuke.allNodes()
    # Recursively find nodes in groups
    nodes = _all_nodes_in_groups(nodes)

    return nodes
 
### Core Methods

# TODO: need a method to check the "localness" of the sources

# TODO: bg_localise()
def bg_localise():
    """Localise files via a nice BG process."""

    # subprocess...  nuke -t... nuke.localiseFiles()   --- (no thinking about how and where)
    # or possibly do the copy manually  
    pass

def localised_path(node):
    """Are the paths in these nodes local?"""

    for knob in _file_knobs([node]):
        if not knob.toScript().startswith(local_root): return False
    return True

def localised_proxy_path(node):
    """Does the proxy path point to a local file?"""
    
    # TODO: write this function
    if 'proxy' in node.knobs():
        if node.knob('proxy').toScript().startswith(local_root): return True
    return False

def localise_path(nodes=None):
    """Change remote file paths to localised_path file paths. 
    (eg. /asset/wud/ma becomes /mnt/scratch/localise_path/_asset/wud/ma)"""

    nodes = _smart_nodelist_expand(nodes)
    for knob in _file_knobs(nodes):
        # Don't double-localise_path.
        if localised_path(knob.node()): continue
        # Munge path
        searchreplace.__ReplaceKnobValue(remote_root, local_root, knob)
        # Add reminder text to node's label
        k = knob.node().knob('label')
        if k.value() == "": k.fromScript(label_text)
        else: k.fromScript("\n".join([k.toScript(), label_text]))
        # Colour the node as a further reminder that we've mangled the path
        k.node().knob('tile_color').fromScript(warning_colour)

def localise_proxy_path(nodes=None):
    """Set the proxy path to the local path for this file."""

    nodes = _smart_nodelist_expand(nodes)
    print nodes
    for node in [node for node in nodes if 'proxy' in node.knobs()]:
        knob = node.knob('proxy')
        # Don't double-localise_path.
        if localised_proxy_path(node): 
            print 'skipping', knob.name()
            continue
        # Assign and munge path
        knob.fromScript( node.knob('file').toScript() )
        searchreplace.__ReplaceKnobValue(remote_root, local_root, knob)
        # Add reminder text to node's label
        k = knob.node().knob('label')
        if k.value() == "": k.fromScript(proxy_label_text)
        else: k.fromScript("\n".join([k.toScript(), proxy_label_text]))
        # Colour the node as a further reminder that we've mangled the path
        k.node().knob('tile_color').fromScript(proxy_warning_colour)

def delocalise(nodes=None):
    """Chance localized file paths to remote file paths.
    (eg. /mnt/scratch/localise_path/_asset/wud/ma becomes /asset/wud/ma)"""

    nodes = _smart_nodelist_expand(nodes)
    for knob in _file_knobs(nodes):
        searchreplace.__ReplaceKnobValue(local_root, remote_root, knob)
        k = knob.node().knob('label')
        k.fromScript(k.toScript().replace('\n'+label_text, ''))
        k.fromScript(k.toScript().replace(label_text, ''))
        # Remove warning tile colour from node 
        k.node().knob('tile_color').fromScript('0')

def clear_local_proxy(nodes=None):
    """Clear the proxy knob if it's pointing to a local file."""

    nodes = _smart_nodelist_expand(nodes)
    for node in [node for node in nodes if 'proxy' in node.knobs()]:
        knob = node.knob('proxy')
        knob.setValue('')
        k = knob.node().knob('label')
        k.fromScript(k.toScript().replace('\n'+proxy_label_text, ''))
        k.fromScript(k.toScript().replace(proxy_label_text, ''))
        # Remove warning tile colour from node 
        k.node().knob('tile_color').fromScript('0')

    # TODO: Write this
    pass

def add_menu():
    """Add "Comp Island" submenu to "Cache" menu."""

    # Build Comp Island submenu
    m = nuke.menu('Nuke').findItem('Cache')
    m.addSeparator()
    m_ci = m.addMenu('Comp Island')
    # Add Comp Island features
    m_ci.addCommand('Localise file paths', "comp_island.localise_path()")
    m_ci.addCommand('Delocalise file paths', "comp_island.delocalise()")
    m_ci.addCommand('Localise file proxy', "comp_island.localise_proxy_path()", proxy_kbd)
    m_ci.addCommand('Delocalise file proxy', "comp_island.clear_local_proxy()", deproxy_kbd)
    m_ci.addCommand('Help (wiki)', "nukescripts.openurl.start('http://wiki.rsp.com.au/rspwiki/index.php/User:Timothyb/Comp_Localization')")



### Nuke GUI
if nuke.env['gui']:
    add_menu()

