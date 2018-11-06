## Thread Parser
## Charles Seife, cs129@nyu.edu
##
## Takes a threadified flat file and attempts to impute parent-->child relationships
## for use in a directed graph. Again, crude and needs improvement.

import twitterinfrastructure as TI
import datetime

def stringify_list(inlist,delimiter="\t"):
    first = True
    outstring = ""
    for item in inlist:
        if first:
            first = False
        else:
            outstring += delimiter
        outstring += str(item)
    return outstring;

### MAIN BODY ###

delimiter = "\t"
originalfilesuffix = ".threadedlogfile.tsv"
threadedfilesuffix = ".parsedthreadfile.tsv"

threadidheader = "threadnum"
tweetidheader = "id_str"
tweetinreplytotidheader = "in_reply_to_status_id_str"
tweetquotingtidheader = "quoted_status_id_str"
tweeternameheader = "screen_name_tweeter"
rtusernameheader = "rtuserscreen_name"
replyusernameheader = "in_reply_to_screen_name"
tweettimeheader = "created_at"
threadnumheader = "threadnum"

threadmultheader = "thread_multiplicity"
threadearliestheader = "earliest_thread_timestamp"
threadtimedeltaheader = "thread_age_seconds"
userstreammultiplicityheader = "user_stream_multiplicity"
proximateparentheader = "proximate_parent"

userheaderlist = ["id_str_tweeter","name_tweeter","screen_name_tweeter","url_tweeter","description_tweeter","protected_tweeter","verified_tweeter","followers_count_tweeter","friends_count_tweeter","listed_count_tweeter","favourites_count_tweeter","statuses_count_tweeter","created_at_tweeter","utc_offset_tweeter","time_zone_tweeter","geo_enabled_tweeter","lang_tweeter","profile_background_color_tweeter","profile_link_color_tweeter","profile_sidebar_border_color_tweeter","profile_sidebar_fill_color_tweeter","profile_use","background_image_tweeter","withheld_in_countries_tweeter","withheld_scope_tweeter"]

statusdict = {}
nodedict = {}
edgedict = {}


fileprefix = input("What is the file prefix? ")

infilename = fileprefix + originalfilesuffix
outfilename = fileprefix + threadedfilesuffix

infilepointer = open(infilename,"r",encoding="utf-8")
headerline = infilepointer.readline().strip()
headerlist = headerline.split(delimiter)
for i in range(0,len(headerlist)):
    rawheader = headerlist[i]
    header = rawheader.lower().strip()
    headerlist[i]=header

for line in infilepointer:
    datalist = line.split(delimiter)
    for i in range (0,len(datalist)):
        rawdatum = datalist[i]
        cleandatum = TI.ensure_string(rawdatum)
        datalist[i] = cleandatum
        
    tweetid = TI.lookup_value(tweetidheader,headerlist,datalist,cast="str")
    statusdict[tweetid] = datalist
infilepointer.close()

#calculate thread multiplicities, earliest in thread, user mutliplicities
threadmultdict={}
threadearliestdict = {}
usermultdict = {}
for statusname in statusdict.keys():
    status = statusdict[statusname]
    threadid = TI.lookup_value(threadidheader,headerlist,status,cast="str")
    tweettime = TI.lookup_value(tweettimeheader,headerlist,status,cast="datetime")
    if threadid in threadmultdict.keys():
        threadmult = threadmultdict[threadid]
        threadmultdict[threadid] = threadmult + 1
        oldtime = threadearliestdict[threadid]
        if tweettime < oldtime:
            threadearliestdict[threadid] = tweettime
    else:
        threadmultdict[threadid] = 1
        threadearliestdict[threadid]=tweettime
        status = statusdict[statusname]
    tweetername =TI.lookup_value(tweeternameheader,headerlist,status,cast="str") 
    if tweetername in usermultdict.keys():
        usermult = usermultdict[tweetername]
        usermultdict[tweetername] = usermult +1
    else:
        usermultdict[tweetername] = 1

#add thread multiplicities, earliest in thread, usermultiplicities to statuses
headerlist.append(threadmultheader)
headerlist.append(threadearliestheader)
headerlist.append(threadtimedeltaheader)
headerlist.append(userstreammultiplicityheader)
for statusname in statusdict.keys():
    status = statusdict[statusname]
    threadid = TI.lookup_value(threadidheader,headerlist,status,cast="str")
    status.append(threadmultdict[threadid])
    status.append(threadearliestdict[threadid])
    tweettime = TI.lookup_value(tweettimeheader,headerlist,status,cast="datetime")
    deltatime = tweettime - threadearliestdict[threadid]
    status.append(str(int(deltatime.total_seconds())))
    tweetername =TI.lookup_value(tweeternameheader,headerlist,status,cast="str") 
    status.append(usermultdict[tweetername])

threadmultdict={} #free memory
threadearliestdict = {}
usermultdict = {}

proximateparentdict = {}
#calculate proximate parent
for statusname in statusdict.keys():
    status = statusdict[statusname]
    tweetername = TI.lookup_value(tweeternameheader,headerlist,status,cast="str").strip()
    irtname = TI.lookup_value(replyusernameheader,headerlist,status,cast="str").strip()
    rtname = TI.lookup_value(rtusernameheader,headerlist,status,cast="str").strip()
    rtid = TI.lookup_value(tweetquotingtidheader,headerlist,status,cast="str").strip()
    irtid = TI.lookup_value(tweetinreplytotidheader,headerlist,status,cast="str").strip()
    threaddelta = TI.lookup_value(threadtimedeltaheader,headerlist,status,cast="int")
    if irtname != "":
        proximateparentdict[statusname] = irtname
    elif rtname != "":
        proximateparentdict[statusname] = rtname

    elif (rtid !=""):
        if rtid in statusdict.keys():
            tempstatus = statusdict[rtid]
            parent=TI.lookup_value(tweeternameheader,headerlist,tempstatus,cast="str").strip()
        else:
            parent = "author-" + rtid
        proximateparentdict[statusname] = parent
    elif (irtid !=""):
        if irtid in statusdict.keys():
            tempstatus = statusdict[irtid]
            parent=TI.lookup_value(tweeternameheader,headerlist,tempstatus,cast="str").strip()
        else:
            parent ="author-" + irtid
        proximateparentdict[statusname] = parent
    elif threaddelta == 0:
        proximateparentdict[statusname] = tweetername
    else:
        threadstring = TI.lookup_value(threadnumheader,headerlist,status,cast="str")
        proximateparentdict[statusname]="author-thread-"+threadstring

#add proximate parent to statuses
headerlist.append(proximateparentheader)
for statusname in statusdict.keys():
    status = statusdict[statusname]
    status.append(proximateparentdict[statusname])

proximateparentdict = {} #free memory


# print results to flat file

outfilepointer = open(outfilename,"w",encoding = "utf-8")
newheaderline = stringify_list(headerlist)
print (newheaderline,file=outfilepointer)
for statusname in statusdict.keys():
    status = statusdict[statusname]
    statusstring = stringify_list(status)
    print(statusstring,file=outfilepointer)
    outfilepointer.flush()


    
