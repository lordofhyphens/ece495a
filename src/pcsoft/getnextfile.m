function nextfile = getnextfile(file)
	letterpos = index(file, ".dat") - 1;
	fileletter = substr(file, letterpos, 1);
	letterascii = toascii(fileletter);

	if(letterascii != 122)
		nextfile = strcat(substr(file, 1, letterpos-1), char(letterascii + 1), ".dat");
	else
		nextfile = strcat(substr(file, 1, letterpos-1), "aa.dat");
	endif

endfunction
