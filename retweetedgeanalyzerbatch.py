import datetime
import time
import numpy
import sys

def comparray_to_reallist(arr):
    inlist = arr.tolist()
    outlist = []
    for tuple in inlist:
        realpart = numpy.real(tuple)
        imagpart = numpy.imag(tuple)
        valsquared = realpart*realpart + imagpart*imagpart
        val = numpy.sqrt(valsquared)
        outlist.append(val)
    return outlist;

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
        

def whichbin (datum, binslist):
    j = 0
    listlen = len(binslist)
    while (j < listlen-1):
        if datum < binslist[j+1]:
            answer = j
            j = listlen + 1
        else:
            j+=1
    if j == (listlen -1):
        answer = j
    return answer;
    

def histo (datalist, binslist, floatingpoint = False):
    outlist = []
    for i in range (0,len(binslist)):
        outlist.append(0)
    for datumstr in datalist:
        if floatingpoint:
            datum = float(datumstr)
        else:
            datum = int(datumstr)
        j = 0
        binnum = whichbin (datum, binslist)
        outlist [binnum] +=1
    return outlist;

def countinlist(datalist,startinterval,endinterval,inorder=True):
    count = 0
    for item in datalist:
        if (int(item) >= startinterval) and (int(item)<endinterval):
            count+=1
        if inorder:
            if int(item)>=endinterval:
                break;
    return count;
        

def make_even_interval_list (datalist,resolution): #datalist is a list of values, not tuples
    listlength = len(datalist)
    lastentry = datalist[listlength-1]
    outlist = []
    currenttime = 0
    while currenttime <= (lastentry-resolution):
        count = countinlist(datalist,currenttime, currenttime+resolution)
        orderedpair = (currenttime,count)
        outlist.append(orderedpair)
        currenttime += resolution
    return outlist;

def smooth_list (datalist,numentries): #datalist is a list of tuples, not values
    listlength = len(datalist)
    outlist = []
    if listlength < numentries:
        outlist = [(0,-1)]
    else:
        for i in range (0,listlength-numentries+1):
            partial=0
            for j in range (i,(i+numentries)):
                currententry = datalist[j]
                currententryval = currententry[1] #ordered pair
                partial += float(currententryval)
            smoothedval = partial/numentries
            xval = datalist[i][0] #ordered pair
            outtuple = (xval, smoothedval)
            outlist.append (outtuple)

    return outlist;
        
    currenttime = 0
    while currenttime <= (lastentry-resolution):
        count = countinlist(datalist,currenttime, currenttime+resolution)
        orderedpair = (currenttime,count)
        outlist.append(orderedpair)
        currenttime += resolution
    return outlist;


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

def statcalculator_list(datalist,operation):
    length = len(datalist)
    #sortedlist = datalist.sort()
    if length >0:
        if operation == "median":
            answer = numpy.median(datalist)
        elif operation == "sigma":
            answer = numpy.std(datalist)
        elif operation == 'mean':
            answer = numpy.mean(datalist)
    else:
        answer = ""
    try:
        test = float (answer)
    except:
        answer = -1
    return answer;

def extract_value_list(headername,datalist,headerlist,verbose=True,casting=""):
    newlist = []
    if headername in headerlist:
        headerindex = headerlist.index(headername)
        for item in datalist:
            if casting == "":
                val = item[headerindex]
            elif casting == "datetime":
                rawvalue = item[headerindex]
                val = datetime.datetime.strptime(rawvalue,"%Y-%m-%d %H:%M:%S")
            newlist.append(val)
        
    elif verbose:
        print ("Header ",headername,"not found in data list.")
    return newlist;
        

def print_useranalysis(datalist,headerlist,fp):
    followers = lookup_value("followers_count",headerlist,datalist,'int')
    friends = lookup_value("friends_count",headerlist,datalist,'int')
    favscount = lookup_value("favourites_count",headerlist,datalist,'int')
    tweetcount = lookup_value("statuses_count",headerlist,datalist,'int')
    created=lookup_value("created_at",headerlist,datalist,'datetime')
    recorddate = lookup_value("recordmadeon",headerlist,datalist,'datetime')
    deltatime = recorddate - created
    deltasecs = deltatime.total_seconds()
    deltadays = deltasecs/86400
    #print ("longevity" + delimiter + "1",file=fp)
    #print (str(deltadays),file=fp)
    tweetrate = tweetcount/deltadays
    favrate = favscount/deltadays
    follrate= followers/deltadays
    friendrate= friends/deltadays
    if followers != 0:
        tweetfollratio = float(tweetcount) / float(followers)
    else:
        tweetfollratio = -1
    if favscount !=0:
        tweetfavratio = float(tweetcount)/float(favscount)
    else:
        tweetfavratio = -1
    #print ("tweetrate" + delimiter + "1", file=fp)
    #print (str(tweetrate),file = fp)
    #print ("favrate" + delimiter + "1", file = fp)
    #print (str(favrate), file = fp)
    #print ("follrate" + delimiter + "1", file = fp)
    #print(str(follrate), file = fp)
    #print ("friendrate" + delimiter + "1", file = fp)
    #print (str(friendrate), file = fp)
    #print("tweetfollratio" + delimiter + "1", file = fp)
    #print (str(tweetfollratio), file = fp)
    #print ("tweetfavratio" + delimiter + "1", file = fp)
    #print (str(tweetfavratio), file = fp)
    return;

