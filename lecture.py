import textrank
import click
import scrapy
from attr._make import fields
import os

ignore_list = "WEBVTT, [MUSIC],[INAUDIBLE], [SOUND], >>"
stack = ""

curminute = "00:00:00.000"
curtext = []
newMinute = True



def toHTML(fhtml, text):
    fhtml.write("<p>")
    fhtml.write(text)
    fhtml.write("</p>")
    fhtml.write("\n")

def toHTML2(fhtml, text):
    fhtml.write(text)
    fhtml.write("\n")
    
def getmin(timestamp):
    fields = splitTS(timestamp)
    return fields[1]

def ifcounter(words):
    if len(words) == 1 and words[0].isdigit() == True:
        return True
    return False

def splitTS(timestamp):
    fieldst = timestamp.split(".")
    fields = fieldst[0].split(":")
    fields.append(fieldst[1])
    if len(fields) != 4:
        return ""  
    return fields

def issameminute(ts1, ts2):
    fields1 = splitTS(ts1)
    fields2 = splitTS(ts2)
    if len(fields1) == 4 and len(fields2) == 4 and fields1[0] == fields2[0] and fields1[1] == fields2[1] : 
       return True
    return False

def istimestampline(words):
    if len(words) == 3 and words[1] == "-->":
        fields1 = splitTS(words[0])        
        fields2 = splitTS(words[2])        
        if len(fields1) == 4 and len(fields2) == 4:
            for dig in fields1:
                if not dig.isdigit():
                    return False
            for dig in fields2:
                if not dig.isdigit():
                    return False
            return True
    return False

def process_line(fhtml, imgdir, line):    
    global curminute 
    global curtext
    global newMinute
    if len(line) > 0:
        words = line.split()
        if not ifcounter(words):
            if istimestampline(words):
                if issameminute(curminute, words[0]) == False:
                    toHTML(fhtml, curminute)
                    curminute = words[0]
                    newMinute = True                    
            else:
                if newMinute == True:
                    newMinute = False
                    toHTML(fhtml, " ".join(curtext))
                    imgcommand = "<img src=\"" + imgdir + "/img0" + getmin(curminute) + ".jpg\"" + ">"
                    toHTML2(fhtml, imgcommand)
                    del curtext[:]
                for word in words: 
                    if word not in ignore_list:
                        curtext.append(word)


def createLecture(c_radir, htmldir, imgdir, lname):
    global curminute
    global curtext 
    global newMinute 
    
    curminute = "00:00:00.000"
    curtext = []
    newMinute = True
    
    message = """<html>
    <head><h2>"""
    message += lname
    message += """</h2></head>
    <body>"""
    
    htmlfile = htmldir + "/" + lname + ".html"
    fhtml = open(htmlfile,"w+")
    fhtml.write(message)
    
    c_ravtt = c_radir + "/subtitles.vtt"

    with open(c_ravtt) as f:
        for line in f:
            line = line.rstrip()
            process_line(fhtml, imgdir, line)
  
        message = """
        </body>
        </html>"""  
        fhtml.close()



def makeImageDir(lname):
    tmpname = lecturedir
    if os.path.exists(tmpname) == False:
        os.mkdir(tmpname)
    tmpname += "/images"
    if os.path.exists(tmpname) == False:
        os.mkdir(tmpname)
    tmpname += "/" + lname
    if os.path.exists(tmpname) == False:
        os.mkdir(tmpname)
    return tmpname

def makeHtmlDir():   
    tmpname = lecturedir
    if os.path.exists(tmpname) == False:
        os.mkdir(tmpname)
    tmpname += "/lectures"
    if os.path.exists(tmpname) == False:
        os.mkdir(tmpname)
    return tmpname
    
        
def callFfmpeg(c_radir, imgdir):
    cmd = ffmpeg + " -i " + c_radir + "/index.mp4 -vf fps=1/60 " + imgdir + "/img%03d.jpg"
    var = os.system(cmd)
    
def kwToString(keywords):
    lk = list(keywords)
    return ", ".join(lk)

def firstSentence(txttext):
    import re
    sentences = re.split('\. |: |;', txttext)
    return sentences[0] + "."

def cleanText(txttext):
    return ' '.join(filter(lambda x: x not in ignore_list,  txttext.split()))

def __main__ ():
    courseras = os.listdir(courseradir)
    
    hdir = makeHtmlDir()
    
    rootHtmlName = hdir + "/Lectures.html"
    
    message = """<html>
    <head><h2>Lectures</h2></head>
    <body>"""
    
    fhtml = open(rootHtmlName,"w+")
    fhtml.write(message)

    for d in courseras:
        if(d[0] != "."):
            print "Processing " + d
            idir = makeImageDir(d)
            callFfmpeg(courseradir + "/" + d, idir)           
            createLecture(courseradir + "/" + d , hdir, idir, d)
            toHTML(fhtml, "<a href=" + hdir +"/" + d + ".html>" + d + "</a>" )
            txtfile = courseradir + "/" + d + "/subtitle.txt"
            with open(txtfile) as f:
                txttext = f.read()
                txttext = cleanText(txttext)
                fs = firstSentence(txttext)
                toHTML(fhtml, "<b>" + fs + "</b>")
                print "Creating summary for " + d
                summary = textrank.extract_sentences(txttext)
                toHTML(fhtml, "<u>Summary:</u>")
                toHTML(fhtml, summary)
                print "Collecting keywords " + d
                keywords = textrank.extract_key_phrases(txttext)                
                toHTML(fhtml, "<u>Key-phrases:</u>")
                toHTML(fhtml, kwToString(keywords))
    message = """
    </body>
    </html>"""  
    fhtml.close()

from config import courseradir
from config import lecturedir 
from config import ffmpegdir
from config import ffmpeg

if courseradir == "" or  lecturedir == "" or ffmpegdir == "":
	print "Improper configuration. Fix config.py"
else : 
	__main__()

print "All done"
