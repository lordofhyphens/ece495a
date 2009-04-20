function dispd
	pathto = "data\\";
	fext = ".dat";

	% Read acquisition from acqdisp
	acfid = fopen("acqdisp.txt", "r");
	theacq = fgetl(acfid);
	fclose(acfid);

	% If file is blank, convert theacq to a string
	if(theacq == -1)
		theacq = "-1";
	endif

	% If acqdisp is not blank, display it
	if(strcmp(theacq, "-1") != 1)
		% Get position of colon and pipe
		colpos = index(theacq, ":");
		pipepos = index(theacq, "|");

		% Split off label and acquisition name
		if(length(theacq) > pipepos)
			thelabel = substr(theacq, pipepos+1);
		else
			thelabel = "";
		endif

		theacq = substr(theacq, 1, pipepos-1);

		% Get prefix and init startfile
		pref = substr(theacq, 1, colpos-1);
		startfile = strcat(pref, strcat('a', fext));

		% If acq has multi-parts, set endfile
		if(length(theacq) > colpos)
			endfile = strcat(pref, substr(theacq, colpos+1, 1), fext);
		else
			endfile = "";
		endif

		% Plot the (first) data.
		readandplot(startfile, pathto, thelabel);

		% If acq is multi-part, prompt user to display next parts
		if(strcmp(endfile, "") != 1)
			nextfile = getnextfile(startfile, fext);

			do
				opt = menu("Plot is multi-part. Options:", "Display next part", "Quit");

				if(opt == 1)
					readandplot(nextfile, pathto);
					nextfile = getnextfile(nextfile);
				endif
			until(strcmp(nextfile, endfile) == 1 || opt == 2);
		endif
	endif

endfunction


% Executes function when called from commandline
dispd
