Gridsh
======

A bash shell that will take a list of ssh servers and use them to distribute the workload of your
commands.

The scenario I imagined is if you have a collection of machines, and you wanted to be able to quickly
identify a machine that is most suitable to taking on new work and complete a command using that machine,
while you get instantly returned to the shell, ready to run more commands and to be notified when tasks
have finished.

###This software aims to fix the troubles of doing this manually by:
- Using an algorithm (time to compute a FLOP * decimal system load) to determine suitable machines
- Almost seemlessly allowing you to upload and download required files to and from the node
- Allowing you to see real time data on the tasks being run on all machines

Jargen Index
------------
I just thought I'd clarify this, because in many cases, the server will be acting as a client of the
nodes, and using the term 'client' would get confusing. I also offer a new command injection system
to specify the way these commands are to be run.

- Server              = this software that will be handling the commands
- Node                = the ssh servers that will be running the commands, supplying processing
- KeyCommands         = used to specify special tasks that you want Gridsh to perform. The syntax of these commands match '\w+:?.*;'
- KeyWord             = Anything that matches \1 in '(\w+)(:|;)'
- KeyCommand argument = Anything matching \1 in '\w+:?(.*);'

```
example$ if:./*; of:arc.7z; 7z a +of +if
```
Note: the values assigned to KeyWords can be used again in the command
to save retyping by prepending the KeyWord with a '+'. This is
optional.

```
example$ verbose; example; testValue:10; echo "Hello World";
```
Note: KeyCommands can consist of only KeyWords.


