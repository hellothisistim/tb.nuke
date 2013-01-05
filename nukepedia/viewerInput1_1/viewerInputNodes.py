### Creates presets for VIEWER_INPUT nodes 
# written by Howard Jones 2012
# modified 14th October - added Normalize thanks to Diogo and Ivam for the method.

############### IP Menu #######################
m = toolbar.addMenu("IP", "IP.png")
m.addCommand('Grid','nuke.load("viewerInputNodes"), viewerInput(ipNode="Grid", openPanel=True)')
m.addCommand('Mirror','nuke.load("viewerInputNodes"), viewerInput(ipNode="Mirror")')
m.addCommand('Normalize','nuke.load("viewerInputNodes"), viewerInput(ipNode="Normalize")')
m.addCommand('Saturation','nuke.load("viewerInputNodes"), viewerInput(ipNode="Saturation")')
m.addCommand('Over Checkerboard','nuke.load("viewerInputNodes"), viewerInput(ipNode="Over Checkerboard")')
m.addCommand('Over 18% Grey','nuke.load("viewerInputNodes"), viewerInput(ipNode="Over 18% Grey")')
m.addCommand('choose from list','nuke.load("viewerInputNodes"), viewerInput()')
m.addCommand('remove','nuke.load("viewerInputNodes"), viewerInput(ipNode="Remove")')


def viewerInput(ipNode=None, openPanel=False):
  if not ipNode:
    p=nuke.Panel('Input Process',300)
    p.addEnumerationPulldown('IP node','Grid Mirror Normalize "Over Checkerboard" "Over 18% Grey" Saturation')
    p.addBooleanCheckBox('open panel', False)
    pp=p.show()
    if pp:
      ipNode=p.value('IP node')
      openPanel=p.value('open panel')
    else:
      return
  if 'Remove'==ipNode:
    removeExistingNode()
    return
  makeViewerNode(ipNode, openPanel)
  nuke.activeViewer().node().knob('input_process').setValue(True)

def makeViewerNode(ipNode, openPanel):
    removeExistingNode()
    if 'Mirror'== ipNode:
      n=mirrorIP(openPanel)
    elif 'Normalize'== ipNode:
      n=normalizeIP(openPanel)
    elif 'Grid'== ipNode:
      n=gridIP(openPanel)
    elif 'Saturation'== ipNode:
      n=saturationIP(openPanel)
    elif 'Over Checkerboard'== ipNode:
      bg='CheckerBoard2'
      n=overIP(bg, openPanel)
    elif 'Over 18% Grey'== ipNode:
      bg='Constant'
      n=overIP(bg, openPanel)

    n['name'].setValue('VIEWER_INPUT')
    n['label'].setValue(ipNode)
    return

def removeExistingNode():
    for i in nuke.allNodes():
        i['selected'].setValue(False)
        if 'VIEWER_INPUT' == i['name'].value():
            print 'deleting old viewer input node'
            i['selected'].setValue(True)
            nukescripts.node_delete(popupOnError=True)

def mirrorIP(openPanel=False):
  n=nuke.createNode('Mirror', inpanel=openPanel)
  n['Horizontal'].setValue(True)
  return n

def gridIP(openPanel=False):
  n=nuke.createNode('Grid', inpanel=openPanel)
  return n
  
def saturationIP(openPanel=False):
  hsv=nuke.createNode('Colorspace', inpanel=False)
  shuf=nuke.createNode('Shuffle', inpanel=False)
  
  hsv['colorspace_out'].setValue('HSV')
  hsv['selected'].setValue(True)
  
  shuf['red'].setValue('green')
  shuf['green'].setValue('green')
  shuf['blue'].setValue('green')

  hsv['selected'].setValue(True)
  shuf['selected'].setValue(True)
  
  n=nuke.collapseToGroup(show=openPanel)
  return n
  
def overIP(bg, openPanel=False):
  BG=nuke.createNode(bg, inpanel=False)
  MG=nuke.createNode('Merge2', inpanel=False)
  MG.setInput(1,None)
  MG.setInput(0, BG)
  
  if 'Constant'==bg:
    BG['color'].setValue((0.18,0.18,0.18,0))

  BG['selected'].setValue(True)
  MG['selected'].setValue(True)
  n=nuke.collapseToGroup(show=openPanel)

  return n



def normalizeIP(openPanel=False):
  nDot=nuke.createNode('Dot', inpanel=False)
  maxD=nuke.createNode('Dilate', inpanel=False)
  minD=nuke.createNode('Dilate', inpanel=False)
  maxBB=nuke.createNode('CopyBBox', inpanel=False)
  minBB=nuke.createNode('CopyBBox', inpanel=False)
  fromMinMax=nuke.createNode('Merge2', inpanel=False)
  fromMinIn=nuke.createNode('Merge2', inpanel=False)
  mDivide=nuke.createNode('Merge2', inpanel=False)

  maxD.setInput(0,nDot)
  minD.setInput(0,nDot)
  maxBB.setInput(0,maxD)
  maxBB.setInput(1,nDot)
  minBB.setInput(0,minD)
  minBB.setInput(1,nDot)
  fromMinMax.setInput(0,maxBB)
  fromMinMax.setInput(1,minBB)
  fromMinIn.setInput(0,nDot)
  fromMinIn.setInput(1,minBB)
  mDivide.setInput(0,fromMinMax)
  mDivide.setInput(1,fromMinIn)

  maxD.setName('DilateMax')
  maxD['size'].setExpression('max(input.format.w, input.format.h)')
  minD.setName('DilateMin')
  minD['size'].setExpression('-max(input.format.w, input.format.h)')
  fromMinMax['operation'].setValue('from')
  fromMinIn['operation'].setValue('from')
  mDivide['operation'].setValue('divide')


  nDot['selected'].setValue(True)
  maxD['selected'].setValue(True)
  minD['selected'].setValue(True)
  maxBB['selected'].setValue(True)
  minBB['selected'].setValue(True)
  fromMinMax['selected'].setValue(True)
  fromMinIn['selected'].setValue(True)
  mDivide['selected'].setValue(True)

  n=nuke.collapseToGroup(show=openPanel)

  return n


  
  
#viewerInput(ipNode='Grid')   #set a few presets through ipNode

























