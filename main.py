import hashlib
import os

# import pyqt5

IGNORE_EXTENSIONS = ['.ini', '.tlog', '.xml', '.hpp', '.ico', '.config', '.resx', '.manifest', '.cache']
IGNORE_PATHS = ['']
DELETE_FROM_DIR = ""
IGNORE_HIDDEN = True
AUTOREMOVE_COPIES = False


def sha(file):
    h = hashlib.sha256()
    try:
        with open(file, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                h.update(chunk)
    except PermissionError:
        print('no permission to check file', file)
    return h.hexdigest()


def force_delete(addr, in_dict, d, h):
    if DELETE_FROM_DIR in addr:
        os.remove(addr)
        print(addr, 'deleted')
        return True
    elif DELETE_FROM_DIR in in_dict:
        os.remove(in_dict)
        d.update({h: addr})
        print(in_dict, 'deleted')
        return True
    return False


def walk_through(path):
    d = dict()
    addr = ''
    try:
        for root, subdirs, files in os.walk(path):
            for filename in files:
                if IGNORE_HIDDEN:
                    if filename[0] == '.':
                        continue
                    if os.path.splitext(filename)[1] in IGNORE_EXTENSIONS:
                        continue
                addr = os.path.join(root, filename)
                cnt = False
                for i in IGNORE_PATHS:
                    if i in addr:
                        cnt = True
                        break
                if cnt: continue
                h = sha(addr)
                conflict = d.get(h)
                if conflict == None:
                    d.update({h: addr})
                else:
                    # if force_delete(addr, conflict, d, h):
                    #    continue

                    print('***  SAME FILES  ***')
                    print('fileA:', addr)
                    print('fileB:', conflict)
                    del_ok = input('Which file to delete? Enter A/B  -  ')

                    if del_ok == 'A':
                        os.remove(addr)
                        print(addr, 'deleted')
                    elif del_ok == 'B':
                        print(conflict, 'deleted')
                        os.remove(conflict)
                        d.update({h: addr})
                    else:
                        print('IGNORED')
    except PermissionError:
        print('no permission to check/delete file', addr)


if __name__ == '__main__':
    print('Welcome to python file eater!')
    path = input('Enter path: ')
    walk_through(path)
    print('==  FINISHED  ==')
