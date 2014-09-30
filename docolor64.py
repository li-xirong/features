import sys, os, time

from util import checkToSkip
from color64 import extractColor64
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

    resultFilename = os.path.join(rootpath, collection, "FeatureData", "color64", "id.feature.txt")
    if checkToSkip(resultFilename, overwrite):
        return 0

    try:
        os.makedirs(os.path.split(resultFilename)[0])
    except:
        pass
      
    done = 0  
    fout = open(resultFilename, "w")
    for line in open(imagepathFilename):
        if not line.strip():
            continue
        name,fullpath = str.split(line.strip())
        feature = extractColor64(fullpath)
        
        if feature:
            output = name + " " + " ".join([str(x) for x in feature])
            fout.write(output + "\n")
        done += 1
        if done % 100 == 0:
            printMessage("info", "docolor64", "%d done" % done)
    # done
    fout.close()        
    printMessage("info", "docolor64", "%d done" % done)  
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

    