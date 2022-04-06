
nuke.tprint('HELLO from '+ os.path.realpath(__file__))



##
## The "me" menu
##
m = nuke.menu('Nodes')
user = os.getenv('USER')
tm = m.findItem(user)

if tm is not None:

    nuke.tprint("Found menu: ", tm.name())
    # apChroma_v1
    tm.addCommand('apChroma', "nuke,createNode('apChroma')", icon="apChroma.png")
    tm.addCommand('apChromaMerge', "nuke,createNode('apChromaMerge')", icon = "apChroma.png")



nuke.tprint('ALL DONE from '+ os.path.realpath(__file__))
