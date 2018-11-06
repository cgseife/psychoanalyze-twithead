## Crappy Twitter-analysis infrastructure
## Charles Seife, cs129@nyu.edu

import tweepy
import time
import datetime
import sys


def strip_badchars(instring):
    badcharlist = ["\t","\n","\r","\v","\f"]
    outstring = instring
    for c in badcharlist:
        outstring = outstring.replace(c,"|")
    return outstring;

def ensure_string(instring):
    if instring == None:
        instring = ""
    instring = strip_badchars(str(instring))
    return instring;

def user_parser(user, delimiter="\t",headerprint = False,addsuffix=""):
    outstring = ""
    if headerprint:
        outstring ='id_str'+addsuffix
        outstring = outstring + delimiter + 'name'+addsuffix
        outstring = outstring + delimiter + 'screen_name'+addsuffix
        outstring = outstring + delimiter + 'url'+addsuffix
        outstring = outstring + delimiter + 'description'+addsuffix
        outstring = outstring + delimiter + 'protected'+addsuffix
        outstring = outstring + delimiter + 'verified'+addsuffix
        outstring = outstring + delimiter + 'followers_count'+addsuffix
        outstring = outstring + delimiter + 'friends_count'+addsuffix
        outstring = outstring + delimiter + 'listed_count'+addsuffix
        outstring = outstring + delimiter + 'favourites_count'+addsuffix
        outstring = outstring + delimiter + 'statuses_count'+addsuffix
        outstring = outstring + delimiter + 'created_at'+addsuffix
        outstring = outstring + delimiter + 'utc_offset'+addsuffix
        outstring = outstring + delimiter + 'time_zone'+addsuffix
        outstring = outstring + delimiter + 'geo_enabled'+addsuffix
        outstring = outstring + delimiter + 'lang'+addsuffix
        outstring = outstring + delimiter + 'profile_background_color'+addsuffix
        outstring = outstring + delimiter + 'profile_link_color'+addsuffix
        outstring = outstring + delimiter + 'profile_sidebar_border_color'+addsuffix
        outstring = outstring + delimiter + 'profile_sidebar_fill_color'+addsuffix
        outstring = outstring + delimiter + 'profile_use_background_image'+addsuffix
        outstring = outstring + delimiter + 'withheld_in_countries'+addsuffix
        outstring = outstring + delimiter + 'withheld_scope'+addsuffix
        outstring = outstring + delimiter + 'recordmadeon'+addsuffix
    else:
        id_str = user.id_str
        name = user.name
        screen_name = user.screen_name
        try:
            url = ensure_string(user.url)
        except:
            url = ""
        try:
            description = ensure_string(user.description)
        except:
            description = ""
        protected = ensure_string(user.protected)
        verified = ensure_string(user.verified)
        followers_count = ensure_string(user.followers_count)
        friends_count = ensure_string(user.friends_count)
        listed_count = ensure_string(user.listed_count)
        favourites_count = ensure_string(user.favourites_count)
        statuses_count = ensure_string(user.statuses_count)
        created_at = ensure_string(user.created_at)
        try:
            utc_offset = ensure_string(user.utc_offset)
        except:
            utc_offset = ""
        try:
            time_zone = ensure_string(user.time_zone)
        except:
            time_zone = ""
        try:
            geo_enabled = ensure_string(user.geo_enabled)
        except:
            geo_enabled = ""
        try:
            lang = ensure_string(user.lang)
        except:
            lang = ""
        try:
            profile_background_color = ensure_string(user.profile_background_color)
        except:
            profile_background_color = ""
        try:
            profile_link_color = ensure_string(user.profile_link_color)
        except:
            profile_link_color = ""
        try:
            profile_sidebar_border_color = ensure_string(user.profile_sidebar_border_color)
        except:
            profile_sidebar_border_color = ""
        try:
            profile_sidebar_fill_color = ensure_string(user.profile_sidbar_fill_color)
        except:
            profile_sidebar_fill_color = ""
        try:
            profile_use_background_image = ensure_string(user.profile_use_background_image)
        except:
            profile_use_background_image = ""
        try:
            withheld_in_countries = ensure_string(user.withheld_in_countries)
        except:
            withheld_in_countries = ""
        try:
            withheld_scope= ensure_string(user.withheld_scope)
        except:
            withheld_scope = ""
        nowdate = datetime.datetime.now()
        nowstring = nowdate.strftime("%Y-%m-%d %H:%M:%S")
        outstring = id_str
        outstring = outstring + delimiter + name
        outstring = outstring + delimiter + screen_name
        outstring = outstring + delimiter + url
        outstring = outstring + delimiter + description
        outstring = outstring + delimiter + protected
        outstring = outstring + delimiter + verified
        outstring = outstring + delimiter + followers_count
        outstring = outstring + delimiter + friends_count
        outstring = outstring + delimiter + listed_count
        outstring = outstring + delimiter + favourites_count
        outstring = outstring + delimiter + statuses_count
        outstring = outstring + delimiter + created_at
        outstring = outstring + delimiter + utc_offset
        outstring = outstring + delimiter + time_zone
        outstring = outstring + delimiter + geo_enabled
        outstring = outstring + delimiter + lang
        outstring = outstring + delimiter + profile_background_color
        outstring = outstring + delimiter + profile_link_color
        outstring = outstring + delimiter + profile_sidebar_border_color
        outstring = outstring + delimiter + profile_sidebar_fill_color
        outstring = outstring + delimiter + profile_use_background_image
        outstring = outstring + delimiter + withheld_in_countries
        outstring = outstring + delimiter + withheld_scope
        outstring = outstring + delimiter + nowstring
    return outstring;

