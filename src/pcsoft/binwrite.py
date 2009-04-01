# bintest.py
import struct, sys

nums = []

if len(sys.argv) == 2:
	wrifile = sys.argv[1]
else:
	if len(sys.argv) == 1:
		prompt = "Please enter the name of the file to write to: "
	elif len(sys.argv) > 2:
		prompt = "Too many arguments, please enter the name of the file to write to: "
	
	wrifile = raw_input(prompt)


innums = raw_input("Enter the numbers to write, separated by commas and whitepace if you prefer: ")

nums = []
for thisnum in innums.split(','):
	nums.append(int(thisnum.strip()))

fid = open(wrifile, "wb")

for i in range(0, len(nums)):
	fid.write(struct.pack('b', nums[i]))


fid.close()

