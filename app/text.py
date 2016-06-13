import os

if 'louis' not in os.listdir(os.getcwd()):
    print "Making new directory louis in " + os.getcwd()
    os.mkdir(os.getcwd() + "/louis")
else:
    print "louis already is a directory here."
