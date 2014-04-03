

def printFiles():
		
	for n in nuke.allNodes():
	    if 'file' in n.knobs():
	        file = n.knob('file').value()
	        if file != '':
	            print n.name(), '\n\t', file


def relativeToScript(path):





def fooSortedFiles()
	files = []
	    
	for n in nuke.allNodes():
	    if 'file' in n.knobs():
	        file = n.knob('file').value()
	        if file != '':
	            files.append(file)

	return sorted(files)