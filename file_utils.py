# borrowed from https://github.com/lengstrom/fast-style-transfer/blob/master/src/utils.py
import os

def get_files(img_dir):
    
    imgs = list_files(img_dir)
    return imgs

def list_files(in_path):

    img_files = []

    for (dirpath, dirnames, filenames) in os.walk(in_path):
        for file in filenames:
            filename, ext = os.path.splitext(file)
            ext = str.lower(ext)
            if ext == '.jpg' or ext == '.jpeg' or ext == '.gif' or ext == '.png' or ext == '.pgm':
                img_files.append(os.path.join(dirpath, file))

    return img_files