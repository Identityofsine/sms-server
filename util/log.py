import sys

def log(msg: str):
	#check if -v flag is set
	if "--debug" in sys.argv:
		print(msg)

def stdout(msg: str):
	print(msg, file=sys.stdout)
	# clear the buffer
	sys.stdout.flush()

def error(msg: str):
	print("{error:\"" + msg + "\"}", file=sys.stderr) 
	pass
