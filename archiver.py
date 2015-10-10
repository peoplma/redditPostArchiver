#!/usr/bin/env python
# -*- coding: utf-8 -*-

import praw
import snudown
import datetime
import time
import re
import sys
from requests.exceptions import HTTPError
import datetime
import os
import traceback
import requests
print "      __     __ _                            _                        _     _                "
print " the / /    / /| |                          (_)                      | |   (_)               "
print "    / / __ / /_| | ___   __ _  ___  ___ ___  _ _ __     __ _ _ __ ___| |__  ___   _____ _ __ "
print "   / / '__/ / _` |/   \ / _` |/ _ \/ __/ _ \| | '_ \   / _` | '__/ __| '_ \| \ \ / / _ \ '__|"
print "  / /| | / / (_| | (_) | (_| |  __/ (_| (_) | | | | | | (_| | | | (__| | | | |\ V /  __/ |  "
print " /_/ |_|/_/ \__,_|\___/ \__, |\___|\___\___/|_|_| |_|  \__,_|_|  \___|_| |_|_| \_/ \___|_| project"
print "                         __/ |   "
print "                        |___/           code-name: chugger  "
print "Code written by: /u/peoplma and /u/healdb"
print "Sillines added by: /u/joshtheimpaler"
print "Wow by: /r/dogecoin\n\n"
b = "timestamp:"
d = ".."

#Config Details-
r = praw.Reddit('searchandarchive by ')
def resume():
	if os.path.exists('config.txt'):
		line = file('config.txt').read()
		startStamp,endStamp,step,subName=line.split(',')
		startStamp,endStamp,step=int(startStamp),int(endStamp),int(step)
		return startStamp,endStamp,step,subName
	else:
		return 0
choice = input('\nMENU\nPlease choose one of the following:\n1. Start New Archive\n2. Continue Archiving\n3. Exit\n(Input the number)\n')
if(choice==1):
	subName=raw_input('Input the subreddit to archive: ')
	sdate=raw_input('Input start date in the format dd/mm/yyyy: ')
	startStamp= int(time.mktime(datetime.datetime.strptime(sdate, "%d/%m/%Y").timetuple()))
	edate=raw_input('Input end date in the format dd/mm/yyyy: ')
	endStamp= int(time.mktime(datetime.datetime.strptime(edate, "%d/%m/%Y").timetuple()))
	step=input('Input seconds between each search, 30 recommended: ')
	obj=file('config.txt','w')
	obj.write(str(startStamp)+','+str(endStamp)+','+str(step)+','+str(subName))
	obj.close()
elif(choice==2):
	try:
		startStamp,endStamp,step,subName=resume()
	except:
		print('Nothing to continue.')
		exit()
else:
	exit()	
sdate=datetime.datetime.fromtimestamp(int(startStamp)).strftime('%d-%m-%Y')
edate=datetime.datetime.fromtimestamp(int(endStamp)).strftime('%d-%m-%Y')
folderName=str(subName+' '+str(sdate)+' '+str(edate))
if not os.path.exists(folderName):
    os.makedirs(folderName)
""" 
Customization Configuration

"""
# Path to which to output the file #
outputFilePath1='./'
# The Path to the stylesheet, relative to where the html file will be stored #
pathToCSS='css/style.css'
"""
Reddit Post Archiver
By Samuel Johnson Stoever
"""

monthsList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def writeHeader(posttitle):
    htmlFile.write('<!DOCTYPE html>\n<html>\n<head>\n')
    htmlFile.write('\t<meta charset="utf-8"/>\n')
    htmlFile.write('\t<link type="text/css" rel="stylesheet" href="' + pathToCSS +'"/>\n')
    htmlFile.write('\t<title>' + posttitle + '</title>\n')
    htmlFile.write('</head>\n<body>\n')

