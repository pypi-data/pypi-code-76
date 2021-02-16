import os, sys
status = None
path = sys.argv[1]
if not os.path.exists(path):
	status = "does-not-exist"
elif os.path.isdir(path):
	status = "directory"
else:
	status = "file"
print(status)