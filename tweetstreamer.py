## Tweet streamer
## Charles Seife, cs129@nyu.edu
##
## To be honest, I don't quite grok the streaming interface yet. Expect
## instability.
##
## ID is not the screen name, but the Twitter ID number.
#

import tweepy
import time
import datetime
import sys

import twitterinfrastructure as TI


### STREAMING STUFF ####

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global globalfp
        outstring = TI.status_parser(status,TI.strip_badchars(status.text))
        print (outstring, file=globalfp, flush = True)
        print(">>",status.user.screen_name, status.text)
        return;

    def on_error(self, status_code):
        print ("<<>>Error code>",status_code)
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False;
        return True;


### MAIN BODY ###

keyfilename = "apikeys.txt"

api = TI.get_api (keyfilename)
mystreamlistener = MyStreamListener()
mystream = tweepy.Stream(auth = api.auth, listener=mystreamlistener)

logfileprefix = input ("Logfile prefix? ")
logfilesuffix = ".streamlogfile.tsv"
logfilename = logfileprefix+logfilesuffix
logfilepointer = open (logfilename,"w",encoding="utf-8")
globalfp = logfilepointer
headers = TI.status_parser("","",headerprint = True)
print (headers,file=globalfp)

answer = input("By [I]D number or by [k]eywords? ")
if answer in ["i","I"]:
    userid = input("ID of whose tweets to log: ")
    mystream.filter(follow=[userid])
elif answer in ["k","K"]:
    keywordlist = []
    counter = 1
    kw = "XX"
    while kw!= "":
        newkw = input ("Please enter keyword "+str(counter)+" or <CR> to exit: ")
        kw = newkw.strip().lower()
        if kw!="":
            keywordlist.append(kw)
            counter+=1
    if len(keywordlist)>=1:
        mystream.filter(track=keywordlist)
else:
    print ("Answer not recognized. Exiting.")
    

logfilepointer.flush()


