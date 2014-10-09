# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

## init.py
## loaded by nuke before menu.py

nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./python')


## Create output directories automatically
## Taken from the Nuke Python Dev Guide
def createWriteDir():
  import nuke, os, errno
  file = nuke.filename(nuke.thisNode())
  dir = os.path.dirname( file )
  osdir = nuke.callbacks.filenameFilter( dir )
  # cope with the directory existing already by ignoring that exception
  try:
    os.makedirs( osdir )
  except OSError, e:
    if e.errno != errno.EEXIST:
      raise
nuke.addBeforeRender(createWriteDir)


# Make all filepaths load without errors regardless of OS (No Linux support and no C: support)
# Big thanks to Fredrik Averpil: http://fredrik.averpil.com/post/17033531721
def myFilenameFilter(filename):
  if nuke.env['MACOS']:
    filename = filename.replace( 'X:', '/Volumes/Work/jobs/phos' )
  if nuke.env['WIN32']:
    filename = filename.replace( '/Volumes/Work/jobs/phos', 'X:' )

  return filename


# Use the filenameFilter(s)
nuke.addFilenameFilter(myFilenameFilter)
