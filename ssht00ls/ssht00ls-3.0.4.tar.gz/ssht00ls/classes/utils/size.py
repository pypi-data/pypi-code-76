import os, sys, fil3s
size = None
path = sys.argv[1]
if not os.path.exists(path):
	size = "does-not-exist"
else:
	size = Formats.FilePath(path).size(mode="MB")
print(size)