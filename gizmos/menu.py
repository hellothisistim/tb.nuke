
nuke.tprint('START: '+ os.path.realpath(__file__))

# Find the current user's nodes menu.
m = nuke.menu('Nodes')
user = os.getenv('USER')
tm = m.findItem(user)

if tm is not None:
    #nuke.tprint("Found menu: ", tm.name())

    tm.addCommand('Gizmos/Draw/ColorChecker', "nuke.createNode('ColorChecker')", icon="T-icon.png")
    tm.addCommand('Gizmos/Filter/Offset', "nuke.createNode('Offset')", icon="T-icon.png")
    tm.addCommand('Gizmos/Filter/Perspective_Correct', "nuke.createNode('Perspective_Correct')", icon = "T-icon.png")
    tm.addCommand('Gizmos/Keyer/RGBCMY_Selector', "nuke.createNode('RGBCMY_Selector')", icon="T-icon.png")

else:
    print("User " + user + " does not have a menu. Not adding gizmos.")

nuke.tprint('  END: '+ os.path.realpath(__file__))
