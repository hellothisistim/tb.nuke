# ~/.nuke/nukepedia/menu.py

nuke.tprint('HELLO from the ~/.nuke/nukepedia/menu.py')

nuke.pluginAddPath('./viewerInput1_1')

# 
## The "me" menu
##
m = nuke.menu('Nodes')
user = os.getenv('USER')
tm = m.findItem(user)
if tm is not None:

    # Label Dots
    try:
        import labelDots
        tm.addCommand('Label Dots', 'nuke.load("labelDots"), dotLabel()')

    except:
        nuke.tprint('labelDots not found.')

try:
	import cycle_vlut
    cycle_vlut.setup_menu()
except:
	nuke.tprint('cycle_vlut not found.')


nuke.tprint('ALL DONE from the ~/.nuke/nukepedia/menu.py')
