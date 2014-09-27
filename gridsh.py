import json, paramiko, re, sys
"""
server = this software that will be handling the commands
node = the ssh servers that will be running the commands, supplying processing

I just thought I'd clarify this, because in many cases, the server will
be acting as a client of the nodes, and using the term 'client' would get
confusing.

"""
class nodeObj:
	def __init__(self, node):
		self.host = node['host']
		self.port = node['port']
		self.user = node['user']
		self.pasw = node['pass']
		self.ssh  = None
	def getSpeed(self):
		#connect to host
		#send command to get the host to time a single FLOP
		##We're going to use the bogoMips system instead
		output = self.runCommand("grep bogomips /proc/cpuinfo")['stdout'].read()
		bogoMips = 0.0
		for proc in output.splitlines():
			bogoMip = float(re.match("^bogomips\s+:\s(\d+\.\d+)", proc).group(1))
			bogoMips += bogoMip
		#possibly times this value by the system load?
		##We're going to divide it, because bigger is better in bogoMips
		load = self.runCommand("uptime")['stdout'].read()
		load = float(re.match("^.+load\saverage:\s\d+\.\d+,\s(\d+\.\d+),\s\d+\.\d+$", load).group(1))
		if load == 0.0:
			load = 0.009
		speed = bogoMips / float(load / len(output.splitlines()))
		return speed

	def runCommand(self, command):
		##if no session was supplied
		if self.ssh == None:
			#connect to node.user@node.host:node.port with ssh
			paramiko.util.log_to_file('ssh.log')
			self.ssh = paramiko.SSHClient()
			self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.ssh.load_system_host_keys()
			self.ssh.connect(self.host, username=self.user, password=self.pasw)
		#run command
		stdin, stdout, stderr = self.ssh.exec_command(command)
		output = {
			"stdin"	: stdin,
			"stdout": stdout,
			"stderr": stderr,
			"ssh"	: self.ssh
			}
		return output

def getNodes():
	try:
		f = open('./nodes.json', 'r')
	except:
		quit("[E] node config file ./nodes.json not found.\n\
			Use nodes.json.template as a guide, and fill it with\
			your nodes' credentials.")
	rawJson = f.read()
	f.close()
	try:
		nodesJson = json.loads(rawJson)
	except:
		quit("[E] Invalid JSON in nodes.json")
	nodes = []
	for index, node in enumerate(nodesJson):
		#attempt to connect to node
		nodeObject = nodeObj(node)
		if "-d" in sys.argv:
			print "[ ] Testing node %s of %s (%s@%s:%s)"%(index, len(nodesJson), nodeObject.user, nodeObject.host, nodeObject.port)
		output = nodeObject.runCommand('echo "Hello World"')
		if output['stdout'].read() == "Hello World\n":
			nodeObject.ssh = output['ssh']
			nodes.append(nodeObject)
			if "-d" in sys.argv:
				print "[+] Node %s loaded successfully"%(index)
		else:
			nodesJson.remove(node)
			if "-d" in sys.argv:
				print "[-] Node %s failed, and was removed"%(index)
		#remove from the list if it fails
	return nodes

def parseCommand(rawCommand):

	"""
	Gridsh has special commands called KeyCommands. KeyCommands are used
	to specify special tasks that you want Gridsh to perform. The syntax
	of these commands match '\w+:?.*!'. Anything that matches \1 in 
	'(\w+)(:|!)' is called a KeyWord. Anything matching \1 in '\w+:?(.*)!'
	is called a KeyCommand argument.

	example$ if:./*! of:arc.7z! 7z a +of +if
	Note: the values assigned to KeyWords can be used again in the command
		to save retyping by prepending the KeyWord with a '+'. This is
		optional.

	example$ verbose! example! testValue:10! echo "Hello World";
	Note: KeyCommands can consist of only KeyWords.

	"""
	keyCommands = re.findall('\w+:?.*!', rawCommand)
	args = []
	for keyCommand in keyCommands:
		word = re.search('^\w+(:|!)', keyCommand).group(0)
		word = word[:-1]
		arg  = re.search('.+!$' , keyCommand).group(0)
		arg  = arg[ :-1]
		args.append({"word": word, "arg":arg})
		rawCommand = rawCommand.replace(keyCommand, '' )
		rawCommand = rawCommand.replace('+' + word, arg)
	return rawCommand, args

def commandHandler(nodes):
	#get command from client
	command = raw_input("$ ")
	##parse command into keywords
	command, args = parseCommand(command)
	#iterate keywords and execute their meaning
	for arg in args:
		if arg['word'] == 'exit':
			quit()
	print args
	print command
	#find suitable node
	speeds = []
	##iterate through nodes
	for node in nodes:
		##make a list of the current speed of the node
		speeds.append(node.getSpeed())
	##Choose the node with the fastest speed
	node = nodes[speeds.index(max(speeds))]
	#run command on node
	#get output of command
	output = node.runCommand(command)
	return output['stdout'].read()
	
#make list of working nodes
if "-d" in sys.argv:
	print "[ ] Enumerating nodes"
nodes = getNodes()
if "-d" in sys.argv:
	print "[+] Loaded %s nodes sucessfully"%(len(nodes))
while 1:
	print commandHandler(nodes)
#for node in nodes:
#	print node.getSpeed()

