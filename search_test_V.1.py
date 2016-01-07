from splinter import Browser
from easygui import *
import pafy
import io
from os import getcwd, path, makedirs
from traceback import format_exc
from time import sleep
from sys import exit

def download_progress(total, recvd, ratio, rate, eta):
    print(total, recvd, rate, eta)

#GUI Creation
msg = "Enter the keyword to search"
title = "Youtube TVC Scrapper"
fieldNames = ["Enter the Brand Name :",
              "No. of pages to be scrapped :"]
fieldValues = multenterbox(msg, title, fieldNames)

while 1:
    if fieldValues is None:
        break
    errmsg = ""
    for i in range(len(fieldNames)):
        if fieldValues[i].strip() == "":
            errmsg += '"%s" is a required field.\n\n' % fieldNames[i]
    if errmsg == "":  # if no problems found
        break
    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

if fieldValues is None:
    exit(0)
    
#file_name = "lux shampoo ad" # change name here
folder_name = "downloads\\" + fieldValues[0].lower() + "\\"
if not path.exists(folder_name): makedirs(folder_name)
pages = fieldValues[1]

report_folder = "reports\\"
if not path.exists(report_folder): makedirs(report_folder)
fh = io.open("reports\\" + fieldValues[0].lower() + ".xls", "w", encoding='utf8')

fh.write(u"URL\tTitle\tAuthor\tUser Name\tCategory\tLikes\tDislikes\tDuration\tPublished\tRating\tView Count\tFile Name\n")

chrome = Browser("chrome")
#print "visit 'chrome://settings/content' to disable images"
sleep(5)

links = []
page_no = 1
while page_no <= int(pages): # change page no here
    search_url = "https://www.youtube.com/results?search_query=" + "+".join(fieldValues[0].split()) + "&filters=video&page=" + str(page_no)
    chrome.visit(search_url)
    sleep(2)
    for a in chrome.find_by_xpath("//a[@class='yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2       spf-link ']"):
        links.append(a["href"]) 
    page_no += 1
chrome.quit()

# flag = False
for url in links:
    try: 
        video = pafy.new(url)
        if video.length <= 120:
            title = video.title 
            print title
            # if title == "rexona men in philippines": flag = True
            # if flag:
            author = video.author
            username = video.username
            category = video.category
            description = video.description
            likes = video.likes
            dislikes = video.dislikes
            duration = video.duration
            published = video.published
            rating = video.rating
            viewcount = video.viewcount
            best = video.getbest(preftype="mp4")
            filename = ""
            filename = best.download(filepath=getcwd() + "\\" + folder_name, quiet=True, callback=download_progress)
            fh.write(url + u"\t" + title + u"\t" + author + u"\t" + username + u"\t" + category + u"\t" + str(likes) + u"\t" + str(dislikes) + u"\t" + duration + u"\t" + published + u"\t" + str(rating) + u"\t" + str(viewcount) + u"\t" + filename + u"\n")
    except Exception, err:
        fh.write(url + u"\t" + title + u"\t" + author + u"\t" + username + u"\t" + category + u"\t" + str(likes) + u"\t" + str(dislikes) + u"\t" + duration + u"\t" + published + u"\t" + str(rating) + u"\t" + str(viewcount) + u"\t" + filename + u"\n")
        print format_exc()
        continue
fh.close()
