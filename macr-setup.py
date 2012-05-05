#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
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


def cConf():
    conf = open('/etc/macr/macr.conf', 'a')

    interface = input('Interface (eth0): ')
    if interface is '':
        conf.write('interface = eth0\n\n')
    else:
        line = str('interface = ' + interface + '\n\n')
        conf.write(line)

    prolist = input('Profile list (/usr/share/macr/profiles): ')
    if prolist is '':
        os.system('cp profiles /usr/share/macr/profiles')
        conf.write('profilelist = /usr/share/macr/profiles\n\n')
    else:
        line = str('profilelist = ' + prolist + '\n\n')
        conf.write(line)

    vlist = input('Vendor list (/usr/share/macr/manuf): ')
    if vlist is '':
         os.system('cp manuf /usr/share/macr/manuf')
         conf.write('vlist = /usr/share/macr/manuf\n\n')
    else:
        line = str('vlist = ' + vlist + '\n\n')
        conf.write(line)

    os.system('cp macr /usr/local/bin/macr')

    conf.close()
    print('Macr installed')
    exit(0) 

def dConf():
    print('copying files...')
    os.system('cp macr.conf /etc/macr/macr.conf')
    os.system('cp profiles /usr/share/macr/profiles')
    os.system('cp manuf /usr/share/macr/manuf')
    os.system('cp macr /usr/local/bin/macr')

    print('Macr installed')
    exit(0)

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
    if sys.version_info[0] == 3 and sys.version_info[1] == 2:
        print('Python version', sys.version_info[0:3], 
              'should be sufficient')
    else:
        print('It appears that you are not using python3.2 ')
        print('Macr will only work on python3.2 or later.')
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

        makeConf = input('Would you like make a custom conf file(Y/n): ')
        if makeConf == 'y' or makeConf == 'Y' or makeConf == 'yes':
            print('Making custom conf file.')
            cConf()
        else:
            print('Using default conf file.')
            dConf()  
        
        
    if arg.uninstall is True:
        print('Uninstalling macr...')
        os.system('rm -R /etc/macr')
        os.system('rm  -R /usr/share/macr')
        os.system('rm /usr/local/bin/macr')
        
        print('Macr uninstalled')
        exit(0)
    
    print('install by typeing: "sudo macr-setup.py --install"')
    
        
    return 0

if __name__ == '__main__':
    main()

