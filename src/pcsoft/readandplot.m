function readandplot(filename, pathto, label)
	acqfile = strcat(pathto, filename);
	dfid = fopen(acqfile, "r");
	[val, count] = fread(dfid, 100, "int8");
	fclose(dfid);

	n = 0:count-1;
	plot(n, val);

	undloc = findstr(acqfile, "_");
	dotloc = findstr(acqfile, ".");
	fnameloc = rindex(acqfile,"\\");
		
	fdate = substr(acqfile, fnameloc+1, (undloc)-(fnameloc+1));
	fnum = substr(acqfile, undloc+1, dotloc - (undloc+1));

	title(['Plot of ', fdate, ' - ', fnum]);

	% If label exists, add it to legend
	if(strcmp(label, "") != 1)
		legend(label);
	endif
endfunction

