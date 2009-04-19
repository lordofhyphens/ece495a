function dispd
	pathto = "data\\";

	if(nargin != 0)
		usage("dispd");
		return;
	else
		acfid = fopen("acqdisp.txt", "r");
		lastpoll = fgetl(acfid);
		fclose(acfid);

		do
			acfid = fopen("acqdisp.txt", "r");
			thispoll = fgetl(acfid);
			fclose(acfid);

			if(thispoll == -1)
				thispoll = int2str(thispoll);
			endif
			if(lastpoll == -1)
				lastpoll = int2str(lastpoll);
			endif


			if(strcmp(thispoll, "-1") != 1)
				colpos = index(thispoll, ":");
				pipepos = index(thispoll, "|");
				thislabel = substr(thispoll, pipepos+1);
				thispoll = substr(thispoll, 1, pipepos-1);
				pref = substr(thispoll, 1, colpos-1);
				startfile = strcat(pref, 'a.dat');

				if(length(thispoll) > colpos)
					endfile = strcat(pref, substr(thispoll, colpos+1, 1), '.dat');
				else
					endfile = "";
				endif

				# Plot the (first) data.
				readandplot(startfile, pathto, thislabel);

				if(strcmp(endfile, "") != 1)
					nextfile = getnextfile(startfile);

					do
						opt = menu("Plot is multi-part. Options:", "Display next part", "Quit");

						if(opt == 1)
							readandplot(nextfile, pathto);
							nextfile = getnextfile(nextfile);
						endif
					until(strcmp(nextfile, endfile) == 1 || opt == 2);
				endif
			endif

			lastpoll = thispoll;

			acfid = fopen("acqdisp.txt", "w");
			fputs(acfid, "");
			fclose(acfid);
			
			opt = menu("Program options:", "Display acquisition", "Quit");
		until(opt == 2);
	endif
endfunction

