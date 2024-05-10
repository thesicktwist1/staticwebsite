from textnode import TextNode
import os
import shutil
from copy_static import copy_static
src_path = "/root/workspace/github.com/thesicktwist1/staticwebsite/src"
dst_path = "/root/workspace/github.com/thesicktwist1/staticwebsite/public"

def main():
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    copy_static(src_path,dst_path)



 

main()

