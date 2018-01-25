#!/usr/bin/env python3

# Program to clear the Netbeans Cache

# TODO: Do not delete anything that starts with *jython* (including subdirectories and directory contents).

import os
from sys import stderr, argv
from shutil import rmtree


def getVersion ():
	return "0.00.01"


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def clean_nb_cache(cache_dir, verbose):
	"""
	Given a directory containing the Netbeans cache structure, check that it has
	subdirectories and ask which one to clean, then delete all contents in 'index'
	"""
	total_dirs = 0
	subdirs = get_immediate_subdirectories(cache_dir)
	if len(subdirs) > 0:
		ask_dir = "For which version of NetBeans do you wish to clear caches?\nType the directory at the prompt (or leave blank for none), followed by <Enter>."
		for a_dir in subdirs:
			ask_dir = ask_dir + "\n\t" + a_dir
		ask_dir = ask_dir + "\n\t? "
		clean_dir = input(ask_dir).rstrip()
		if len(clean_dir) > 0:
			clean_full = os.path.join(cache_dir, clean_dir, "index")
			print("Cleaning " + clean_full + " ...")
			subdirs = get_immediate_subdirectories(clean_full)  # Don't want to delete index but its subdirectories
			for a_dir in subdirs:
				if str(a_dir).startswith("jython"):
					continue  # ignore jython directories
					if (verbose):
						print("Cleaning " + a_dir + " ...")
					total_dirs += 1
				rmtree(os.path.join(clean_full, a_dir), ignore_errors=True)  # Will delete the dir as well
				if (verbose):
					print ("Cleaning " + os.path.join(clean_full, a_dir) + " ...")
				total_dirs += 1
		else:
			print("No cache directory supplied!", file=stderr)
	else:
		print("Cannot find a netbeans version in " + cache_dir, file=stderr)
	print("Cleaning cache completed. (%s directories cleaned.)" % total_dirs)

def main(verbose):
	print("NetBeans Cache Cleaner [" + getVersion() + "]")
	print("\nPlease exit NetBeans if you haven't already ...\nSupply -v or --verbose for verbose output. Supply -V or --version for version information.\n")
	home_dir = os.getenv("HOME", "/home")  # Get the location of $HOME (UNIX)
	cache_dir = os.path.join(home_dir, ".cache", "netbeans")
	if os.path.isdir(cache_dir): # Get a list of directories in $HOME/.cache/netbeans/, assuming it exists
		clean_nb_cache(cache_dir, verbose)
	elif os.path.isdir(os.path.join(home_dir, ".netbeans", "cache")):  # Alternate cache location
		clean_nb_cache(os.path.join(home_dir, ".netbeans", "cache"), verbose)
	elif os.getenv("OS", "?").startswith("Windows") and len(os.getenv("USERPROFILE", "")) > 0: # NetBeans puts its cache in different location in home dir on Windows
		home_dir = os.getenv("USERPROFILE", "")  # Windows Equivalent of HOME
		cache_dir = os.path.join(home_dir, "AppData", "Local", "NetBeans", "Cache")
		if os.path.isdir(cache_dir):
			clean_nb_cache(cache_dir, verbose)
		else:
			print("Cannot find NetBeans cache in " + cache_dir, file=stderr)
	else:
		print("Cannot find NetBeans cache in " + cache_dir, file=stderr)
# Ask the user to choose which version of Netbeans to clear, based on directories
# Delete all files and directories (recursive) within the 'index' dir

if __name__ == "__main__":
	if ("-V" in argv) or ("--version") in argv:
		print(getVersion())
	else:
		verbose = ("-v" in argv) or ("--verbose" in argv)
		main(verbose)