# FragileDesires.py
# http://www.fragiledesires.com/2017/archives/001
# http://www.fragiledesires.com/2017/page/1 This will get the main image
# http://www.fragiledesires.com/2017/members/080 I think this works best. this gets the title


from lxml import html
import requests
from Movie import movie
from datetime import date
from dateutil.parser import parse
import time


def parseFragileDesires(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    movies = []
    # //*[@class="attachment-home-image size-home-image wp-post-image"]
    videos = tree.xpath('//*[@class="attachment-home-image size-home-image wp-post-image"]')
    # print(videos)
    for eachVideo in videos:
        vid = movie()

        # url of MainPic
        urlOfMainPic = eachVideo.get("src")
        vid.mainImage = urlOfMainPic
        # print(urlOfMainPic)

        vid.site = "http://www.FragileDesires.com"

        # url to MainVid
        linkToVideoPage = eachVideo.getparent().get("onclick").split("'")[1]
        # print(linkToVideoPage)

        if ("member" in linkToVideoPage) or ("archives" in linkToVideoPage) :
            # Site specific ID
            siteSpecificID = urlOfMainPic.split("/")[-1][:-4]
            vid.movieID = siteSpecificID
            # print(siteSpecificID)

            pageOfEachVid = requests.get(linkToVideoPage)
            treeOfEachVid = html.fromstring(pageOfEachVid.content)

            title = treeOfEachVid.xpath('//*[@class="single_title"]')[0].text[6:]
            # print(title)
            vid.title = title

            # Adding Nana as the only Actress
            vid.actors.append("Nana")
            
            print(vid.createAddMovieUrl())
            requests.get(vid.createAddMovieUrl())



        else: #not a real video...like the 1st thing which is a diary entry
            pass

url = "http://www.fragiledesires.com/2017/page/"



for x in range(1,9):
    parseFragileDesires(url+str(x))
    time.sleep(5)