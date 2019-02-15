# tcp_lock_server.py

This provides a TCP server, listening on 39842/tcp.

This will prompt the connecting client to provide correct responses to each of the challeneges chosen at random.

An incorrect or late answer will result in disconnection, and failiure of the challenge.

If all challenges are solved without exceeding the time limit (self.response_limit) or submitting an incorrect answer, the server will write out the FLAG and disconnect the client.

If the time is excceded or an incorrect response received the server will write out a message from the self.terminated list, and close the connection.

*NOTE* update the tcp_lock_server.py file with the FLAG you want to return you can also tweak timeout settings however ymmv 

## Solving this challenge

You will want to write a program which interprets the text sent from the server, and calculates / provides the correct response over the tcp connection to the server very quickly (think sub second).

You will also want to store the response and write it out to the console as this will aid debugging and allow you to see the flag once you have completed the challeneges.

This tests your scripting ability, it is by no means a practical security measure only a measure of ability to script to solve a particular problem.

*DO NOT* deploy this method to protect any asset, seriously ...

## This IS achieveable

It may appear to be impossible, however scripting to reply sub second and ensure accurate responses is key as this [![asciicast](https://asciinema.org/a/l1Ak2GOdeyfnkJ8u0awXHeTrn.svg)](https://asciinema.org/a/l1Ak2GOdeyfnkJ8u0awXHeTrn) shows.
