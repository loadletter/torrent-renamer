#!/usr/bin/env python2
import os
import sys
from bencode import bdecode

def is_torrent(path):
	return os.path.isfile(path) and path.lower().endswith(".torrent")

def rename_file(path):
	try:
		with open(path, 'rb') as f:
			data = bdecode(f.read())
	except Exception as e:
		print >>sys.stderr, "Error decoding:", path, ":", e
	else:
		name = data['info']['name'] + '.torrent'
		newname = os.path.join(os.path.dirname(path), name)
		if os.path.isfile(newname):
			print >>sys.stderr, "Destination file alredy exists, ignoring:", path, "->", newname
		else:
			os.rename(path, newname)
	
def rename_dir(path):
	for f in os.listdir(path):
		p = os.path.join(path, f)
		if is_torrent(p):
			rename_file(p)

def main(paths):
	for path in paths:
		if is_torrent(path):
			rename_file(path)
		elif os.path.isdir(path):
			rename_dir(path)
		else:
			print >>sys.stderr, "Not a .torrent or directory:", path
	
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage:", sys.argv[0], "file.torrent [dir] ..."
		sys.exit(1)
	main(sys.argv[1:])
		
