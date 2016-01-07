from splinter import Browser
import pafy
import io
from os import getcwd, path, makedirs
from traceback import format_exc
from time import sleep
from sys import exit

def download_progress(total, recvd, ratio, rate, eta):
    print(total, recvd, rate, eta)

file_name = "Dove Shampoo" # change here
folder_name = "downloads\\" + file_name + "\\"
if not path.exists(folder_name): makedirs(folder_name)

fh = io.open("reports\\" + file_name + ".xls", "w", encoding='utf8')
fh.write(u"tTitle\tAuthor\tUser Name\tCategory\tLikes\tDislikes\tDuration\tPublished\tRating\tView Count\tFile Name\n")
if not path.exists("reports"): makedirs("reports")
playlist_url = "https://www.youtube.com/playlist?list=PLaryEbODsc4bCmBLMlXOZeVrpQYJQzy4t" # change here
chrome = Browser("chrome")
print "visit 'chrome://settings/content' to disable images"
sleep(20)
chrome.visit(playlist_url)
sleep(5)
while chrome.is_element_present_by_xpath("//button[@class='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button']"):
    chrome.find_by_xpath("//button[@class='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button']").click()
    sleep(2)
sleep(5)
links = [a["href"] for a in chrome.find_by_xpath("//a[@class='pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link ']")]
chrome.quit()

playlist = pafy.get_playlist(playlist_url)
length = len(playlist['items'])
for i in range(1,length):
    try:
        details = playlist['items'][i]['playlist_meta']
        if details['length_seconds'] <= 120:
            title = details['title']
            print title
            author = details['author']
            username = details['user_id']
            category = details['category_id']
            description = details['description']
            likes = details['likes']
            dislikes = details['dislikes']
            duration = details['duration']
            published = details['added']
            rating = details['rating']
            viewcount = details['views']
            best = playlist['items'][i]['pafy'].getbest(preftype="mp4")
            filename = best.download(filepath=getcwd() + "\\" + folder_name, quiet=True, callback=download_progress)
            fh.write(title + u"\t" + author + u"\t" + str(username) + u"\t" + str(category) + u"\t" + str(likes) + u"\t" + str(dislikes) + u"\t" + duration + u"\t" + str(published) + u"\t" + str(rating) + u"\t" + str(viewcount) + u"\t" + filename + u"\n")
    except Exception, err:
        fh.write(title + u"\t" + author + u"\t" + str(username) + u"\t" + str(category) + u"\t" + str(likes) + u"\t" + str(dislikes) + u"\t" + duration + u"\t" + str(published) + u"\t" + str(rating) + u"\t" + str(viewcount) + u"\t" + filename + u"\n")
        print format_exc()
        continue
fh.close()