def strip_punctuation(instring):
    punctmarks = [".","'",",",":",";","(",")","!","?",">","<","["]
    outstring = instring
    for punct in punctmarks:
        if outstring.find(punct) > -1:
            outstring = outstring.split(punct)[0]
    return outstring;

def print_edgeanalysis(scrname,nwork,tweetfilepointer,headerlist,fp, delimiter="\t"):
    tweetcount = 0
    isreplycount = 0
    isquotecount = 0
    retweetedcount=0
    retweetedcountlist = []
    favoritedcount = 0
    favoritedcountlist = []
    totalretweets = 0
    totalfavorites = 0
    fivehashes = 0
    trainliketweets = 0
    alltweetslist=[]
    irtsnindex = headerlist.index("in_reply_to_screen_name")
    quoteindex = headerlist.index("is_quote_status")
    fulltextindex = headerlist.index("full_text")
    createdatindex = headerlist.index("created_at")
    numretweetsindex = headerlist.index("retweet_count")            
    rtindex = headerlist.index("retweeted")
    numfavindex = headerlist.index("favorite_count")
    rtscreennameindex = headerlist.index("rtuserscreen_name")
    
    print ("network" + delimiter + "type" + delimiter + "infosource"+delimiter+"infotarget"
           + delimiter + "timestamp",file=fp)

    for tweet in tweetfilepointer:
        tweetcount +=1
        datalist = tweet.split(delimiter)
        datalist[len(datalist)-1]=datalist[len(datalist)-1].strip() #get rid of cr
        alltweetslist.append(datalist)
        tweettext = datalist[fulltextindex]
        tweettimestamp = datalist[createdatindex]
        if datalist[rtscreennameindex] != "": #Have a RT name
            tweettype = "RT"
            sourceid = datalist[rtscreennameindex].lower()
            targetid = scrname
            print (nwork+ delimiter + tweettype + delimiter + sourceid +
                   delimiter + targetid+delimiter+tweettimestamp,file=fp)
        elif tweettext.find("@")> -1:  #have an at mention
            tweettype = "AT"
            targetid = scrname
            atlist = tweettext.split("@")
            for i in range (1,len(atlist)):
                rawname = atlist[i]
                unpipedlist = rawname.split("|") #kill pipe
                lessrawname = unpipedlist[0]
                almostcleanname = lessrawname.split(" ")[0]
                cleanname = strip_punctuation(almostcleanname)
                if len(cleanname)>0:
                    sourceid = cleanname.lower()
                    print (nwork + delimiter + tweettype + delimiter + sourceid
                           + delimiter + targetid+delimiter + tweettimestamp,file=fp)
    return alltweetslist;


        
### MAIN BODY ###

delimiter = "\t"
logfilesuffix = ".tweetlogfile.tsv"
analysisfilesuffix = ".retweetedges.tsv"

batchfilename = input("File name containing batch: ")
batchfilepointer = open(batchfilename+".namesfile","r",encoding="utf-8")
for batchline in batchfilepointer:
    splitbatchlist = batchline.split("\t")
    usernameraw = splitbatchlist[0]
    username = usernameraw.lower().strip()
    print("Analyzing "+username)
    nwork = ""
    if len(splitbatchlist)>0:
        nworkraw = splitbatchlist[1]
        nwork = nworkraw.lower().strip()


    logfilename = username+logfilesuffix
    logfilepointer = open (logfilename,"r",encoding="utf-8")
    

    userheadersstring = logfilepointer.readline()
    if userheadersstring.strip()=="":
        continue
    else:
        analysisfilename = username + analysisfilesuffix
        analysisfilepointer = open(analysisfilename,"w", encoding = "utf-8")
    userdatastring = logfilepointer.readline()
    userheaders = userheadersstring.split(delimiter)
    for i in range (0,len(userheaders)):
        userheaders[i] = userheaders[i].lower().strip()
    userdata = userdatastring.split(delimiter)

    print (userheadersstring,file=analysisfilepointer,end="")
    print (userdatastring,file=analysisfilepointer,end="")
    print_useranalysis(userdata,userheaders,analysisfilepointer)

    tweetheaderstring = logfilepointer.readline()
    tweetheaders = tweetheaderstring.split(delimiter)
    for i in range (0,len(tweetheaders)):
        tweetheaders[i] = tweetheaders[i].lower().strip()
    tweetslist = print_edgeanalysis(username,nwork, logfilepointer,tweetheaders,analysisfilepointer)

    logfilepointer.close()
    analysisfilepointer.close()