def parsePost(postObject):
    writeHeader(fixUnicode(postObject.title))
    postObject.replace_more_comments()
    postAuthorName = ''
    postAuthorExists = 0
    try:
        postAuthorName = fixUnicode(postObject.author.name)
        postAuthorExists = 1
    except AttributeError:
    	postAuthorExists = 0
    htmlFile.write('<div class="title">\n')
    if postObject.is_self:
        # The post is a self post
        htmlFile.write(fixUnicode(postObject.title))
        htmlFile.write('\n<br/><strong>')
    else:
        # The post is a link post
        htmlFile.write('<a id="postlink" href="' + fixUnicode(postObject.url))
        htmlFile.write('">')
        htmlFile.write(fixUnicode(postObject.title))
        htmlFile.write('</a>\n<br/><strong>')
    if postAuthorExists:
        htmlFile.write('Posted by <a id="userlink" href="' + fixUnicode(postObject.author._url))
        htmlFile.write('">')
        htmlFile.write(postAuthorName)
        htmlFile.write('</a>. </strong><em>')
    else:
        htmlFile.write('Posted by [Deleted]. </strong><em>')
    htmlFile.write('Posted at ')
    postDate = time.gmtime(postObject.created_utc)
    htmlFile.write(str(postDate.tm_hour) + ':')
    htmlFile.write(str(postDate.tm_min) + ' UTC on ')
    htmlFile.write(monthsList[postDate.tm_mon-1] + ' ')
    htmlFile.write(str(postDate.tm_mday) + ', ' + str(postDate.tm_year))
    htmlFile.write('. ' + str(postObject.ups - postObject.downs))
    if postObject.is_self:
        htmlFile.write(' Points. </em><em>(self.<a id="selfLink" href="')
    else:
        htmlFile.write(' Points. </em><em>(<a id="selfLink" href="')
    htmlFile.write(postObject.subreddit._url)
    htmlFile.write('">' + postObject.subreddit.display_name)
    if postObject.is_self:
        htmlFile.write('</a>)</em><em>')
    else:
        htmlFile.write('</a> Subreddit)</em><em>')
    htmlFile.write(' (<a id="postpermalink" href="')
    htmlFile.write(fixUnicode(postObject.permalink))
    htmlFile.write('">Permalink</a>)</em>\n')
    if postObject.is_self:
        htmlFile.write('<div class="post">\n')
        htmlFile.write(snudown.markdown(fixMarkdown(postObject.selftext)))
        htmlFile.write('</div>\n')
    else:
        htmlFile.write('<div class="post">\n<p>\n')
        htmlFile.write(postObject.url)
        htmlFile.write('</p>\n</div>\n')
    htmlFile.write('</div>\n')
    for comment in postObject._comments:
        parseComment(comment, postAuthorName, postAuthorExists)
    htmlFile.write('<hr id="footerhr">\n')
    htmlFile.write('<div id="footer"><em>Archived on ')
    htmlFile.write(str(datetime.datetime.utcnow()))
    htmlFile.write(' UTC</em></div>')
    htmlFile.write('\n\n</body>\n</html>\n')
    #Done
def parseComment(redditComment, postAuthorName, postAuthorExists, isRoot=True):
    commentAuthorName = ''
    commentAuthorExists = 0
    try:
        commentAuthorName = fixUnicode(redditComment.author.name)
        commentAuthorExists = 1
    except AttributeError:
        commentAuthorExists = 0
    if isRoot:
        htmlFile.write('<div id="' + str(redditComment.id))
        htmlFile.write('" class="comment">\n')
    else:
        htmlFile.write('<div id="' + str(redditComment.id)) 
        htmlFile.write('" class="comment" style="margin-bottom:10px;margin-left:0px;">\n')
    htmlFile.write('<div class="commentinfo">\n')
    if commentAuthorExists:
        if postAuthorExists and postAuthorName == commentAuthorName:
            htmlFile.write('<a href="' + redditComment.author._url)
            htmlFile.write('" class="postOP-comment">' + commentAuthorName + '</a> <em>')
        else:
            htmlFile.write('<a href="' + redditComment.author._url)
            htmlFile.write('">' + commentAuthorName + '</a> <em>')
    else:
        htmlFile.write('<strong>[Deleted]</strong> <em>')
    htmlFile.write(str(redditComment.ups - redditComment.downs))
    htmlFile.write(' Points </em><em>')
    htmlFile.write('Posted at ')
    postDate = time.gmtime(redditComment.created_utc)
    htmlFile.write(str(postDate.tm_hour) + ':')
    htmlFile.write(str(postDate.tm_min) + ' UTC on ')
    htmlFile.write(monthsList[postDate.tm_mon-1] + ' ')
    htmlFile.write(str(postDate.tm_mday) + ', ' + str(postDate.tm_year))
    htmlFile.write('</em></div>\n')
    htmlFile.write(snudown.markdown(fixMarkdown(redditComment.body)))
    for reply in redditComment._replies:
        parseComment(reply, postAuthorName, postAuthorExists, False)
    htmlFile.write('</div>\n')
    #Done
def fixMarkdown(markdown):
    newMarkdown = markdown.encode('utf8')
    return re.sub('\&gt;', '>', str(newMarkdown))
