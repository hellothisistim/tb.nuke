# From Alexey Kuchinski
# Sourced from https://community.foundry.com/discuss/post/912109 on 6 May 2022

import nuke
def TrackToRoto():
    def TrackToRotoIn():
        panel=nuke.Panel("roto name")
        panel.addSingleLineInput("name","")
        panel.addBooleanCheckBox('create RotoPaint', False)
        panel.show()
        if panel.value("name") != '':
            name = panel.value("name").replace(' ', '_')
            #check for unique name
            nl = []
            for nn in nuke.allNodes():
                nl.append(nn.name())
            if name in nl:
                #not unique
                i = 1
                namei = name +'_'+ str(i)
                while namei in nl:
                    namei = name +'_'+ str(i)
                    i =i+1
                name = namei
            #check for unique name done

            kind = panel.value("create RotoPaint")

            track = nuke.selectedNode()
            if kind == 1:
                roto = nuke.nodes.RotoPaint()
            else:
                roto = nuke.nodes.Roto()
            x = int(track['xpos'].value())
            y = int(track['ypos'].value())
            roto.setXYpos(x,y+100)
            #roto['label'].setValue(track['label'].value())
            first = nuke.Root().knob('first_frame').getValue()
            first = int(first)
            last = nuke.Root().knob('last_frame').getValue()
            last = int(last)+1
            frame = first
            Knobs = roto['curves']
            root=Knobs.rootLayer
            transform = root.getTransform()


            roto['name'].setValue(name)
            roto['tile_color'].setValue(11632127)

            roto.setSelected(True)
            track.setSelected(False)
            while frame<last:
                r = track['rotate'].getValueAt(frame,0)
                rr = transform.getRotationAnimCurve(2)
                rr.addKey(frame,r)
                tx = track['translate'].getValueAt(frame,0)
                translx = transform.getTranslationAnimCurve(0)
                translx.addKey(frame,tx)
                ty = track['translate'].getValueAt(frame,1)
                transly = transform.getTranslationAnimCurve(1)
                transly.addKey(frame,ty)
                sx = track['scale'].getValueAt(frame,0)
                ssx = transform.getScaleAnimCurve(0)
                ssx.addKey(frame,sx)
                sy = track['scale'].getValueAt(frame,1)
                ssy = transform.getScaleAnimCurve(1)
                ssy.addKey(frame,sy)
                cx = track['center'].getValueAt(frame,0)
                ccx = transform.getPivotPointAnimCurve(0)
                ccx.addKey(frame,cx)
                cy = track['center'].getValueAt(frame,1)
                ccy = transform.getPivotPointAnimCurve(1)
                ccy.addKey(frame,cy)
                frame = frame+1

    try:
        tracker = nuke.selectedNode()
        if "Tracker"in tracker.Class():
            TrackToRotoIn()
        else:
            tra = nuke.selectedNode()
            rot = nuke.createNode("Roto")
            x = int(tra['xpos'].value())
            y = int(tra['ypos'].value())
            rot.setXYpos(x,y+50)
            rot['hide_input'].setValue(0)
    except:
        nuke.createNode("Roto")

TrackToRoto()
