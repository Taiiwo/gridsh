import json, paramiko, re
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
		#possibly times this value by the system load?
		return timeTaken

	def runCommand(self, command):
		##if no session was supplied
		if self.ssh == None:
			#connect to node.user@node.host:node.port with ssh
			self.ssh = paramiko.SSHClient()
			self.ssh.connect(node.host, username=node.user, password=node.pasw)
		#run command
		stdin, stdout, stderr = self.ssh.exec_command(command)
		output = {
			"stdin"	: stdin,
			"stdout": stdout,
			"stderr": stderr,
			"ssh"	: ssh
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
	for node in nodesJson:
		#attempt to connect to node
		nodeObject = nodeObj(node)
		output = nodeObject.runCommand('echo "Hello World"')
		if output['stdout'] == "Hello World":
			nodeObject.ssh = output['ssh']
			nodes.append(nodeObject)
		else:
			nodesJson.remove(node)
		#remove from the list if it fails
	return nodes

def parseCommand(rawCommand):

	"""
	Gridsh has special commands called KeyCommands. KeyCommands are used
	to specify special tasks that you want Gridsh to perform. The syntax
	of these commands match '\w+:?.*;'. Anything that matches \1 in 
	'(\w+)(:|;)' is called a KeyWord. Anything matching \1 in '\w+:?(.*);'
	is called a KeyCommand argument.

	example$ if:./*; of:arc.7z; 7z a +of +if
	Note: the values assigned to KeyWords can be used again in the command
		to save retyping by prepending the KeyWord with a '+'. This is
		optional.

	example$ verbose; example; testValue:10; echo "Hello World";
	Note: KeyCommands can consist of only KeyWords.

	"""
	keyCommand = re.findall('\w+:?.*;', rawCommand)
	args = []
	for keyCommand in keyCommands:
		word = re.search('^\w+(:|;)', keyCommand)
		word = word[:-1]
		arg  = re.search('.+;$' , keyCommand)
		arg  = arg[ :-1]
		args["keyword"] = arg
		command.replace(keyCommand, '' )
		command.replace('+' + word, arg)
	return command, args

def commandHandler(nodes):
	#get command from client
	command = raw_input("$ ")
	##parse command into keywords
	command, args = parseCommand(command)
	#iterate keywords and execute their meaning
	#find suitable node
	speeds = []
	##iterate through nodes
	for node in nodes:
		##make a list of the current speed of the node
		speeds.append(node.getSpeed())
	##Choose the node with the fastest speed
	node = nodes[speeds.index(max(values))]
	#run command on node
	#get output of command
	output = node.runCommand(command)
	return output
	
#make list of working nodes
nodes = getNodes()
commandHandler(nodes)
