"""
Contains many common functions
"""
import os,time,re,datetime

def truncate(string, chars_number):
    """
    Truncates a string to the 'chars_number' character.
    """
    return string[:chars_number] + '..' if len(string) > chars_number else string

def datetimeToUnix(date):
    """
    Transform a datetime in unix format with milliseconds
    """
    return int(time.mktime(date.timetuple())*1000)

def datetimeToUnixSec(date):
    """
    Transform a datetime in unix format
    """
    return int(time.mktime(date.timetuple()))

def upy_re_match(regex,value):
    """
    Checks if value match with regex
    """
    reg = re.compile(regex)
    return reg.match(value)  

def now():
    """
    Returns datetime.datetime.now()
    """
    return datetime.datetime.now()

def today():
    """
    Returns datetime.date.today()
    """
    return datetime.date.today()

def compare_dicts(dict1, dict2):
    """
    Checks if dict1 equals dict2
    """
    for k,v in dict2.items():
        if v != dict1[k]:
            return False
    return True

def filter_files(path, string):
    """
    This function filter all files that contains the string passed as parameter in the name
    """
    try:
        listing = os.listdir(path)
        return [f for f in listing if string in f]
    except:
        raise ValueError("Error in upy.contrib.tree.menu @ filter_files()")
    
def clean_cache(path, string_in_filename = None):
    """
    Cleans files contain string_in_filename from path 
    """
    if string_in_filename:
        for tmpfile in filter_files(path,string_in_filename):
            os.unlink("%s%s" % (path,tmpfile))
    else:
        for tmpfile in os.listdir(path):
            os.unlink("%s%s" % (path,tmpfile))
            
def clean_path(source):
    """
    Replace backslashes from source.file_name with a slash 
    """
    source.file_name = source.file_name.replace('\\','/')
    return source

def getAccentedVocal(vocal,acc_type="g"):
    """
    It returns given vocal with grave or acute accent 
    """
    vocals = {'a':{'g':u'\xe0','a':u'\xe1'},
              'e':{'g':u'\xe8','a':u'\xe9'},
              'i':{'g':u'\xec','a':u'\xed'},
              'o':{'g':u'\xf2','a':u'\xf3'},
              'u':{'g':u'\xf9','a':u'\xfa'}}
    return vocals[vocal][acc_type]

def _av(vocal,acc_type="g"):
    """
    It's a shortcut to getAccentedVocal function
    """
    return getAccentedVocal(vocal,acc_type)