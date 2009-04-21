function nextfile = getnextfile(file, fext)
	letterpos = index(file, fext) - 1;
	fileletter = substr(file, letterpos, 1);
	letterascii = toascii(fileletter);

	if(letterascii != 122)
		nextfile = strcat(substr(file, 1, letterpos-1), char(letterascii + 1), fext);
	else
		nextfile = strcat(substr(file, 1, letterpos-1), 'aa', fext);
	endif

endfunction
