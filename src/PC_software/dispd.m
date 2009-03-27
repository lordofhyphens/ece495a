function dispd
	pathto = "data\";

	if(nargin != 0)
		usage("dispd");
		return;
	else
		acfid = fopen(strcat(pathto, "acqconfig.txt"), "r");
		txt = fgetl(acfid);
		semipos = findstr(txt, ";");
		
		startfile = substr(txt, 1, semipos(1) - 1);

		if(semipos(2) > semipos(1) + 1)
			endfile = substr(txt, (semipos(1) + 1), semipos(2) - (semipos(1) + 1));
		else
			endfile = "";
		endif

		fclose(acfid);
		readandplot(startfile);
		nextfile = getnextfile(startfile);

		do
			currfile = nextfile;
			nextfile = getnextfile(currfile);
		until(strcmp(nextfile, endfile) == 1);
	endif
endfunction

