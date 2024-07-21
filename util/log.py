import sys

def log(msg: str):
	#check if -v flag is set
	if "--debug" in sys.argv:
		print(msg)

def error(msg: str):
	print("{error:\"" + msg + "\"}") 
	pass
