import warnings
warnings.filterwarnings("ignore")
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import sys
import matplotlib.pyplot as plt
import copy

def series_to_dataframe(inseries):
    xlist = []
    ylist = []
    d = {}
    for xval in inseries.keys():
        xlist.append(xval)
        ylist.append(inseries[xval])
    d['x'] = xlist
    d['y'] = ylist
    df = pd.DataFrame(d)
    return df;


def make_dataframe_oned(measdict,onedmeaslist):
    d = {}
    for measure in onedmeaslist:
        measvalsdict = measdict[measure]
        newseries = pd.Series(measvalsdict)
        d[measure] = newseries
    df = pd.DataFrame(d)
    return df;

def make_series_tuplelist(tuplelist):
    d = {}
    for tuple in tuplelist:
        cleanedtuple = tuple.strip()
        cleanedtuple = cleanedtuple.replace("(","")
        cleanedtuple = cleanedtuple.replace(")","")
        brokentuple = cleanedtuple.split(",")
        xval = float(brokentuple[0])
        yval = float(brokentuple[1])
        d[xval]=yval
    sr = pd.Series(d)       
    return sr;
    #MAYBE EXTRACT XLIST, YLIST, MAKE EACH A SERIES, PUT IN DICT, X, Y, THEN DF
    ## OR CONVERT SR TO DF FOR PLOTTING -- prob better

def make_dataframe_twodtuples(measdict,measurename):
    d = {}
    measurevalsdict = measdict[measurename]
    for screenname in measurevalsdict.keys():
        d[screenname] = make_series_tuplelist(measurevalsdict[screenname])
    df = pd.DataFrame(d)
    return df;

def radar_plot_day(measurename,screenname,twoddict):
    titlestring = measurename + " : " + screenname
    currentdf = twoddict[measurename]
    sr = currentdf[accountname]
    oldlabelslist = sr.keys()
    numlabels = len(oldlabelslist)
    valueslist = []
    angleslist = []
    labelslist = []
    angles2list = []
    labels2list = []
    for i in range (0,numlabels):
        valueslist.append(int(sr[oldlabelslist[i]]))

        newangle = 2.0*3.14159*float(-1*i)/float(numlabels) + 3.14159/2.0 
        if newangle >= 2.0 * 3.14159:
            newangle = newangle - 2*3.14159
        elif newangle < 0:
            newangle = newangle + 2*3.14159
        angleslist.append(newangle)
        #angleslist.append(2.0*3.14159*float(i)/float(numlabels)) ## CCW starting at theta=0
        labelslist.append(round(int(oldlabelslist[i])/3600,2))
        if i%2 == 0:
            angles2list.append(newangle)
            labels2list.append(round(int(oldlabelslist[i])/3600,2))
    
    valueslist.append(valueslist[0])
    angleslist.append(angleslist[0])
    labels = np.array(labelslist)
    values = np.array(valueslist)
    angles = np.array(angleslist)
    angles2 = np.array(angles2list)
    labels2 = np.array(labels2list)
    fig=plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(angles2 * 180/np.pi, labels2)
    ax.set_title(titlestring)
    ax.grid(True)
    plt.show()
    return;
    
#TO DO: JOIN RADAR PLOTS INTO ONE PROCEDURE
def radar_plot_week(measurename,screenname,twoddict):
    titlestring = measurename + " : " + screenname
    currentdf = twoddict[measurename]
    sr = currentdf[accountname]
    oldlabelslist = sr.keys()
    oldnumlabels = len(oldlabelslist)
    oldvalueslist = []
    valueslist = []
    angleslist = []
    labelslist = []
    angles2list = []
    labels2list = []
    daysofweek=['Mo','Tu','We','Th','Fr','Sa','Su']
    for i in range (0,oldnumlabels):
        oldvalueslist.append(int(sr[oldlabelslist[i]]))
    numlabels = oldnumlabels/12
    numlabels = int(numlabels)
    for i in range (0, numlabels):
        value=0
        for j in range (0, 12):
            index = i*12 + j
            value +=oldvalueslist[index]
        valueslist.append(value)

        newangle = 2.0*3.14159*float(-1*i)/float(numlabels) + 3.14159/2.0 
        if newangle >= 2.0 * 3.14159:
            newangle = newangle - 2*3.14159
        elif newangle < 0:
            newangle = newangle + 2*3.14159
        angleslist.append(newangle)
        labelslist.append(round(int(oldlabelslist[i])/3600,2))
        angles2list.append(newangle)
        if i%4 == 0:
            labels2list.append(daysofweek[int(i/4)])
        else:
            labels2list.append("")
    
    valueslist.append(valueslist[0])
    angleslist.append(angleslist[0])
    labels = np.array(labelslist)
    values = np.array(valueslist)
    angles = np.array(angleslist)
    angles2 = np.array(angles2list)
    labels2 = np.array(labels2list)
    fig=plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-', color="red", linewidth=2)
    ax.fill(angles, values, "r",alpha=0.25)
    ax.set_thetagrids(angles2 * 180/np.pi, labels2)
    ax.set_title(titlestring)
    ax.grid(True)
    plt.show()
    return;


