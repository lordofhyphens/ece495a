pathToSoft = '#PATH#\';
filename = input("Please enter data file name: ");

datafilepath = [pathToSoft, "data\\", filename];
disp(datafilepath);

dfid = fopen(datafilepath, "r");
[val, count] = fread(dfid, 20, "uint8");

n=0:count-1;
plot(val, count);
