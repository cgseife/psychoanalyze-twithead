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
    print ("longevity" + delimiter + "1",file=fp)
    print (str(deltadays),file=fp)
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
    print ("tweetrate" + delimiter + "1", file=fp)
    print (str(tweetrate),file = fp)
    print ("favrate" + delimiter + "1", file = fp)
    print (str(favrate), file = fp)
    print ("follrate" + delimiter + "1", file = fp)
    print(str(follrate), file = fp)
    print ("friendrate" + delimiter + "1", file = fp)
    print (str(friendrate), file = fp)
    print("tweetfollratio" + delimiter + "1", file = fp)
    print (str(tweetfollratio), file = fp)
    print ("tweetfavratio" + delimiter + "1", file = fp)
    print (str(tweetfavratio), file = fp)
    return;

def print_tweetanalysis(tweetfilepointer,headerlist,fp, delimiter="\t"):
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
    numretweetsindex = headerlist.index("retweet_count")            
    rtindex = headerlist.index("retweeted")
    numfavindex = headerlist.index("favorite_count")
    for tweet in tweetfilepointer:
        tweetcount +=1
        datalist = tweet.split(delimiter)
        datalist[len(datalist)-1]=datalist[len(datalist)-1].strip() #get rid of cr
        alltweetslist.append(datalist)
        if datalist[irtsnindex] != "": #in reply
            isreplycount +=1
        if datalist[quoteindex] in ["TRUE","true","True"]:
            isquotecount +=1
        else:
            try:
                numretweets = int(datalist[numretweetsindex])
            except:
                numretweets = 0
            totalretweets += numretweets
            retweetedcountlist.append(numretweets)
            if numretweets > 0:
                retweetedcount +=1
            try:
                numfavs = int(datalist[numfavindex])
            except:
                numfavs = 0
            totalfavorites += numfavs
            favoritedcountlist.append(numfavs)
            if numfavs >0:
                favoritedcount +=1
        tweettext = datalist[fulltextindex]
        if len(tweettext.split('#'))>= 6: #at least 5 hashtags
            fivehashes +=1
        if len(tweettext.split('@'))>=6: #at least 5 accounts ref'd
            trainliketweets +=1            
    rtedratio = float(retweetedcount) / float(tweetcount)
    fvedratio = float(favoritedcount) / float(tweetcount)
    replyratio = float(isreplycount) / float(tweetcount)
    quoteratio = float(isquotecount) / float(tweetcount)
    fivehashesratio = float(fivehashes)/float(tweetcount)
    trainlikeratio = float(trainliketweets)/float(tweetcount)
    if retweetedcount > 0:
        avgrt = float (totalretweets) / float(retweetedcount)
    else:
        avgrt = -1
    if favoritedcount > 0:
        avgfv = float (totalfavorites) / float(favoritedcount)
    else:
        avgfv = -1
    nonrtcount = float(tweetcount - isquotecount)
    if nonrtcount>0:
        proprt = float(retweetedcount)/nonrtcount
        propfv = float (favoritedcount)/nonrtcount
    else:
        proprt = -1
        propfv = -1

    medianrtcount = statcalculator_list(retweetedcountlist,"median")
    medianfvcount = statcalculator_list(favoritedcountlist,"median")

    print ("isreplycount" + delimiter + "1", file=fp)
    print (str(isreplycount),file = fp)
    print ("isquotecount" + delimiter + "1", file=fp)
    print (str(isquotecount),file = fp)
    print ("retweetedcount" + delimiter + "1", file=fp)
    print (str(retweetedcount),file = fp)
    print ("favoritedcount" + delimiter + "1", file=fp)
    print (str(favoritedcount),file = fp)
    print ("totalretweets" + delimiter + "1", file=fp)
    print (str(totalretweets),file = fp)
    print ("totalfavorites" + delimiter + "1", file=fp)
    print (str(totalfavorites),file = fp)
    print ("rtedratio" + delimiter + "1", file=fp)
    print (str(rtedratio),file = fp)
    print ("replyratio" + delimiter + "1", file=fp)
    print (str(replyratio),file = fp)
    print ("quoteratio" + delimiter + "1", file=fp)
    print (str(quoteratio),file = fp)
    print ("avgrtcount" + delimiter + "1", file=fp)
    print (str(avgrt),file = fp)
    print ("medianrtcount" + delimiter + "1", file=fp)
    print (str(medianrtcount),file = fp)
    print ("avgfvcount" + delimiter + "1", file=fp)
    print (str(avgfv),file = fp)
    print ("medianfvcount" + delimiter + "1", file=fp)
    print (str(medianfvcount),file = fp)    
    print ("nonquoteproprt" + delimiter + "1", file=fp)
    print (str(proprt),file = fp)
    print ("nonquotepropfv" + delimiter + "1", file=fp)
    print (str(propfv),file = fp)
    print ("fivehashesratio" + delimiter + "1", file=fp)
    print (str(fivehashesratio),file = fp)
    print ("trainlikeratio" + delimiter + "1", file=fp)
    print (str(trainlikeratio),file = fp)
    
    return alltweetslist;

