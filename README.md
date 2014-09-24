Gridsh
======

A bash shell that will take a list of ssh servers and use them to distribute the workload of your commands.

The scenario I imagined is if you have a collection of machines, and you wanted to be able to quickly
identify a machine that is most suitable to taking on new work and complete a command using that machine,
while you get instantly returned to the shell, ready to run more commands and to be notified when tasks
have finished.

This software aims to fix the troubles of doing this manually by:
- Using an algorithm (time to compute a FLOP * decimal system load) to determine suitable machines
- Almost seemlessly allowing you to upload and download required files to and from the node
- Allowing you to see real time data on the tasks being run on all machines
