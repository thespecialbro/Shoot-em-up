#! python
'''
Verifies that everything is working
with the file system and python modules
'''
def main():
    print('Importing modules:')
    pygame_e = False
    config_e = False
    shmup_e = False
    pygbutton_e = False

    import time
    import random
    import os
    import sys
    print('\ttime\n\trandom\n\tos\n\tsys')

    print('\tSHMUP:')
    try:
        import SHMUP
    except ImportError:
        print('\t\tIs this test script in the same folder as SHMUP.py?')
        shmup_e = False
    else:
        print('\t\tSHMUP.py exists')
        shmup_e = True

    print('\tPygame:')
    try:
        import pygame
    except ImportError:
        print('\t\tThis game requires Pygame to work!')
        pygame_e = False
    else:
        print('\t\tPygame module exists')
        pygame_e = True

    print('\tConfig:')
    try:
        import config
    except ImportError:
        print('\t\tDid you remember to NOT delete the config.py file?')
        config_e = False
    else:
        print('\t\tconfig.py exists')
        config_e = True

    print('\tPygbutton:')
    if config.menu:
        try:
            import pygbutton
        except ImportError:
            print('\t\tRequires Pygbutton module to work!')
            pygbutton_e = False
        else:
            print('\t\tPygbutton module exists')
            pygbutton_e = True
    else:
        print('\t\tDid not attempt')

    print('\nWalking game directories:')
    file_num = 0
    dir_num = 0
    game_dir = os.path.dirname(__file__)
    dir_dict = {game_dir:[]}
    for dir_name, subdir_list, file_list in os.walk(game_dir):
        dir_num += 1
        dir_dict[game_dir].append(dir_name)
        for file_name in file_list:
            file_num += 1
            dir_dict[game_dir].append(file_name)

    print('\t{}'.format(dir_dict))
    print('Found {} directories and {} files'.format(dir_num, file_num))
    print('Finished walking directories.')

    print('\nVersion testing:')
    print('\tTesting Python version:')
    if sys.version_info[0] >= 3:
        if sys.version_info[1] >= 5:
            print('\t\tPython version is verified to be 3.5 or higher\n')
        elif sys.version_info[1] < 5:
            print('\t\tPython version is verified to be 3.x or higher\n')
    else:
        print('\t\tPython version is out of date!\nYou must use Python version 3 or higher!')
        time.sleep(5)
        raise SystemExit

    print('\tTesting Pygame version:')
    if pygame.version.ver != "1.9.2a0":
        print('''\t\tWARNING:
    \t\tThis version of pygame is not the version it was written in (1.9.2a0)!
    \t\tSome features may not work the same!
    ''')
    else:
        print('\t\tPygame version is verified to be {}\n'.format(pygame.version.ver))

    print('Shmup Version {}\nShmup Release {}\nShmup Version Number {}\n'.format(SHMUP.VERSION, SHMUP.RELEASE, SHMUP.VER_NUMBER))

if __name__ == '__main__':
    main()