def print_timeanalysis(alltweetslist,headerlist,recordmadeon,utcoffset,fp, delimiter="\t"):
    timestamplist = extract_value_list("created_at",alltweetslist,headerlist,casting="datetime")
    burstlist = []
    length = len (timestamplist)
    if length >0:
        zerothtweettime = timestamplist[0]
        recordedtweettime = timestamplist[length-1]
        recordeddelta = (zerothtweettime-recordedtweettime).total_seconds()
        if recordeddelta < 0:
            recordeddelta = recordeddelta * -1
            print ("Negative value")
        if recordeddelta > 0:
            recordedtweetrate = length *86400/float(recordeddelta)
        else:
            recordedtweetrate = -1
    else:
        recordedtweetrate = -1
    if length >=500:
        fivehundredthtweettime = timestamplist[499]
        fivehundreddelta = (zerothtweettime-fivehundredthtweettime).total_seconds()
        fivehundredtweetrate = 500.0*86400.0/float(fivehundreddelta)
    else:
        fivehundredtweetrate = -1
    if length >=1000:
        thousandthtweettime = timestamplist[999]
        thousandddelta = (zerothtweettime-thousandthtweettime).total_seconds()
        thousandtweetrate = 1000.0*86400.0/float(thousandddelta)
        fiveconektweetaccel = 86400*(fivehundredtweetrate - thousandtweetrate)/(fivehundredthtweettime-thousandthtweettime).total_seconds()
    else:
        thousandtweetrate=-1
        fiveconektweetaccel = -123456.7



    print ("recordedtweetrate" + delimiter + "1", file=fp)
    print (str(recordedtweetrate),file = fp) #tweet rate for logged tweets, <=3700 of them
    print ("fivehundredtweetrate" + delimiter + "1", file=fp)
    print (str(fivehundredtweetrate),file = fp)
    print ("thousandtweetrate" + delimiter + "1", file=fp)
    print (str(thousandtweetrate),file = fp)


    if recordedtweetrate >0:
        rateratio5Crec = fivehundredtweetrate/recordedtweetrate
    else:
        rateratio5Crec = -1
    if thousandtweetrate>0:
        rateratio5C1K = fivehundredtweetrate/thousandtweetrate
    else:
        rateratio5C1K = -1
        
    print ("rateratio5Crec" + delimiter + "1", file=fp)
    print (str(rateratio5Crec),file = fp) #tweet rate ratio: 500tw vs. recorded
    print ("rateratio5C1K" + delimiter + "1", file=fp)
    print (str(rateratio5C1K),file = fp) #tweet rate ratio: 500tw vs. 1000tw
    
    if fiveconektweetaccel != -123456.7:
        print ("fiveconektweetaccel" + delimiter + "1", file=fp)
        print (str(fiveconektweetaccel),file = fp)
        #acceleration between 500K / 100K per day


    for i in range(0,(length-1)):
        burstlist.append((timestamplist[i]-timestamplist[i+1]).total_seconds())
    tweetgapmean = statcalculator_list(burstlist,"mean")
    tweetgapmedian = statcalculator_list(burstlist,"median")
    tweetgapsigma = statcalculator_list(burstlist,"sigma")
    try:
        burstiness = (tweetgapsigma - tweetgapmean)/(tweetgapsigma + tweetgapmean) #Goh-Barabasi parameter
    except:
        burstiness = -1
    print ("tweetgapmean" + delimiter + "1", file=fp)
    print (str(tweetgapmean),file = fp)
    print ("tweetgapmedian" + delimiter + "1", file=fp)
    print (str(tweetgapmedian),file = fp)    
    print ("burstiness" + delimiter + "1", file=fp)
    print (str(burstiness),file = fp)

    
    burstbins = [0,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131702,262144,524288,1048576]
    bursthisto = histo(burstlist,burstbins)
    tuplelist = []
    for i in range (0,len(burstbins)):
        newtuple = (burstbins[i],bursthisto[i])
        tuplelist.append(newtuple)
    print ("bursthisto" + delimiter + "2",file=fp)
    print_list (tuplelist,file=fp)
    
    deltalist = [] # captures distance from now [recordmadeon] when tweets made
    for timestamp in timestamplist:
        deltalist.append((recordmadeon - timestamp).total_seconds()+14400) #recordmadeon in ET; timestamp GMT

    secsin15min = 15*60
    secsin30min = 30*60
    secsin60min = 60*60
    secsinday = 60*60*24
    secsinweek = 7 * secsinday
    weekinto256 = 2362.5
    
    dailytweets = make_even_interval_list(deltalist,secsinday)
    if len(dailytweets)==0:
        dailytweets = [(0,-1)]
    print("dailytweets"+delimiter + "2",file = fp)
    print_list(dailytweets, file = fp)
    dailytweetssmoothedweekly = smooth_list(dailytweets,7)
    print("tweetssmoothedweek"+delimiter + "2",file = fp)
    print_list(dailytweetssmoothedweekly, file = fp)

    numbins = int(secsinweek / secsin30min)
    week30minbins = []
    for i in range(0,numbins):
        week30minbins.append(i*secsin30min)

    day15minbins=[]
    numbins = int (secsinday/secsin15min)
    for i in range (0,numbins):
        day15minbins.append(i*secsin15min)

    week256bins=[]
    numbins = int (secsinweek/weekinto256)
    for i in range (0,numbins):
        week256bins.append(i*weekinto256)
        
    ETcorrection = datetime.timedelta(seconds=-14400)
    recordmadeonGMT = recordmadeon + ETcorrection
    localcorrection = datetime.timedelta(seconds=utcoffset)
    recordmadeonlocal = recordmadeonGMT + localcorrection

    nextmonday = recordmadeonlocal+datetime.timedelta(seconds=secsinday)
    while nextmonday.weekday()!=0: #monday = 0, defining start of week
        nextmonday += datetime.timedelta(seconds=secsinday)
    midnightmondaylocal = nextmonday.replace(hour=0, minute=0, second=0, microsecond=0)

    weekdeltalist= []
    for timestamp in timestamplist:
        localtimestamp = timestamp + localcorrection
        timeprior = midnightmondaylocal - localtimestamp
        timepriorsec = timeprior.total_seconds()
        timepriorsecweek = timepriorsec % secsinweek
        timeaftermonday = secsinweek - timepriorsecweek
        weekdeltalist.append(timeaftermonday)
        
    tuplelist = []
    weektweethisto = histo(weekdeltalist,week30minbins)
    for i in range (0,len(week30minbins)):
        newtuple = (week30minbins[i],weektweethisto[i])
        tuplelist.append(newtuple)
    print("weektweethisto"+delimiter + "2",file = fp)
    print_list(tuplelist, file = fp)

    daydeltalist = []
    for stampweeksecs in weekdeltalist:
        stampdaysecs = stampweeksecs % secsinday
        daydeltalist.append(stampdaysecs)
        
    tuplelist = []
    daytweethisto = histo(daydeltalist,day15minbins)
    for i in range (0,len(day15minbins)):
        newtuple = (day15minbins[i],daytweethisto[i])
        tuplelist.append(newtuple)
    print("daytweethisto"+delimiter + "2",file = fp)
    print_list(tuplelist, file = fp)

    tuplelist = []
    week256histo = histo(weekdeltalist,week256bins)
    for i in range (0,len(week256bins)):
        newtuple = (week256bins[i],week256histo[i])
        tuplelist.append(newtuple)
    print("week256histo"+delimiter + "2",file = fp)
    print_list(tuplelist, file = fp)


    weekarray = numpy.array(week256histo,dtype=int)
    fftweekarray = numpy.fft.fft(weekarray)
    sample_size = 256
    sample_rate = float((secsinweek)/weekinto256)
    freqbinsarray = numpy.fft.fftfreq(sample_size,d=(1.0/sample_rate))
    freqbinslist = freqbinsarray.tolist()
    ## consider inverting all values in freqbinslist
    fftweekreallist = comparray_to_reallist(fftweekarray)

    tuplelist = []
    for i in range (0,len(week256bins)):
        newtuple = (freqbinslist[i],fftweekreallist[i])
        tuplelist.append(newtuple)
    print("week256fft"+delimiter + "2",file = fp)
    print_list(tuplelist, file = fp)


                    
                    
    #DO FFT
    return;
        
### MAIN BODY ###

delimiter = "\t"
logfilesuffix = ".tweetlogfile.tsv"
analysisfilesuffix = ".tweetanalysis.tsv"

batchfilename = input("File name containing batch: ")
batchfilepointer = open(batchfilename+".namesfile","r",encoding="utf-8")
for batchline in batchfilepointer:
    usernameraw = batchline.split("\t")[0]
    username = usernameraw.lower().strip()
    print("Analyzing "+username)


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
    tweetslist = print_tweetanalysis(logfilepointer,tweetheaders,analysisfilepointer)

    zerotime = lookup_value("recordmadeon",userheaders,userdata,cast='datetime')
    timezonedelta = lookup_value("utc_offset",userheaders,userdata,cast='int')
    print_timeanalysis(tweetslist,tweetheaders,zerotime,timezonedelta,analysisfilepointer)

    logfilepointer.close()
    analysisfilepointer.close()
