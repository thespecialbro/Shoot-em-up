#! python
'''
Verifies that everything is working
with the file system and python modules
'''
def main():
    print('Importing modules:')
    import time
    import random
    import os
    import sys
    import shmup

    try:
        import pygame
    except ImportError:
        print('\tThis game requires Pygame to work!')
        time.sleep(5)
        raise SystemExit
    print('\tPygame module exists...')
    try:
        import config
    except ImportError:
        print('\tDid you remember to NOT delete the config.py file?')
        time.sleep(5)
        raise SystemExit
    print('\tConfig.py exists...')
    if config.menu:
        try:
            import pygbutton
        except ImportError:
            print('\tRequires Pygbutton module to work!')
            time.sleep(5)
            raise SystemExit
        print('Pygbutton module exists.\n')

    print('Testing Python version:')
    if sys.version_info[0] >= 3:
        if sys.version_info[1] >= 5:
            print('\tPython version is verified to be 3.5 or higher\n')
        elif sys.version_info[1] < 5:
            print('\tPython version is verified to be 3.x or higher\n')
    else:
        print('\tPython version is out of date!\nYou must use Python version 3 or higher!')
        time.sleep(5)
        raise SystemExit

    print('Testing Pygame version:')
    if pygame.version.ver != "1.9.2a0":
        print('''\tWARNING:
    \tThis version of pygame is not the version it was written in!
    \tSome features may not work the same!
    ''')
    else:
        print('\tPygame version is verified to be {}\n'.format(pygame.version.ver))

    file_num = 0
    dir_num = 0
    game_dir = os.path.dirname(__file__)
    for dir_name, subdir_list, file_list in os.walk(game_dir):
        dir_num += 1
        print('{} - Found directory: {}'.format(dir_num, dir_name))
        for fname in file_list:
            file_num += 1
            print('\t{}\t{}'.format(fname, file_num))

    print('\nfound {} directories and {} files'.format(dir_num, file_num))

if __name__ == '__main__':
    main()
