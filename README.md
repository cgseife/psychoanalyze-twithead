psychoanalyze-tweethead collection
November 6, 2018
Charles Seife, NYU
cs129@nyu

*** README ***

This code was only meant for my own use, so apologies for the ugliness. It's also far from my main activity, so please don't expect quick (or any!) response to bug fix requests, etc.

In addition to the files included, you need to make an apikeys.txt file that keeps your Twitter api keys (format: consumer_key|consumer_secret|access_token|accesstoken_secret).

Some programs in first three groups operate on a file that ends in ".namesfile"; each line in the namesfile has 2+  entries, delimited by tabs. Entry #1 (mandatory) = screen name of twitter user. Entry #2 (mandatory) = network label (for plotting). I've been using entry 3 for a measure of the confidence that I've got that the user is a bot, and entry 4 for my justification for that confidence, but YMMV. Sample included.

Bottleneck is the collector, thanks to the throttle on the API. Everything beyond that is relatively quick -- I haven't found the need to multiprocess. Each user gets two or more flat files, so the directory will fill up very quickly, but once the amalgamation of the analysis is done, you can move/discard those files.

Error handling is poor, and a few issues remain w/r/t data integrity (such as rare hiccups on bad characters.) 

As for streaming, my tweetstreamer is unstable, especially with high-volume keyword lists. Definitely room for improvement with everything in group 4.

Good luck!


*** tweetcollector folder ***

Group 1: Tweet analysis & plotting

1. tweetcollectorbatch.py
	For each user in a namefile, gather info and last ~3220 tweets
	IN: namefile; OUT:  tweetlogfile

2. tweetanalyzerbatch.py
	For each user in a namefile, analyze tweets contained in tweetlogfile
	IN: namefile, tweetlogfile; OUT: tweetanalysis

3. analysiscollectorbatch.py
	Collect all tweetanalyses related to a namefile in one large file
	IN: namefile, tweetanalysis; OUT: collectedanalysis

4. analysisplotter.py
	Plots all tweetanalyses in one collectedanalysis file
	IN: collectedanalysis


Group 2: Comms network generation from collected tweets

1. retweetedgeanalyzerbatch.py
	For each user in a namefile, extract edges&nodes (RTs and @s) from tweetlogfile
	IN: namefile, tweetlogfile; OUT: retweetedges

2. collectrtedgesbatch.py
	Collect all retweetedges files related to a namefile, place into 2 node/edge files
	IN: namefile, retweetedges; OUT: collectedrtedges, collectedrtnodes


Group 3: Followers/friends network generation

1. networkfollowercollectorbatch.py
	For each user in a namefile, extract followers and friends
	OUT: followers

2. collectrtedgesbatch.py
	Collect all followers files related to a namefile, place into 2 node/edge files
	IN: namefile, followers; OUT: collectedfollowedges, collectedfollownodes


Group 4: Stream monitoring via keyword/user

1. tweetstreamer.py
	Using keywords or user ID number, records all relevant tweets that come through stream
	OUT: streamlogfile

2. threadifyer.py
        Using the stream log file, attempts to identify threads
	OUT: threadedlogfile

3. threadparser.py
	Using the threaded log file, attempts to find parent->child relationships
	OUT: parsedlogfile, which can be modified for use in Gephi.