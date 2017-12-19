import textrank
import click
import scrapy
from attr._make import fields

filename = "/Users/julia/UIUC/CS410/Project/Lessons/Week3/Lesson3.3/subtitles.vtt"
fileout = "/Users/julia/UIUC/CS410/Project/CS410mat/Week3/Lesson3.3.html"
imgdir = "/Users/julia/UIUC/CS410/Project/Slides/Week3/Lesson3.3/"

ignore_list = "WEBVTT, [MUSIC],[INAUDIBLE]"
stack = ""

curminute = "00:00:00.000"
curtext = []
newMinute = True
fout = open(fileout,"w+")



def toHTML(text):
    global fout
    fout.write("<p>")
    fout.write(text)
    fout.write("</p>")
    fout.write("\n")

def toHTML2(text):
    global fout
    fout.write(text)
    fout.write("\n")
    
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

def process_line(line):    
    global curminute
    global curtext
    global newMinute
    if len(line) > 0:
        words = line.split()
        if not ifcounter(words):
            if istimestampline(words):
                if issameminute(curminute, words[0]) == False:
                    toHTML(curminute)
                    curminute = words[0]
                    newMinute = True                    
            else:
                if newMinute == True:
                    newMinute = False
                    toHTML(" ".join(curtext))
                    imgcommand = "<img src=\"" + imgdir + "img0" + getmin(curminute) + ".jpg\"" + ">"
                    toHTML2(imgcommand)
                    del curtext[:]
                for word in words: 
                    if word not in ignore_list:
                        curtext.append(word)


message = """<html>
<head>Lesson 3.3</head>
<body>"""

fout.write(message)



with open(filename) as f:
    for line in f:
        line = line.rstrip()
        process_line(line)
  
message = """
</body>
</html>"""  
fout.close()

print "All done"