import sys

def log(msg: str):
	#check if -v flag is set
	if "-v" in sys.argv:
		print(msg)
