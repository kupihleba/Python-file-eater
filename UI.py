class Controller:
    def __init__(self):
        pass

    def show_welcome(self):
        print("""Welcome to python file eater!
        Enter the directory you want to scan""")

    def get_path(self):
        return input('Path: ')

    def show_finished(self):
        print('==  FINISHED  ==')

    def show_finisher(self, time):
        print('==  FINISHED  ==')
        print('Runtime:\t', time, 's')

    def show_files_info(self, lst):
        print('Files to be scaned -', len(lst))

    def show_same_files(self, fileA, fileB):
        print('***  SAME FILES  ***')
        print('fileA:', fileA)
        print('fileB:', fileB)