def fixUnicode(text):
    return str(text.encode('utf8'))
# End Function Definitions
# r = praw.Reddit(user_agent='RedditPostArchiver Bot, version 0.93')
# Disclaimer, storing plain text passwords is bad.
# uncomment the following line to login (e.g., in case of Unable to Archive Post:
# r.login('username', 'password')
def getNew(subName,folderName):
    subreddit_comment = r.get_comments(subName, limit=1000)
    subreddit_posts = r.get_submissions(subName, limit=1000)
    for comment in subreddit_comment:
        print comment
        url= comment.permalink
        data= {'user-agent':'archive by /u/healdb'}
        #manually grabbing this file is much faster than loading the individual json files of every single comment, as this json provides all of it
        response = requests.get(url+'.json',headers=data)
        #Create a folder called dogecoinArchive before running the script
        filename=folderName+"/"+comment.name
        obj=open(filename, 'w')
        obj.write(response.text)
        obj.close()
        #print post_json
    for post in subreddit_posts:
        print post
        postID= (post.id)
        url1= post.permalink
        #pprint(vars(post))
        data= {'user-agent':'archive by /u/healdb'}
        #manually grabbing this file is much faster than loading the individual json files of every single comment, as this json provides all of it
        if submission.id not in already_done:
            response = requests.get(url1+'.json',headers=data)
            #Create a folder called dogecoinArchive before running the script
            filename=folderName+"/"+post.name
            obj=open(filename, 'w')
            obj.write(response.text)
            obj.close()
            #print post_json
            already_done.add(submission.id)
        else:
            continue
def main(startStamp,endStamp,step,folderName,subName,progress):
    count=step
    try:
        startStamp =open(folderName+"/lastTimestamp.txt").read()
        print("Resuming from timestamp: " + startStamp)
        time.sleep(3)
        startStamp=int(startStamp)
        progress=startStamp
    except: 
        pass
    c=1
    for currentStamp in range(startStamp,endStamp,step):
        e=' --'
        if(c%2==0):
            e=' |'
        f = str(currentStamp)
        g = str(currentStamp+step)
        search_results = r.search(b+f+d+g, subreddit=subName, syntax='cloudsearch')
        end=str((int((float(count)/float(progress)*20.0))*10)/2)+'%'
        print(('\n'*1000)+'Archiving posts and comments...\n['+'*'*int((float(count)/float(progress)*20.0))+'_'*(20-int(float(count)/float(progress)*20.0))+']'+end+e)
        count+=step
        for post in search_results:
            #print("---I found a post! It\'s called:" + str(post))
            url= (post.permalink).replace('?ref=search_posts','')
            postID= (post.id)
            #pprint(vars(post))
            data= {'user-agent':'archive by /u/healdb'}
            #manually grabbing this file is much faster than loading the individual json files of every single comment, as this json provides all of it
            response = requests.get(url+'.json',headers=data)
            #Create a folder called dogecoinArchive before running the script
            filename=folderName+"/"+post.name+'.json'
            obj=open(filename, 'w')
            obj.write(response.text)
            obj.close()
            #print post_json
            #print("I saved the post and named it " + str(post.name) + " .---")
            try:
                outputFilePath = outputFilePath1 + postID + '.html'
                thePost = r.get_submission(submission_id=postID)
                htmlFile = open(outputFilePath,'w')
                parsePost(thePost)
                htmlFile.close()
            except HTTPError: 
                print('Unable to Archive Post: Invalid PostID or Log In Required (see line 157 of script)')
            time.sleep(1)
        obj=open(folderName+"/lastTimestamp.txt", 'w')
        obj.write(str(currentStamp))
        obj.close()
        c+=1
    print('Welp, all done here! Stopped at timestamp '+ str(currentStamp))
progress = endStamp-startStamp
while True:
    try:
        main(startStamp,endStamp,step,folderName,subName,progress)
        print("Succesfully got all posts within parameters.")
        choice=input('You can now either\n1. Exit\n2. Get new posts\n(Input the number)\n')
        if(choice==1):
            exit()
        else:
            while True:
                getNew(subName,folderName)
    except KeyboardInterrupt:
        exit()
    except SystemExit:
        exit()
    except:
        print("Error in the program! The error was as follows: ")
        error = traceback.format_exc()
        time.sleep(5)
        print(error)
        time.sleep(5)
        print("Resuming in 5 seconds...")
        time.sleep(5)
