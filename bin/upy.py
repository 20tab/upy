"""
Contains the script that create a upy project 
"""
import os
import shutil


def search_set():
    """
    Return path's name that contains all necessary files for upy project initialization
    """
    THIS_PATH = os.path.realpath(os.path.dirname(__file__)) 
    dirname = os.path.abspath(os.path.join(THIS_PATH, '../../upy/bin/upy_project_set'))
    return dirname

def q_venv():
    """
    It asks to user if he want create virtualenv
    """
    q = raw_input("Do you want install a virtualenv? (y/n): ")
    if q == "y":
        return True
    elif q == "n":
        return False
    else:
        print "Tap y or n"
        return q_venv()

def venv_location():
    """
    It asks to user to tap the virtualenv destination as relative path from current position
    """
    q = raw_input("Tap venv's location (also with relative position): ")
    if not os.path.exists("%s" % q):
        return q
    else:
        print "The directory with the name '%s' exists." % q
        return venv_location()


def create_project():
    """
    It creates upy project
    """
    name = raw_input("Insert project name: ")
    dirname = search_set()
    listing = []
    if os.path.exists(dirname):
        listing = os.listdir(dirname)
    
    if os.path.exists("%s" %(name)):
        print "Project already exists!"
    else:
        try:
            os.mkdir(name)
            os.makedirs("%s/templates/admin" % name)
            print "Configuring project!"
            print "Copying files: "
            print listing
            for f in listing:
                if os.path.isdir("%s/%s" % (dirname,f)):
                    shutil.copytree("%s/%s" % (dirname,f),'%s/%s' % (name,f))
                elif f[-3:] != "pyc" or f[-3:] != "svn":
                    shutil.copy2('%s/%s' % (dirname,f), '%s/%s' % (name,f))
        except Exception, e:
            print e
            print "Something is going wrong!"
        else:
            if q_venv():
                venv_loc = venv_location()
                os.system("virtualenv %s" % venv_loc)
                os.system("%s/bin/pip install django" % venv_loc)
                os.system("%s/bin/pip install django-mptt" % venv_loc)
                os.system("%s/bin/pip install django-imagekit" % venv_loc)
            print "Project configured!"  
        
            

create_project()