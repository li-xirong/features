import sys, os

from util import checkToSkip
from optparse import OptionParser

FILTER_SET = set(str.split(".jpg .png .bmp"))


    
def process(options, collection):
    rootpath = options.rootpath
    overwrite = options.overwrite
    
    resultfile = os.path.join(rootpath, collection, "id.imagepath.txt")
    
    if checkToSkip(resultfile, overwrite):
        return 0

    imageFolders = [os.path.join(rootpath, collection, 'ImageData')]
    filenames = []
    imageSet = set()
    
    for imageFolder in imageFolders:
        for r,d,f in os.walk(imageFolder):
            for filename in f:
                name,ext = os.path.splitext(filename)
                if ext not in FILTER_SET:
                    continue
                    
                if name in imageSet:
                    print ("id %s exists, ignore %s" % (name, os.path.join(r,filename)))
                    continue
                    
                imageSet.add(name)
                filenames.append("%s %s" % (name, os.path.join(r, filename)))
    try:            
        os.makedirs(os.path.split(resultfile)[0])
    except:
        pass

    fout = open(resultfile, "w")
    fout.write("\n".join(filenames) + "\n")
    fout.close()
    
    idfile = os.path.join(rootpath, collection, "ImageSets", '%s.txt' % collection)
    try:            
        os.makedirs(os.path.split(idfile)[0])
    except:
        pass           
    fout = open(idfile, "w")
    fout.write("\n".join(sorted(list(imageSet))) + "\n")
    fout.close()


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
      

        