function dispd
	pathto = "data\\";

	if(nargin != 0)
		usage("dispd");
		return;
	else
		acfid = fopen("acqdisp.txt", "r");
		txt = fgetl(acfid);

		if(txt != -1)
			colpos = index(txt, ":");
			pref = substr(txt, 1, colpos-1);
			startfile = strcat(pref, 'a.dat');

			if(length(txt) > colpos)
				endfile = strcat(pref, substr(txt, colpos+1, 1), '.dat');
			else
				endfile = "";
			endif

			fclose(acfid);
			readandplot(startfile, pathto);

			if(strcmp(endfile, "") != 1)
				nextfile = getnextfile(startfile);

				do
					uin = menu("Plot options ", "Display next plot", "Quit");

					if(uin == 1)
						readandplot(nextfile, pathto);
						nextfile = getnextfile(nextfile);
					endif
				until(strcmp(nextfile, endfile) == 1 || uin == 2);

			endif
		endif
	endif
endfunction

