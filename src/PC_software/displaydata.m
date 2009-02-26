function [val, count] = displaydata(path)

	if (nargin != 1)
		usage("displaydata(filename)");
		return;
	else
		dfid = fopen(path, "r");
		[val, count] = fread(dfid, 20, "int8");

		n = 0:count-1;
		stem(n, val);

		undloc = findstr(path, "_");
		fnameloc = rindex(path,"\\");

		fdate = substr(path, fnameloc+1, (undloc)-(fnameloc+1));
		fnum = substr(path, undloc+1, 1);

		disp(['fdate = ', fdate, '; fnum = ', fnum]);
		title(['Plot of ', fdate, ' - ', fnum]);

	endif


endfunction