def status_parser(twitterstatus, fulltext, delimiter = "\t", headerprint = False):
    outstring = ""
    if headerprint:
        outstring = "created_at"
        outstring = outstring + delimiter + 'id_str'
        outstring = outstring + delimiter + 'full_text'
        outstring = outstring + delimiter + 'source'
        outstring = outstring + delimiter + 'truncated'
        outstring = outstring + delimiter + 'in_reply_to_status_id_str'
        outstring = outstring + delimiter + 'in_reply_to_user_id_str'
        outstring = outstring + delimiter + 'in_reply_to_screen_name'
        outstring = outstring + delimiter + 'quoted_status_id_str'
        outstring = outstring + delimiter + 'is_quote_status'
        outstring = outstring + delimiter + 'filter_level'
        outstring = outstring + delimiter + 'quote_count'
        outstring = outstring + delimiter + 'reply_count'
        outstring = outstring + delimiter + 'retweet_count'
        outstring = outstring + delimiter + 'favorite_count'
        outstring = outstring + delimiter + 'favorited'
        outstring = outstring + delimiter + 'retweeted'
        outstring = outstring + delimiter + 'possibly_sensitive'
        outstring = outstring + delimiter + 'lang'
        outstring = outstring + delimiter + 'rtuserscreen_name'
        outstring = outstring + delimiter + user_parser("", delimiter="\t",headerprint = True,addsuffix="_tweeter")
    else:
        created_at = str(twitterstatus.created_at)
        id_str = twitterstatus.id_str
        source = str(twitterstatus.source)
        truncated = str(twitterstatus.truncated)
        try:
            in_reply_to_status_id_str =ensure_string(twitterstatus.in_reply_to_status_id_str)
        except:
            in_reply_to_status_id_str = ""
        try:
            in_reply_to_user_id_str =ensure_string(twitterstatus.in_reply_to_user_id_str)
        except:
            in_reply_to_user_id_str = ""
        try:
            in_reply_to_screen_name =ensure_string(twitterstatus.in_reply_to_screen_name)
        except:
            in_reply_to_screen_name = ""
            
        try:
            quoted_status_id_str = ensure_string(twitterstatus.quoted_status_id_str)
        except:
            quoted_status_id_str = ""
        is_quote_status = str(twitterstatus.is_quote_status)
        try:
            filter_level= str(twitterstatus.filter_level)
        except:
            filter_level = ""
        try:
            quote_count = str(twitterstatus.quote_count)
        except:
            quote_count = ""
        try:
            reply_count = str(twitterstatus.reply_count)
        except:
            reply_count = ""
        try:
            retweet_count = str(twitterstatus.retweet_count)
        except:
            retweet_count = ""
        try:
            favorite_count = str(twitterstatus.favorite_count)
        except:
            favorite_count = ""
        try:
            favorited = str(twitterstatus.favorited)
        except:
            favorited = ""
        try:
            retweeted = str(twitterstatus.retweeted)
        except:
            retweeted = ""
        try:
            possibly_sensitive = str(twitterstatus.possibly_sensitive)
        except:
            possibly_sensitive = ""
        lang = str(twitterstatus.lang)
        try:
            retweeted_status = twitterstatus.retweeted_status
            retweeteduser = retweeted_status.user
            RTUserScreen_name = retweeteduser.screen_name
        except:
            RTUserScreen_name = ""
        #coordinates are useless
        #entities might be useful at some point
   
        try:
            userscreen_name=ensure_string(twitterstatus.user.screen_name)
        except:
            userscreen_name = ""

        try:
            tweeteruser=twitterstatus.user
            tweeterinfostring = user_parser(tweeteruser)
        except:
            tweeterinfostring = ""
        outstring = created_at
        outstring = outstring + delimiter + id_str
        outstring = outstring + delimiter + fulltext
        outstring = outstring + delimiter + source
        outstring = outstring + delimiter + truncated
        outstring = outstring + delimiter + in_reply_to_status_id_str
        outstring = outstring + delimiter + in_reply_to_user_id_str
        outstring = outstring + delimiter + in_reply_to_screen_name       
        outstring = outstring + delimiter + quoted_status_id_str
        outstring = outstring + delimiter + is_quote_status
        outstring = outstring + delimiter + filter_level
        outstring = outstring + delimiter + quote_count
        outstring = outstring + delimiter + reply_count
        outstring = outstring + delimiter + retweet_count
        outstring = outstring + delimiter + favorite_count
        outstring = outstring + delimiter + favorited
        outstring = outstring + delimiter + retweeted
        outstring = outstring + delimiter + possibly_sensitive
        outstring = outstring + delimiter + lang
        outstring = outstring + delimiter + RTUserScreen_name
        outstring = outstring + delimiter + tweeterinfostring
    return outstring;