### MAIN BODY ###

delimiter = "\t"
centername = input("What is the file prefix? ")
infilename =centername+".collectedanalysis.tsv"
infile = open(infilename,"r",encoding="utf-8")

measuredict = {}
onedimensionalmeasureslist = []
twodimensionalmeasureslist = []
higherdimensionalmeasureslist = []
accountlist = []
for line in infile:
    cleanline = line.strip()
    valslist = cleanline.split(delimiter)
    if valslist[0] == "MEASURE": #new measure
        newmeasure = True
        measurename = valslist[1]
        measuredict[measurename] = {}
    else:
        screenname = valslist[0].lower()
        if screenname not in accountlist:
            accountlist.append(screenname)
        datalist = valslist[1:]
        if newmeasure:
            datumstring = datalist[0]
            if datumstring[0] == "(": #tuples = multidimensional
                datumlist = datumstring.split(",")
                if len(datumlist) == 2:
                    twodimensionalmeasureslist.append(measurename)
                    dimension = 2
                else:
                    higherdimensionalmeasureslist.append(measurename)
                    dimension = 3
            else:   #monodimensional
                onedimensionalmeasureslist.append(measurename)
                dimension = 1
            newmeasure = False
        if dimension == 1:
            try:
                measuredict[measurename][screenname]=float(datalist[0])
            except:
                measuredict[measurename][screenname]=datalist[0]
        else: #CURRENTLY ALL HIGHER DIMENSIONS
            measuredict[measurename][screenname]=datalist
onedimensional_dataframe = make_dataframe_oned(measuredict,onedimensionalmeasureslist)



twodimensional_dataframe_dict = {}
for measure in twodimensionalmeasureslist:
    newdf = make_dataframe_twodtuples(measuredict,measure)
    twodimensional_dataframe_dict[measure]=newdf



## SETTING CGSEIFE TO o, everything else to D
#markerlist = []
#for user in rawusertypelist:
#    if user == "cgseife":
#        markerlist.append("o")
#    else:
#        markerlist.append("D")
#markerarray = np.array(markerlist)

