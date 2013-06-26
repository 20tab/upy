#!/usr/bin/python
import os
from project import config
from optparse import OptionParser

def alias(name):
    if not os.path.exists(config.UWSGI_INI):
        print "UPY improperly configured: %s doesn't exists." % config.UWSGI_INI
    pil_lib = None
    virtualenv = None
    for line in open(config.UWSGI_INI):
        line = line.strip()
        if line[:7] == "pil_lib":
            pil_lib = line[7:].replace("=","").replace(" ","")
        if line[:10] == "virtualenv":
            virtualenv = line[10:].replace("=","").replace(" ","")
            if "%d" in virtualenv:
                virtualenv = virtualenv.replace("%d","%s/" % os.path.dirname(os.path.abspath(config.UWSGI_INI)))
            if virtualenv[-1:] == "/":
                virtualenv=virtualenv[:-1]
    command = 'alias %s="PYTHONPATH=%s %s/bin/python"' % (name,pil_lib,virtualenv)
    print command 
        
def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-a",
                      action="store_true",
                      dest="alias",
                      default=False,
                      help="create alias")
    parser.add_option("-n", "--name",
                      action="store",
                      dest="name",
                      default="",
                      help="Alias' name for python command for this project",)
    (options, args) = parser.parse_args()
    if options.alias:
        if options.name:
            alias(options.name)
        else:
            parser.error("-a option needs -n option")
    else:
        parser.error("Wrong number of arguments!")
    
if __name__ == '__main__':
    main()