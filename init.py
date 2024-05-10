nuke.tprint('START: '+ os.path.realpath(__file__))

nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./gizmos/3rdParty')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./python')

### Third-party tools

# Nuke Vector Matrix Toolset: https://github.com/mapoga/nuke-vector-matrix/releases
# Install in the tb.nuke folder.
nuke.pluginAddPath('./nuke-vector-matrix-1.1.0')

nuke.tprint('  END: '+ os.path.realpath(__file__))
