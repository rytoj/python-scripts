import time
import os
from shutil import copy2
import sys


def get_current_date():
	return time.time()


def get_file_mtime(filename):
	return os.path.getmtime(filename)


def validated_file(src):
	return os.path.isfile(src)


def validate_folder(dest):
	return os.path.isdir(dest)


def validate_input(src, dest):
	return validated_file(src) and validate_folder(dest)


def check_if_newer(filename, folder):
	if not validate_input(filename, folder): raise "Invalid input"
	datet = get_current_date()
	while True:
		time.sleep(0.5)
		filet = get_file_mtime(filename)
		if filet > datet:
			print("File was modified")
			copy2(filename, folder)
			datet = get_current_date()


def main():
	if len(sys.argv) < 3:
		print("./{} src-file directory/ ".format(sys.argv[0]))
		sys.exit(1)
	if len(sys.argv) == 3:
		check_if_newer(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
	main()
