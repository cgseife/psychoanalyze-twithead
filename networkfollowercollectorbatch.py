import tweepy
import time
import datetime
import twitterinfrastructure as TI



def startup_program(infilepointer):
    outlist = []
    headerline = infilepointer.readline()
    headerlist = headerline.strip().split("\t")
    idindex = headerlist.index("id_str")
    for line in infilepointer:
        dataline = line.strip()
        datalist = dataline.split("\t")
        id = datalist[idindex]
        outlist.append(id)
    return outlist;
        
    

### MAIN BODY ###

keyfilename = "apikeys.txt"

api = TI.get_api (keyfilename)

logfilesuffix = ".followers.tsv"

batchfilename = input("File name containing batch: ")
batchfilepointer = open(batchfilename,"r",encoding="utf-8")
exceptionfilename = "followexceptions."+ batchfilename
exceptionfile = open (exceptionfilename,"w",encoding="utf-8")
for batchline in batchfilepointer:
    usernameraw = batchline.split("\t")[0]
    username = usernameraw.strip().lower()
    

    logfilename = username+logfilesuffix

    logfilepointer = open (logfilename,"w",encoding="utf-8")

    
    try:
        statpagelist = api.user_timeline(username)
        firststat = statpagelist[0]
    except:
        print (username,file=exceptionfile)
        print (username,"exception.")
        continue
    usermess = firststat.user
    print ("Username: " + username)
    #print ("USERid:", usermess.id_str)
    user = usermess.id_str
    headers = TI.user_parser(usermess,headerprint = True)
    userstring = TI.user_parser(usermess)
    print (headers,file=logfilepointer)
    print(userstring,file=logfilepointer)
    logfilepointer.flush()

    headers = "infosource" + "\t" + "infotarget"
    print (headers,file=logfilepointer)

    currentid = usermess.id_str

    followerlist = api.followers_ids(currentid)
    for foll in followerlist:
        outstring = currentid + "\t" + str(foll)
        print (outstring, file = logfilepointer)

    logfilepointer.flush()

    friendlist = api.friends_ids(currentid)
    for frie in friendlist:
        outstring = str(frie) + "\t" + currentid
        print (outstring, file = logfilepointer)

    logfilepointer.flush()
