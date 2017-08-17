import hashlib
import os
import threading
import time
import timeit

import UI

IGNORE_EXTENSIONS = ['.ini', '.tlog', '.xml', '.hpp', '.ico', '.config', '.resx', '.manifest', '.cache']
IGNORE_PATHS = []
DELETE_FROM_DIR = ''
IGNORE_HIDDEN = True
AUTOREMOVE_COPIES = False
THREADS = 4

d = dict()  # Hashes are here
ui = UI.Controller()
lst_of_files = []  # all full file paths
threads = []
conflict_files = []  # queue of conflict files
running = True  # hopefully it is atomic

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


def ignore_case(filename):
    if IGNORE_HIDDEN and filename[0] == '.':
        return True
    if os.path.splitext(filename)[1] in IGNORE_EXTENSIONS:
        return True
    return False


def same_files(fileA, fileB, hash):
    ui.show_same_files(fileA, fileB)
    del_ok = input('Which file to delete? Enter A/B  -  ')
    try:
        if del_ok == 'A':
            os.remove(fileA)
            print(fileA, 'deleted')
        elif del_ok == 'B':
            print(fileB, 'deleted')
            os.remove(fileB)
            d.update({hash: fileB})
        else:
            print('IGNORED')
    except PermissionError:
        print('No permissions to delete file!')


def get_list_of_files(path):
    lst = []
    for root, subdirs, files in os.walk(path):  # for every folder and file in the directory
        for filename in files:
            if ignore_case(filename): continue
            lst.append(os.path.join(root, filename))
    ui.show_files_info(lst)
    return lst


def span_checking_threads(numb_of_threads):
    lst = []
    # walk_through()
    # return lst
    for i in range(numb_of_threads):
        thread = threading.Thread(target=walk_through)
        lst.append(thread)
        thread.start()
    return lst


def finish():
    for i in threads:
        i.join()
    # ui.show_finished()
    global running
    running = False


def walk_through():
    while lst_of_files:
        addr = lst_of_files.pop()
        try:
            cnt = False

            for i in IGNORE_PATHS:  # HARDCODE!
                if i in addr:  # TODO
                    cnt = True
                    break
            if cnt: return

            h = sha(addr)  # get hash of the file
            conflict = d.get(h)  # try to get the element
            if conflict == None:  # if no element was found - update dict
                d.update({h: addr})
            else:
                # if force_delete(addr, conflict, d, h):
                #    continue
                conflict_files.append([addr, conflict, h])

        except PermissionError:
            print('no permission to check/delete file', addr)
    global running
    running = False


if __name__ == '__main__':
    d.clear()
    ui.show_welcome()
    path = ui.get_path()

    start = timeit.default_timer()
    print('Getting files to scan ...')
    lst_of_files = get_list_of_files(path)
    print('Spanning', THREADS, 'threads')
    threads = span_checking_threads(THREADS)
    while conflict_files or running:
        if conflict_files:
            fileA, fileB, hash = conflict_files.pop()
            same_files(fileA, fileB, hash)
        else:
            time.sleep(1)

    finish()
    stop = timeit.default_timer()
    ui.show_finisher(stop - start)

    while conflict_files:
        fileA, fileB, hash = conflict_files.pop()
        same_files(fileA, fileB, hash)

        # Path: D:\
        # Files to be scaned - 778821
        # ==  FINISHED  ==
        #Runtime:	 201.0480578247407 s
#
