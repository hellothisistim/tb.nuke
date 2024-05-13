nuke.tprint('START: '+ os.path.realpath(__file__))

nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./gizmos/3rdParty')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./python')

### Third-party tools
# 
# Many, many thanks to the authors for making these tools.

# Nuke Vector Matrix Toolset
# by Mathieu Goulet-Aubin and Erwan Leroy
# https://github.com/mapoga/nuke-vector-matrix/releases
nuke.pluginAddPath('./3rdParty/nuke-vector-matrix-1.1.0')




nuke.tprint('  END: '+ os.path.realpath(__file__))