def get_api(keyfilename):
    keyfile = open(keyfilename,"r")
    keyslist = keyfile.read().split("|")
    consumer_key = keyslist[0].strip()
    consumer_secret = keyslist[1].strip()
    access_token = keyslist[2].strip()
    access_token_secret = keyslist[3].strip()
    keyfile.close()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    newapi = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)    
    return newapi;


def get_fullstatuslist (screenname,api,verbose=True):
    statuslist = []
    counter = 0
    try:
        for page in tweepy.Cursor(api.user_timeline, screen_name=screenname, tweet_mode='extended').pages():
            counter+=1
            statuslist.append(page)
            if verbose:
                print ("      Captured %i tweets..."%(counter*20))
    except:
        if verbose:
            print ("Tweet problem:",screenname)        
    return statuslist;

def get_full_tweet(currentstatus):
    full_text_retweeted = currentstatus._json.get("retweeted_status")
    if None != full_text_retweeted:
        outtext = str( full_text_retweeted.get("full_text"))
    else:
        outtext =str(currentstatus._json["full_text"] )
    outtext = ensure_string(outtext)
    return outtext;

### ANALYSIS STUFF ###

def lookup_value(header,headerlist,datalist,cast='none'):
    indexnum = headerlist.index(header.lower())
    rawvalue = datalist[indexnum].strip()
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


def extract_simpleuseranalysis(datalist,headerlist,fp):
    answersdict = {}
    followers = lookup_value("followers_count",headerlist,datalist,'int')
    friends = lookup_value("friends_count",headerlist,datalist,'int')
    favscount = lookup_value("favourites_count",headerlist,datalist,'int')
    tweetcount = lookup_value("statuses_count",headerlist,datalist,'int')
    created=lookup_value("created_at",headerlist,datalist,'datetime')
    recorddate = lookup_value("recordmadeon",headerlist,datalist,'datetime')
    deltatime = recorddate - created
    deltasecs = deltatime.total_seconds()
    deltadays = deltasecs/86400
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
    answersdict ["longevity"] = deltadays
    answersdict["tweetrate"] = tweetrate
    answersdict["favrate"] = favrate
    answersdict["follrate"] = follrate
    answersdict["friendrate"]=friendrate
    answersdict["tweetfollratio"] = tweetfollratio
    answersdict["tweetfavratio"] = tweetfavratio
    return answersdict;

