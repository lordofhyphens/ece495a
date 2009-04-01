function dispd
	pathto = "data\\";
	next = "next";
	n = "next";
	quit = "quit";
	q = "quit";

	if(nargin != 0)
		usage("dispd");
		return;
	else
		acfid = fopen("acqconfig.txt", "r");
		txt = fgetl(acfid);
		semipos = findstr(txt, ";");
		
		startfile = substr(txt, 1, semipos(1) - 1);

		if(semipos(2) > semipos(1) + 1)
			endfile = substr(txt, (semipos(1) + 1), semipos(2) - (semipos(1) + 1));
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
endfunction

