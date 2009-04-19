global sckhost, sckport, pathto, fsuffix, partsize
"""
This file contains global variables used by both acqdata.py and 
inter.py. An explanation of each variable is provided.

sckhost    - socket host name used by both inter.py and acqdata.py

sckport    - socket port number. Change this if the default port is
             throwing errors.

pathtodata - directory that acquisitions will be stored in. can be
             relative, backslashes should be escaped by another backslash,
			 and the value should contain a trailing backslash
			 ex: pathtodata = 'path\\to\\data\\

fext       - file extension for acquisitions. default is .dat

partsize   - acqdata.py breaks up large acquisitions into multiple files.
             this value is the number of KiB (KiB = 1024 bytes) of each 
			 acquisition part.


acqpgsize  - number of acquisitions per "page" for the acquisition display
             list in inter.py

viewnewacq - value of True causes inter.py to set current display page to
             the last page when an acquisition completes. False results in
			 inter.py staying on the same page
"""

sckhost = 'localhost'
sckport = 19364
pathtodata = 'data\\'
fext = '.dat'
partsize = 100
acqpgsize = 30
viewnewacq = True

