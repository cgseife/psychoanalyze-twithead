## Threadifier
## Charles Seife, cs129@nyu.edu
##
## Takes flat file dumped by streamer and attempts to find threads
## Pretty crude... needs improvement

import twitterinfrastructure as TI

class TwitterThread:
    def __init__(self,threadid):
        self.tid = threadid
        self.root_statusid = ""
        self.matchtextlist = []
        self.child_statusidlist = []
        self.statusstringlist = []
        return;

    def recognize_id(self,idlist):
        answer = False
        for targetid in idlist:
            if targetid != "":
                for childid in self.child_statusidlist:
                    if targetid == childid:
                        answer = True #while loops would prevent going through whole threads
        return answer;

    def text_match(self,txt,matchlength):
        answer = False
        if len(txt) >= matchlength:
            targettxt = txt[0:matchlength].lower()
        else:
            targettxt = txt.lower().strip()
        for matchtxt in self.matchtextlist:
            if targettxt == matchtxt:
                answer = True
        if not answer:
            if (len(txt)>=matchlength+2) and (txt[0:2].lower() == "rt"):
                colon = txt.find(":")
                if (colon >=0) and (len(txt)>colon+2):
                    targettext = txt[colon+2:]
                    answer = self.text_match(targettext,matchlength) #recursive call, can be trimmed
        return answer;

    def addtweet(self, wholestring, twid, twtext, twirtid, twquoteid,matchlength):
        if self.root_statusid == "":
            self.root_statusid = twquoteid
        if twirtid not in self.child_statusidlist:
            self.child_statusidlist.append(twirtid)
        if twid not in self.child_statusidlist:
            self.child_statusidlist.append(twid)
        matchtxt = twtext.lower().strip()
        if not self.text_match(matchtxt, matchlength):
            if len(matchtxt)>= matchlength:
                matchtxt = matchtxt[0:matchlength]
            self.matchtextlist.append(matchtxt)
        self.statusstringlist.append(wholestring)
        return;
                    

def find_threadmatch(indict, twid, twtext, twirtid, twquoteid, matchlength):
    answer = 0
    keylist = list(indict.keys())
    keylength = len (keylist)
    i = 0
    keepgoing = False
    if keylength >=1:
        keepgoing = True
    while keepgoing:
        targetthreadid = keylist [i]
        targetthread = indict[targetthreadid]
        i+=1
        if (targetthread.root_statusid!="") and (targetthread.root_statusid in [twid, twirtid, twquoteid]): #instamatch
            answer = targetthreadid
            keepgoing = False
        elif targetthread.recognize_id([twid,twirtid,twquoteid]): #id match
            answer = targetthreadid
            keepgoing = False
        elif targetthread.text_match(twtext,matchlength): #text match
            answer = targetthreadid
            keepgoing = False
        elif i >= keylength:
            keepgoing = False
        #no else necessary; just keep looping

    return answer;

### MAIN BODY ###

delimiter = "\t"
matchchars = 32
originalfilesuffix = ".streamlogfile.tsv"
threadedfilesuffix = ".threadedlogfile.tsv"

tweetidheader = "id_str"
tweettextheader = "full_text"
tweetinreplytotid = "in_reply_to_status_id_str"
tweetquotingtid = "quoted_status_id_str"

threaddict = {}


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

threadid = 1
for line in infilepointer:
    datalist = line.split(delimiter)
    for i in range (0,len(datalist)):
        rawdatum = datalist[i]
        cleandatum = TI.ensure_string(rawdatum)
        datalist[i] = cleandatum
    tweetid = TI.lookup_value(tweetidheader,headerlist,datalist,cast="str")
    tweettext = TI.lookup_value(tweettextheader,headerlist,datalist,cast="str")
    tweetirtid = TI.lookup_value(tweetinreplytotid,headerlist,datalist,cast="str")
    tweetquotetid = TI.lookup_value(tweetquotingtid,headerlist,datalist,cast="str").strip()
    
    matchnum = find_threadmatch(threaddict, tweetid, tweettext, tweetirtid, tweetquotetid, matchchars)
    if matchnum > 0: #match found
        currentthread = threaddict[matchnum]
    else: #new thread
        matchnum = threadid
        currentthread = TwitterThread(matchnum)
        threadid=threadid+1
    currentthread.addtweet(line, tweetid, tweettext, tweetirtid, tweetquotetid, matchchars)
    threaddict[matchnum]=currentthread

outfilepointer = open(outfilename,"w",encoding = "utf-8")
newheaderline = "threadnum" + delimiter + headerline
print (newheaderline,file=outfilepointer)
for threadid in threaddict.keys():
    targetthread = threaddict[threadid]
    for statusstring in targetthread.statusstringlist:
        outstring = str(threadid) + delimiter + statusstring
        print(outstring,end="",file=outfilepointer)
    outfilepointer.flush()


    
