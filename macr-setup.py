#!/usr/bin/python3
# -*- coding: utf-8 -*-
# macr:V0.5-D18-M10-Y11
#
#  macr-setup.py
#  
#    Copyright 2011  <Abirz Novem>
#  
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  

import argparse
import os
import sys


def main():
    
    print('Checking OS...')
    if os.uname()[0] == 'Linux':
        print('OS is Linux.')
    else:
        print('OS is', os.uname()[0])
        print('You know at this time macr only works')
        print('on linux but i would like to get it working')
        print('on freebsd and other systems.')
        exit(1, msg='OS is not Linux.')
        
        
    print('Checking Python version...')
    if sys.version_info[0] == 3:
        print('Python version', sys.version_info[0:3], 
              'sould be sufficient')
    else:
        print('It appears that you are not using python3 ')
        print('Macr will only work on python3')
        exit(1)
    
    parser = argparse.ArgumentParser(description='Macr installer.')
    parser.add_argument('--install', action='store_true',
                        dest='install', help='Install macr.')
    parser.add_argument('--uninstall', action='store_true',
                        dest='uninstall', help='Uninstall macr.')
    arg = parser.parse_args()
# We should be good to go.
    if arg.install is True:
        print('Installing macr...')
        
        print('Making directories...')
        os.makedirs('/etc/macr/')
        os.makedirs('/usr/share/macr/')
        
        print('copying files...')
        os.system('cp macr.conf /etc/macr/macr.conf')
        os.system('cp manuf /usr/share/macr/manuf')
        os.system('cp macr /usr/bin/macr')
        
        print('Macr installed')
        exit(0)
        
    if arg.uninstall is True:
        print('Uninstalling macr...')
        os.system('rm -R /etc/macr')
        os.system('rm  -R /usr/share/macr')
        os.system('rm -R /usr/bin/macr')
        
        print('Macr uninstalled')
        exit(0)
    
    print('install by typeing: "sudo macr-setup.py --install"')
    
        
    return 0

if __name__ == '__main__':
    main()

