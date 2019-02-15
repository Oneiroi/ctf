#!/usr/bin/env python2

"""
__author__ == 'David Busby oneiroi@fedoraproject.org'

This is for python 2.7.x, _if_ you opt for python 3 due to differences in socket handling
a lot of this code will no longer function.

"""
import socket
import re
import math
from contextlib import closing

CTF_LOCK_HOST = "ctf.oneiroi.co.uk" #You will want to set this to your ctf server
CTF_LOCK_PORT = 39842       #You will want to set this to your lock server port 
CTF_LOCK_TLS  = False        #Not used at this time, but planned for future ;-)

def TX(s, wut):
    #Single TX method, for transmit consistency
    if 'float' == wut.__class__.__name__:
        #lock exepects whole numbers
        wut = int(round(wut,0))
    #Debug output not what we are sending
    print("TX", wut)
    #s.send("%s\n"%wut)
    s.send("\x6c\x6f\x6c")

def pick_lock():
    #We need to get through each gate with the correct answer to reach the flag.
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        #using closing() as python2.x has some weird issues throwing AttributeError __exit__, this addresses that.
        s.connect((socket.gethostbyname(CTF_LOCK_HOST),CTF_LOCK_PORT)) #connect to TCP server
        while 1:
            #Ugly _AF_ program looping logic, #YOLO
            rx = s.recv(1024)
            if len(str(rx)) == 0:
                #Well we done messed up, unhandled question perhaps ?
                print ("GAME OVER ... continue ?")
                break
            if "Hello" in "{}".format(rx):
                #we need to discard the greeting banner...
                rx = b""
            rx = rx.strip() #trim any excess white space.
            if b'= ?' in rx:
                #only format question responses, we need the flag as is
                rx = rx[:-5]    #trim = ?: characters as eval does not handle this
                rx = rx.lower() #lower case for consistency e.g. x vs X
            print("RX {}".format(rx)) #Debug output what was received from server 
            #identify and respond
            if b'^' in rx: 
                #power notation, however eval does not handle this, sooo...
                #DIVERT ALL POWER TO REGEX!
                tx = re.sub("([0-9]+)\^([0-9]+)","math.pow(\\1,\\2))", str(rx))
                tx = eval(str(tx))
                TX(s, tx)
            elif b'x' in rx:
                #Multiplication notation, however python eval does not handle this, sooo...
                rx = str(rx) #convert to str
                rx = rx.lower().replace("x",'*') #use str formatting tooling
                tx = eval(rx.strip())
                TX(s, tx) 
            elif b'*' in rx:
                #Y U MIX SYNTAX SERVER?!
                tx = eval(rx)
                TX(s, tx) 
            elif b'yellow + blue' in rx:
                #We can not send logical questions to eval, we need to handle these seperately
                TX(s, "green")
            elif b'red + yellow' in rx:
                TX(s, "orange")
            elif b'Follow the white' in rx:
                TX(s, "gerbil") #Knock, knock, Neo.
            elif b'north south ? west' in  rx:
                TX(s, "east")
            elif b'whiskey tango' in rx:
                TX(s, "WTF") 
            elif b'Congrat' in rx:
                #Flag has been scored, our job is done here :)
                 break
        

def main():
    #Whatcha here for?! go pick_lock!
    pick_lock()

if __name__ == '__main__':
    main()