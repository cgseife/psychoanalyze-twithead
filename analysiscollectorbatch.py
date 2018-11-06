import datetime
import time
import sys

def print_list(inlist, file = sys.stdout, delimiter = "\t",endchar = "\n"):
    length = len(inlist)
    outstring = ""
    for i in range(0,length):
        outstring = outstring + str(inlist[i])
        if i < length-1:
            outstring += delimiter
        else:
            outstring += endchar
    print(outstring,file=file, end="")
    return outstring;

def lookup_value(header,headerlist,datalist,cast='none'):
    index = headerlist.index(header.lower())
    rawvalue = datalist[index].strip()
    if cast == 'str':
        value = str(rawvalue)
    elif cast == 'int':
        if rawvalue != "":
            value = int(rawvalue)
        else:
            value = 0
    elif cast == 'float':
        if rawvalue !="":
            value = float(rawvalue)
        else:
            value = 0.0
    elif cast == 'bool':
        if rawvalue != "":
            value = bool(rawvalue)
        else:
            rawvalue = False
    elif cast == 'datetime':
        if rawvalue != "":
            value = datetime.datetime.strptime(rawvalue,"%Y-%m-%d %H:%M:%S")
        else:
            rawvalue = ""
    else:
        value = rawvalue
    return value;

def collect_useranalysis(datalist,headerlist,fp):
    datadict = {}
    screen_name = lookup_value("screen_name",headerlist,datalist,'str')
    followers = lookup_value("followers_count",headerlist,datalist,'int')
    friends = lookup_value("friends_count",headerlist,datalist,'int')
    favscount = lookup_value("favourites_count",headerlist,datalist,'int')
    tweetcount = lookup_value("statuses_count",headerlist,datalist,'int')
    created=lookup_value("created_at",headerlist,datalist,'str')
    #createdtime = datetime.datetime.strft("%Y-%m-%d %H:%M:%S")

    datadict ['followers'] = [[screen_name],[followers]]
    datadict ['friends'] = [[screen_name],[friends]]
    datadict ['favscount'] = [[screen_name],[favscount]]
    datadict ['tweetcount'] = [[screen_name],[tweetcount]]
    datadict ['created'] = [[screen_name],[created]]

    keepgoing = True
    while keepgoing:
        line = fp.readline()
        if line == "":
            keepgoing = False
        else:
            cleanline = line.strip()
            measurementheaderslist = cleanline.split("\t")
            if len(measurementheaderslist)>=1:
                measname = measurementheaderslist[0]
                dimension = int(measurementheaderslist[1])
                numlines = 1

                valueslist = [[screen_name]]
                for i in range (0,numlines):
                    line = fp.readline()
                    cleanline = line.strip()
                    measurementlist = cleanline.split("\t")
                    valueslist.append(measurementlist)
                if measname not in datadict.keys():
                    datadict[measname] = []
                datadict[measname] = valueslist
    return datadict;

def unpack_measurement(measure,measdict, delimiter="\t"):
    outstringlist = []
    if measure in measdict.keys():
        outerlist = measdict[measure]
        outstringlist.append("MEASURE" + delimiter + measure)
        for dataserieslist in outerlist:
            screennamecontainer = dataserieslist[0]
            screenname = screennamecontainer[0]
            outstring = screenname
            #if len (dataserieslist) == 2: # screenname + 1 line of data
            datacontainer = dataserieslist[1]
            datum = datacontainer[0]
            datumstr = str(datum)
            if datumstr[0] != "(": #not a tuple
                outstring = outstring + delimiter + datumstr
            else:
                for datum in datacontainer:
                    datumstr = str(datum)
                    outstring = outstring + delimiter + datumstr
            outstringlist.append(outstring)
            #else:
                ## IF 2 lines or more of data, loop
                ## for datacontainer in dataserieslist[1:]:
                ## print screenname + dimension
                ## print 

        ### NEED TO DEAL WITH DIFFERENT LENGTHS
    return outstringlist;
            
    


### MAIN BODY ###

delimiter = "\t"
namesfileprefix = input("What is the prefix: ")
namesfilename = namesfileprefix+".namesfile"
collectedfilename = namesfileprefix + ".collectedanalysis.tsv"
analysisfilesuffix = ".tweetanalysis.tsv"
measurementdict = {}

namefilepointer = open (namesfilename,"r",encoding="utf-8")
measurementdict['usertype'] = []
measurementdict['botguess'] = []
for line in namefilepointer:
    cleanline = line.strip()
    cleanlinelist = cleanline.split("\t")
    if len(cleanlinelist) < 1:
        screenname == ""
    else:
        screenname = cleanlinelist[0].strip()
        usertype = cleanlinelist[1].strip()
        if len (cleanlinelist)>=3:
            botguess = cleanlinelist[2].strip()
        else:
            botguess = "unclassified"
    if screenname == "":
        continue
    print (screenname)
    measurementdict['usertype'].append([[screenname],[usertype]])
    measurementdict['botguess'].append([[screenname],[botguess]])
    analysisfilename = screenname + analysisfilesuffix
    try:
        analysisfilepointer = open(analysisfilename,"r", encoding = "utf-8")
    except:
        continue
    userheadersstring = analysisfilepointer.readline()
    if userheadersstring.strip() == "":
        continue
    userdatastring = analysisfilepointer.readline()
    userheaders = userheadersstring.split(delimiter)
    for i in range (0,len(userheaders)):
        userheaders[i] = userheaders[i].lower().strip()
    userdata = userdatastring.split(delimiter)
    newdict = collect_useranalysis(userdata,userheaders,analysisfilepointer)
    for measure in newdict.keys():
        if measure not in measurementdict.keys():
            measurementdict[measure]=[]
        measurementdict[measure].append(newdict[measure])

outfilepointer = open (collectedfilename,"w",encoding="utf-8")
for measurement in measurementdict.keys():
    try:
        datapacklist = unpack_measurement(measurement,measurementdict)
    except:
        print ("Failed to unpack measurement:",measurement)
        continue
    for datapack in datapacklist:
        print (datapack,file=outfilepointer)
     
