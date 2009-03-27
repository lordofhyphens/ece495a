function displaydata
	if(nargin != 0)
		usage("displaydata");
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
		readandplot(startfile)

		
	endif
endfunction

