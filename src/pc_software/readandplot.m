function readandplot(file, pathto)
	path = strcat(pathto, file);
	dfid = fopen(path, "r");
	[val, count] = fread(dfid, 100, "int8");

	n = 0:count-1;
	stem(n, val);

	undloc = findstr(path, "_");
	dotloc = findstr(path, ".");
	fnameloc = rindex(path,"\\");
		
	fdate = substr(path, fnameloc+1, (undloc)-(fnameloc+1));
	fnum = substr(path, undloc+1, dotloc - (undloc+1));

	title(['Plot of ', fdate, ' - ', fnum]);
endfunction
