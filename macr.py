#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
#    macr - Randomizes MAC Addresses and much more
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


import binascii
import fcntl 
import os
import random
import socket
import struct

# Debugging
debug_out = False
#debug_out = True

# ioctl numbers
SIOCGIFHWADDR = 0x8927 #get mac address
SIOCSIFHWADDR = 0x8924 #set mac address

SIOCGIWMODE = 0x8B07 #get operation mode
SIOCSIWMODE = 0x8B06 #set operation mode

SIOCGIFFLAGS = 0x8913 #get flag
SIOCSIFFLAGS = 0x8914 #set flag


###########################Class Interface##############################
class interface:

    def __init__(self, newMac, name):
        self.soc = socket.socket(socket.AF_UNIX, socket.SOCK_RAW)
        self.name = name
        self.oldMac = self.get()
        self.newMac = newMac


    def get(self):
        """ Gets the old mac address of the interface 
		    and returns is in a standard format. 
        """
        raw = fcntl.ioctl(self.soc.fileno(), SIOCGIFHWADDR,  
                          struct.pack('16s240x', 
                          self.name[:15].encode('ascii')))
        macS1 = binascii.hexlify(raw[18:24]).decode('utf-8')
        macS1 += '     '
        macS2 = ''
        for i in range(17):
            macS2 += macS1[i]
            if i in range(1,12,2):
                macS2 += ':'
        return macS2[0:17]
  
  
    def set(self):
        """ Sets the new mac address """
        self.stateToggle('down')
        try:
            opModeSwitched = False
            if self.getOpMode() == b'06':
                opModeSwitched = True
                self.setOpMode('managed')
        except IOError:
            pass 
        macS2 = ''
        for i in range(17):
            if self.newMac[i] != ':':
                macS2 += self.newMac[i]
        macS3 = binascii.unhexlify(macS2.encode('ascii'))
        fcntl.ioctl(self.soc.fileno(), SIOCSIFHWADDR, 
                    struct.pack('16sH12s226x',
                    self.name.encode('ascii'), 1, macS3))
        try:
            if opModeSwitched == True:
                self.setOpMode('monitor')
        except IOError:
            pass 
        self.stateToggle('up')


    def stateToggle(self, toggle):
        """ Toggles the state of the interface. Up or down depending on
		    the argument.
        """
        if toggle is 'up':
            fcntl.ioctl(self.soc.fileno(), SIOCSIFFLAGS,
                        struct.pack('16sH',
                        self.name.encode('ascii'), 4099))
        elif toggle is 'down':
            fcntl.ioctl(self.soc.fileno(), SIOCSIFFLAGS, 
                        struct.pack('16sH',
                        self.name.encode('ascii'), 4098))
    
    
    def getOpMode(self):
        """ Get wireless operation mode. """
        raw = fcntl.ioctl(self.soc.fileno(), SIOCGIWMODE,  
                          struct.pack('16sx', 
                          self.name[:15].encode('ascii')))
        return binascii.hexlify(raw[16:])
    

    def setOpMode(self, mode):
        """ Set wireless operation mode. """
        if mode is 'managed':
            fcntl.ioctl(self.soc.fileno(), SIOCSIWMODE,
                        struct.pack('16sH247x',
                        self.name[:15].encode('ascii'), 2))
        elif mode is 'monitor':
            fcntl.ioctl(self.soc.fileno(), SIOCSIWMODE,
                        struct.pack('16sH247x',
                        self.name[:15].encode('ascii'), 6))


    def display(self): 
        """ Checks if the old and new addresses are the same and 
            displays the new mac address
            
        """
        if self.newMac == self.oldMac:
             print('Mac address has not changed!')
             print(self.name + '\'s old addr =', self.oldMac)
             print(self.name + '\'s new addr =', self.newMac)
             print()
        print (self.name + ': ' + self.newMac)
                       

###########################Class Action#################################            

class Action:
    def __init__(self, confFile=None):
        if confFile is None:
           self.confFile = '/etc/macr/macr.conf'


    def showAddr(self, name):
        for i in name:
            iface = interface(None, i)
            print(i +  ':', iface.get())


    def chEnding(self, name):
        for i in name:
            iface = interface(None, i)
            iface.newMac = iface.get()[:8] + macRand()[8:]
            iface.set()
            iface.display()

    def chBeginning(self,  name):
        for i in name:
            iface = interface(None, i)
            iface.newMac = macRand()[:8]  + iface.get()[8:]
            iface.set()
            iface.display()


    def manufact(self, name, ouiName):
        for i in name:
            iface = interface(None, i)
            vlist = fileSearch('vlist', self.confFile)
            result = []
            for line in open(vlist, 'r', encoding='utf-8'):
                if line[:1] == '#':
                    pass
                elif ouiName.lower() in line[ 9 : len(ouiName)
                                                      + 9 ].lower():
                    result.append(line[:8])
            #print(result)
            iface.newMac = result[random.randrange(len(result))] + macRand()[8:]
            iface.set()
            iface.display()


    def manAddr(self, name, addr):
        for i in name:
            iface = interface(addr, i)
            if debug_out == True:
                print(iface.name + '\'s old addr =', iface.oldMac)
                print(iface.name + '\'s new addr = ', iface.newMac)
            iface.set()
            iface.display()

    def profile(self, name, profileName):
        for i in name:
            profilelist = fileSearch('profilelist', self.confFile)
            result = fileSearch(profileName.lower(), profilelist)
            iface = interface(result, i)
            iface.set()
            iface.display()


    def random(self, name):
        for i in name:
            iface = interface(macRand(), i)
            if debug_out == True:
                print(iface.name + '\'s old addr =', iface.oldMac)
                print(iface.name + '\'s new addr =', iface.newMac)
            iface.set()
            iface.display()
########################################################################

def macRand():
    """ returns a random mac address. """ 
    hex = {
           '0' : 0, '1' : 1, '2' : 2, '3' : 3,
           '4' : 4, '5' : 5, '6' : 6, '7' : 7,
           '8' : 8, '9' : 9, 'a' : 10,'b' : 11,
           'c' : 12,'d' : 13,'e' : 14,'f' : 15 
           }
    rawMac = ''
    for i in range(6):
        rawMac += ":%02x" % random.randrange(256)
        mac = rawMac[1:]
    if hex[mac[1]] % 2 is 0: 
        return mac 
    else:
        # from mac_spoof.py write by a5an0
        rawMac = '00'
        for i in range(5):
            rawMac += ":%02x" % random.randrange(256)
            mac = rawMac
        return mac

def fileSearch(key, name):
# file parser func
    for line in open(name, 'r', encoding='utf-8'):
        if line[:1] == '#':
            pass
        elif key in line[:len(key)] and line[len(key)] == '=':
            result = line[len(key) + 1:-1]
    return result


########################################################################


# vim: ai ts=4 sts=4 et sw=4 ft=python
