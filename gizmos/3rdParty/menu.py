
nuke.tprint('START: '+ os.path.realpath(__file__))

# Find the current user's nodes menu.
m = nuke.menu('Nodes')
user = 'tim'
tm = m.findItem(user)

if tm is not None:
    #nuke.tprint("Found menu: ", tm.name())

    # Gizmos from Adrian Pueyo
    # https://adrianpueyo.com/gizmos/
    tm.addCommand('Gizmos/Filter/apChroma', "nuke.createNode('apChroma')", icon="apChroma.png")
    tm.addCommand('Gizmos/Merge/apChromaMerge', "nuke.createNode('apChromaMerge')", icon = "apChroma.png")
    tm.addCommand('Gizmos/Color/apDespill', "nuke.createNode('apDespill')", icon="apDespill.png")
    tm.addCommand('Gizmos/Keyer/apDirLight', "nuke.createNode('apDirLight')", icon="apDirLight.png")
    tm.addCommand('Gizmos/Filter/apEdgePush', "nuke.createNode('apEdgePush')", icon="apEdgePush.png")
    tm.addCommand('Gizmos/Filter/apGlow', "nuke.createNode('apGlow')", icon="apGlow.png")
    tm.addCommand('Gizmos/Other/aPMatte', "nuke.createNode('aPMatte')", icon="aPMatte.png")
    tm.addCommand('Gizmos/Filter/apScreenClean', "nuke.createNode('apScreenClean')", icon="apScreenClean.png")
    tm.addCommand('Gizmos/Filter/apScreenGrow', "nuke.createNode('apScreenGrow')", icon="apScreenGrow.png")

    tm.addCommand('Gizmos/Keyer/TX_HueKeyer', "nuke.createNode('TX_HueKeyer')")

else:
    nuke.tprint("User " + user + " does not have a menu. Not adding gizmos.")

nuke.tprint('  END: '+ os.path.realpath(__file__))
