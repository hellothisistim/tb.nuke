# ~/.nuke/nukepedia/menu.py

nuke.tprint('HELLO from '+ os.path.realpath(__file__))


nuke.pluginAddPath('./viewerInput1_1')

#
## The "me" menu
##
m = nuke.menu('Nodes')
user = os.getenv('USER')
tm = m.findItem(user)

if tm is not None:

    nuke.tprint("Found menu: ", tm.name())
    # Label Dots
    try:
        import labelDots
        tm.addCommand('Label Dots', 'nuke.load("labelDots"), dotLabel()')

    except:
        nuke.tprint('labelDots not found. Skipping.')

    try:
        import cycle_vlut
        cycle_vlut.setup_menu()
    except:
        nuke.tprint('cycle_vlut not found. Skipping.')


nuke.tprint('ALL DONE from '+ os.path.realpath(__file__))
