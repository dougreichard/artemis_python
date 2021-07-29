# Example web interaction
This demonstrates a Web Client that allows adding and removing enemies.

This takes some setup to run. Since it uses a library that doesn't common with stock python.

# Proof of concept
This is just a proof of concept for example sake.

# Setup

Specifically, the "websockets" python library needs to be installed.

I used a virtual environment (venv) in this directory, and in messaging.py function child_logic update the system path to point to it.

The index.html needs to be served. This is not coded, but I ran a separate server commandline tool.

# What it does
With all the peices in place it will run a seprate child process that sets up Webscoket communication.
The artemis script using queue to send and receive message using Queues to the child process
The child process uses websockets to forward message to/from the queues to a browser

index.html has a button to add enemies, and as enemies are added adds buttons to destory that enemy.




