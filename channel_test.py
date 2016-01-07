from splinter import Browser
import pafy
import io
from os import getcwd, path, makedirs
from traceback import format_exc
from time import sleep
from sys import exit

def download_progress(total, recvd, ratio, rate, eta):
    print(total, recvd, rate, eta)

file_name = "Lakme Channel" # change here
folder_name = "downloads\\" + file_name + "\\"
if not path.exists(folder_name): makedirs(folder_name)
if not path.exists("reports"): makedirs("reports")
fh = io.open("reports\\" + file_name + ".xls", "w", encoding='utf8')
fh.write(u"URL\tTitle\tAuthor\tUser Name\tCategory\tLikes\tDislikes\tDuration\tPublished\tRating\tView Count\tFile Name\n")

channel_url = "https://www.youtube.com/user/ILoveLakme/videos" # change here
chrome = Browser("chrome")
print "visit 'chrome://settings/content' to disable images"
sleep(20)
chrome.visit(channel_url)
sleep(5)
while chrome.is_element_present_by_xpath("//button[@class='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button']"):
      chrome.find_by_xpath("//button[@class='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button']").click()
      sleep(2)
sleep(5)
links = [a["href"] for a in chrome.find_by_xpath("//a[@class='yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2']")]
chrome.quit()
#flag = False
for url in links:
    try:
        video = pafy.new(url)
        if video.length <= 120:
            title = video.title # .encode('ascii', 'ignore')
            print title
            #if title == "rexona men in philippines": flag = True
            #if flag:
            author = video.author # .encode('ascii', 'ignore')
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
            filename = best.download(filepath=getcwd() + "\\" + folder_name, quiet=True, callback=download_progress)
            fh.write(url + u"\t" + title + u"\t" + author + u"\t" + username + u"\t" + category + u"\t" + str(likes) + u"\t" + str(dislikes) + u"\t" + duration + u"\t" + published + u"\t" + str(rating) + u"\t" + str(viewcount) + u"\t" + filename + u"\n")
    except Exception, err:
        print format_exc()
        continue
fh.close()
