

import sys, os, time

from util import checkToSkip
from optparse import OptionParser

def printMessage(message_type, trace, message):
    print ('%s %s [%s] %s' % (time.strftime('%d/%m/%Y %H:%M:%S'), message_type, trace, message))

        
def process(options, collection):
    rootpath = options.rootpath
    overwrite = options.overwrite

    imagepathFilename = os.path.join(rootpath, collection, "id.imagepath.txt")
    if not os.path.exists(imagepathFilename):
        print ('%s does not exist' % imagepathFilename)
        return 0

    
    try:
        os.makedirs(os.path.split(resultFilename)[0])
    except:
        pass
      
    done = 0
    
    for line in open(imagepathFilename):
        if not line.strip():
            continue
        name,fullpath = str.split(line.strip())
        resultfile = fullpath.replace('ImageData', 'ImageData256x256')
        if checkToSkip(resultfile, overwrite):
            continue
        try:
            os.makedirs(os.path.split(resultfile)[0])
        except:
            pass
            
        # The '>' flag is to only apply the resize to images 'greater than' the size given  
        cmd = "convert %s -resize '256>x256>' %s" % (fullpath, resultfile)        
        os.system(cmd)
        done += 1
        if done % 100 == 0:
            printMessage("info", "image_rescale", "%d done" % done)
    # done
    printMessage("info", "image_rescale", "%d done" % done)  
    return done 


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = OptionParser(usage="""usage: %prog [options] collection""")
    parser.add_option("--overwrite", default=0, type="int", help="overwrite existing file (default=0)")
    parser.add_option("--rootpath", default='./', type="string", help="rootpath")

    (options, args) = parser.parse_args(argv)
    if len(args) < 1:
        parser.print_help()
        return 1

    return process(options, args[0])

if __name__ == "__main__":
    sys.exit(main())

    
    