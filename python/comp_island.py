# comp_island.py
#

"""Comp Island enables switching to a completely isolated "island mode" while comping in Nuke. This may be useful in cases when central shared storage is very slow, but comp work still needs to continue.

Here's how it works:

First, make sure you have a local copy of all your source footage using Nuke's built-in localization tools in the Cache menu. Then, use Comp Island to switch all of your Read nodes to the local copy. This provides a speed boost because Nuke can read the cached local files much more quickly than the originals on the slow server. When you're done working, delocalise the paths and you're back to reading the original files on the server.

Comp Island provides two different ways to switch to local files:

The drastic way is to edit the file path in each Read node's "file" knob using the "Localise file paths" option. Unfortunately, this doesn't leave you any record of where the original file is on the server.

A more subtle way is to use "Localise file proxy". This keeps the original file path in the "file" knob and puts the local path in the "proxy" knob. Then switch your script to proxy mode and set "proxy scale" to 1 in Project Setings. Now you can switch back and forth between your local cache and the originals at the push of a button. If your facility uses proxies in a serious way, this could cause you some trouble. In that case, use the drastic option above.

When localising, Comp Island will localize on all selected nodes. If there are no nodes selected, it will work on all nodes in the script, including nodes buried in groups. When changing paths on a node, Comp Island will change its color to something annoyingly saturated and add a note to the label. This is to help you remember to undo these shenanigans when you're finished.

Removing the localised paths is just like putting them in, except you chose the "Delocalize" option that corresponds to the localise you used originally.

* Please note: When playing around with file paths like this, you may run into trouble with tools at your facility that expect Nuke scripts to reference the files on the central storage. Be sure to switch paths back before sending renders to the farm or publishing. You now have great power to push through bottlenecks, but the responsibility to use it safely is also yours.

Tim Bowman (tim@hellothisistim.com)

"""


import nuke
from nukescripts import searchreplace

### Globals
local_root = nuke.toNode('preferences').knob('localCachePath').evaluate() + '\_asset'
remote_root = '/asset'
label_text = '***LOCALISED PATH***'        # This is put in the read's label to indicate the localisation.
proxy_label_text = '***LOCALISED PROXY***' # This is jammed in the read's label to indicate the proxy localisation.
warning_colour = '0xc0125dff'              # Change nodes with localised file paths to this colour.
proxy_warning_colour = '0x52d2ff'          # Change nodes with local proxy paths to this colour.
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


def localised_path(node):
    """Are the paths in these nodes local?"""

    for knob in _file_knobs([node]):
        if not knob.toScript().startswith(local_root): return False
    return True

def localised_proxy_path(node):
    """Does the proxy path point to a local file?"""

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
    print( nodes )
    for node in [node for node in nodes if 'proxy' in node.knobs()]:
        knob = node.knob('proxy')
        # Don't double-localise_path.
        if localised_proxy_path(node):
            print( 'skipping', knob.name() )
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
    """Change localized file paths to remote file paths.
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

def editRootPaths():
    """View and change the local and remote root paths. This will be useful if the defaults for local_root and/or remote_root don't work for your facility. (They probably won't unless you're working at the place I originally built this for.)

    If you find yourself doing this a lot, edit the defaults at the top of comp_island.py."""

    global local_root
    global remote_root
    p = nuke.Panel('Local and Remote Root Paths')
    p.addFilenameSearch('Local root', local_root)
    p.addFilenameSearch('Remote root', remote_root)
    ret = p.show()
    local_root = p.value('Local root')
    remote_root = p.value('Remote root')

def add_menu():
    """Add "Comp Island" submenu to "Cache" menu."""

    # Build Comp Island submenu
    m = nuke.menu('Nuke').findItem('Cache')
    m.addSeparator()
    m_ci = m.addMenu('Comp Island')
    # Add Comp Island features
    nuke.tprint("This is local_root: " + local_root)
    m_ci.addCommand('Edit local and remote root directories', lambda: editRootPaths())
    m_ci.addCommand('Localise file paths', "comp_island.localise_path()")
    m_ci.addCommand('Delocalise file paths', "comp_island.delocalise()")
    m_ci.addCommand('Localise file proxy', "comp_island.localise_proxy_path()", proxy_kbd)
    m_ci.addCommand('Delocalise file proxy', "comp_island.clear_local_proxy()", deproxy_kbd)
    m_ci.addCommand('Help', lambda: nuke.message(__doc__))
