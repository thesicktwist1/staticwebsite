
import os
import shutil

def copy_static(src,dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for s in os.listdir(src):
        source = os.path.join(src,s)
        dest = os.path.join(dst,s)
        if os.path.isfile(source):
            shutil.copy(source,dest)
        else:
            copy_static(source,dest)
    