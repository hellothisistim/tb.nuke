
nuke.tprint('START: '+ os.path.realpath(__file__))

# Find the current user's nodes menu.
m = nuke.menu('Nodes')
user = 'tim'
tm = m.findItem(user)

if tm is not None:
    #nuke.tprint("Found menu: ", tm.name())

    tm.addCommand('Gizmos/Filter/apChroma', "nuke.createNode('apChroma')", icon="apChroma.png")
    tm.addCommand('Gizmos/Merge/apChromaMerge', "nuke.createNode('apChromaMerge')", icon = "apChroma.png")

else:
    nuke.tprint("User " + user + " does not have a menu. Not adding gizmos.")

nuke.tprint('  END: '+ os.path.realpath(__file__))
