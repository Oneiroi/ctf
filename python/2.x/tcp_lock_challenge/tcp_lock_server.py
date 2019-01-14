#!/usr/bin/env python2

import SocketServer
from time import time
import random

"""
Basic TCP server which requires the participant to respond to the challenge questions quickly and accurately.

__author__ == "David Busby <oneiroi@fedoraproject.org>"
"""

#the FLAG to return on completion of all challenges, you should also set this in your CTF platform for the participant to score
FLAG = 'CHANGEME'

#DICT of questions : answers
#You can comment out all but one question to test the operational flow
CHALLENGES = {
  '2x2 = ?' : 4,
  '32*16 = ?': 512,
  '2^52 = ?' : 4503599627370496,
  'yellow + blue = ?' : 'green',
  'red + yellow = ?' : 'orange',
  '2^52 / 2^51 = ?' : 2,
  'Follow the white ?' : 'rabbit',
  'north south ? west' : 'east',
  'whiskey tango ?' : 'foxtrot'
}


class MyTCPHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.terminated = ['You died!', 
                'WASTED', 
                'You loose! Good day sir!', 
                'End of line ...', 
                "You're terminated!", 
                'Asta la vista, baby',
                'Only human.',
                'Dodge this.']
        self.response_limit = 1.0
        self.ticker = 0
        self.request = request
        self.client_address = client_address
        self.server = server
        print("Connection from", self.client_address) #debug information for the administrator, shows tcp connection successful
        self.todo = []
        #produce the list of questions
        for i in CHALLENGES:
            self.todo.append(i)
        self.handle()

    def handle(self):
        #handle the incoming connection
        self.request.sendall("Hello %s your challenges follow, answer them _very_ quickly, or the trap will spring!\n" % self.client_address[0])

        while self.todo:
            #Run the loop while there are still questions to be asked, this relies on self.challenge() to pop (remove) run questions from the list
            self.challenge()
            self.ticker = time()
            self.rx = self.request.recv(1024).strip()
            
            if not self.validate():
                break
            else:
                continue
        #ig we are outside the loop we can presume completion and write the flag out
        self.request.sendall("Congratulations here is the flag!: %s\n" % FLAG)

    def challenge(self):
        #write the challenge question to the user and pop it from the list of questions
        self.tx = random.choice(self.todo)
        self.todo.pop(self.todo.index(self.tx))
        self.request.sendall("%s:" % self.tx)

    def validate(self):
        #validate the response for time exceeded and accuracy
        diff = time() - self.ticker
        if diff > self.response_limit:
            print "Time to RX exceeds limit %s" % diff
            self.request.sendall("%s\n\n" % random.choice(self.terminated))
            self.request.close()

        a = CHALLENGES[self.tx] #get the answer to the challenge
        rx = self.rx #get a copy of the received response

        if isinstance(a, int):
            #answer is an integer we should expect this in the response.
            try:
                rx = int(rx) #attempt type conversion of rx as it's always received as a string
            except ValueError:
                #if we could not convert set the value to None
                rx = None
        
        print "RX from %s got %r expected %r" % (self.client_address[0], rx, a) #debug for administrators to ensure the received response is the expected response
        if rx != a:
            #rx does not match expected answer a
            self.request.sendall("%s\n\n" % random.choice(self.terminated))
            self.request.close()
            return False
        else:
            return True

if __name__ == "__main__":
    server = SocketServer.TCPServer(('0.0.0.0',39842), MyTCPHandler)
    server.serve_forever()