keepgoing = True
while keepgoing:
    print()
    print("L1 = list 1d measures; L2 = list 2d measures.")
    print("P1 = 1d plot; P1L, P1LL = 1d plot, semilog, log;")
    print ("C1, C1L, etc. = as above, but with color as 3rd dimension;")
    print ("P2 = 2d plot; M2 = Multiple 2d series in one plot.")
    print ("RD = day radar plot; RW = week radar plot.")
    print ("Screening tools: SR = day radar; SW = week radar; S2 = 2d.")
    command = input(">>> ")
    if command in ["Exit","EXIT","exit"]:
        keepgoing = False
    elif command in ["L1","l1"]:
        print ()
        print (onedimensionalmeasureslist)
    elif command in ["L2","l2"]:
        print ()
        print (twodimensionalmeasureslist)
    elif command in ["P1","p1","p1l","p1ll","P1L","P1LL"]:
        xaxisvar = input("   X-axis measure: ")
        yaxisvar = input("   Y-axis measure: " )
        titlestring = xaxisvar + " v. "+yaxisvar
        dforig = onedimensional_dataframe.copy()
        df = onedimensional_dataframe.copy()
        dfl = dforig.loc[dforig[xaxisvar]>0]
        dfll = dfl.loc[dfl[yaxisvar]>0]
        xislog = False
        yislog = False
        if command in ["P1L","P1LL","p1l","p1ll"]:
            xislog = True
            df = dfl
        else:
            xislog = False
        if command in ["p1ll","P1LL"]:
            yislog = True
            df = dfll
        else:
            yislog = False
        if xislog:
            df[xaxisvar] = np.log10(df[xaxisvar])
        if yislog:
            df[yaxisvar] = np.log10(df[yaxisvar])
        j = sns.jointplot(x=xaxisvar, y=yaxisvar, data=df)

        plt.show()
    elif command in ["P2","p2"]:
        variablename = input("   Measure name: ")
        accountname = input("   Account name: ")
        colorname = 'red'
        titlestring = variablename + " : " + accountname
        currentdf = twodimensional_dataframe_dict[variablename]
        sr = currentdf[accountname]
        j = sr.plot(kind="bar",color=colorname,title=titlestring,width=0.95)
        plt.show()
    elif command in ["M2","m2"]:
        variablename = input ("   Measure name: ")
        semilog = input ("   Semilog(T/F): ")
        if semilog in ["t","T","True","true","TRUE"]:
            xislog = True
        else:
            xislog = False
        currentdf = twodimensional_dataframe_dict[variablename]
        listofnamestoplot = []
        keepquerying = True
        while keepquerying:
            newnameraw = input ("    Screenname to add: ")
            newname = newnameraw.strip().lower()
            if newname != "":
                if newname in currentdf.keys():
                    listofnamestoplot.append(newname)
                else:
                    print("User",newname,"not found. Skipping...")
            else:
                keepquerying = False
        dftoplot = currentdf[listofnamestoplot]
        j=dftoplot.plot(logx=xislog,title=variablename)
        plt.show()
    elif command in ["RD","rd"]:
        variablename = input("   Measure name: ")
        accountname = input ("   Account name: ")
        radar_plot_day(variablename,accountname,twodimensional_dataframe_dict)
    elif command in ["RW","rw"]:
        variablename = input("   Measure name: ")
        accountname = input ("   Account name: ")
        radar_plot_week(variablename,accountname,twodimensional_dataframe_dict)
    elif command in ["C1","c1","c1ll","C1LL","c1l","C1L"]:
        df = onedimensional_dataframe.copy()
        xaxisvar = input("   X-axis measure: ")
        yaxisvar = input("   Y-axis measure: " )
        titlestring = xaxisvar + " v. "+yaxisvar
        df = onedimensional_dataframe.copy()
        dforig = onedimensional_dataframe.copy()
        dfl = dforig.loc[dforig[xaxisvar]>0]
        dfll = dfl.loc[dfl[yaxisvar]>0]
        yislog = False
        xislog = False
        if command in ["C1L","C1LL","c1l","c1ll"]:
            df = dfl
            xislog = True
        else:
            xislog = False
        if command in ["c1ll","C1LL"]:
            yislog = True
            df = dfll
        else:
            yislog = False
        if xislog:
            df[xaxisvar] = np.log10(df[xaxisvar])
        if yislog:
            df[yaxisvar] = np.log10(df[yaxisvar])
        colordimension = input("Color: A = usertype; B = botguess >> ")
        if colordimension.strip().lower() == "b":
            rawcolortypelist = df['botguess']
        else:
            rawcolortypelist = df['usertype']
        colortypelist = []
        colortypevector = []
        for color in rawcolortypelist:
            if color not in colortypelist:
                colortypelist.append(color)
            colortypevector.append(colortypelist.index(color))
        colortypearray = np.array(colortypevector)
        print ("  Color key:")
        for i in range (0,len(colortypelist)):
            print ("    ",colortypelist[i],"<>",i)
        df.plot(x=xaxisvar,y=yaxisvar,c=colortypearray, kind = 'scatter',s=20,cmap='gist_ncar',alpha=0.7)
        plt.show()
    elif command in ["SR","sr","sw","SW","S2","s2"]:
        if command in ["SR","sr"]:
            variablename = input("    Variable name? [daytweethisto] ")
            if variablename == "":
                variablename = "daytweethisto"
            for accountname in accountlist:
                try:
                    radar_plot_day(variablename,accountname,twodimensional_dataframe_dict)
                except:
                    print("Exception:",accountname)
        elif command in ["SW","sw"]:
            variablename = input("    Variable name? [weektweethisto] ")
            if variablename == "":
                variablename = "weektweethisto"
            for accountname in accountlist:
                try:
                    radar_plot_week(variablename,accountname,twodimensional_dataframe_dict)
                except:
                    print("Exception:",accountname)                    
        elif command in ["S2","s2"]:
            variablename = input("    Variable name? [bursthisto] ")
            if variablename == "":
                variablename = "bursthisto"
            currentdf = twodimensional_dataframe_dict[variablename]
            for accountname in accountlist:
                try:
                    titlestring = variablename + " : " + accountname
                    sr = currentdf[accountname]
                    colorname = 'red'
                    j = sr.plot(kind="bar",color=colorname,title=titlestring,width=0.95)
                    plt.show()
                except:
                    print("Exception:",accountname)
    else:
        print ("Command not recognized.")




