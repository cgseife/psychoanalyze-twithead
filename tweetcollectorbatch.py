## Batch Twitter info/history collector
## Charles Seife, cs129@nyu.edu

import tweepy
import time
import datetime
import twitterinfrastructure as TI


### MAIN BODY ###


keyfilename = "apikeys.txt"

api = TI.get_api (keyfilename)

namesfilesuffix = ".namesfile"
logfilesuffix = ".tweetlogfile.tsv"

batchfilename = input("Prefix of file containing batch: ")
batchfilepointer = open(batchfilename+namesfilesuffix,"r",encoding="utf-8")
exceptionfilename = "exceptions."+ batchfilename
exceptionfile = open (exceptionfilename,"w",encoding="utf-8")
for batchline in batchfilepointer:
    usernameraw = batchline.split("\t")[0]
    username = usernameraw.strip().lower()
    

    logfilename = username+logfilesuffix

    logfilepointer = open (logfilename,"w",encoding="utf-8")


    statpagelist = TI.get_fullstatuslist(username,api)
    try:
        firststat = statpagelist[0][0]
    except:
        print (username,file=exceptionfile)
        continue
    user = firststat.user
    headers = TI.user_parser(user,headerprint = True)
    userstring = TI.user_parser(user)
    print (headers,file=logfilepointer)
    print(userstring,file=logfilepointer)
    logfilepointer.flush()

    headers = TI.status_parser(firststat,"",headerprint = True)
    print (headers,file=logfilepointer)

    for statpage in statpagelist:
        for stat in statpage:
            outstring = TI.status_parser(stat,TI.get_full_tweet(stat))
            print(outstring,file = logfilepointer)
    logfilepointer.flush()

