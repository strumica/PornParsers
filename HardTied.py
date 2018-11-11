from lxml import html
import requests
from Movie import movie
from datetime import date
from dateutil.parser import parse
import time

# page to parse: 'http://www.hardtied.com/hogtied/bondage/gallery.php?type=full&page=&page=75'
# Looks like this script with MINOR editing should work with:
# http://www.hardtied.com
# http://www.sensualpain.com
# http://www.aganmedon.com
# http://www.paintoy.com
# http://www.sexuallybroken.com
# http://www.topgrl.com
# http://www.realtimebondage.com


def parseHardtiedPage(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # This will create a list of Videos on that page:
    movies = []
    videos = tree.xpath('//table[@class="articleWrapper"]')
    for eachVideo in videos:

        vid = movie()

        siteURL = "http://www.hardtied.com"
        # lets find a perMovie url
        postUrl = eachVideo.xpath('*//span[@class="articleTitleText"]/a')[0].get("href")
        uniqueVidUrl = siteURL+postUrl
        # print(uniqueVidUrl)
        uniquePage = requests.get(uniqueVidUrl)
        uniquePageTree = html.fromstring(uniquePage.content)
        mainPartOfPage = uniquePageTree.xpath('//table[@class="articleWrapper"]')[0]
        
        # Find Title and Actress(es)
        for x in mainPartOfPage.xpath('*//span[@class="articleTitleText"]'):
            # print(x.text_content())
            innerTextSplit = x.text_content().split("|")
            vid.title = innerTextSplit[0].strip()
            # print(innerTextSplit)
            for eachActor in innerTextSplit[1:]:
                vid.actors.append(eachActor.strip())
        # Find Date of Video
        uglyDate = mainPartOfPage.xpath('*//span[@class="articlePostDateText"]')[0].text_content()
        vid.date = parse(uglyDate)

        # Find Summary:
        for x in mainPartOfPage.xpath('*//*[@class="articleCopyText"]'):
            # print(x.text_content())
            vid.summary = x.text_content()
        
        # Find Tags:
        try:
            tagBlock = uniquePageTree.xpath('//*[@class="articleTagsText"]')[0].text
            strippedBeginning = tagBlock[5:]
            seperatedByCommas = strippedBeginning.replace("\t", "").replace("\n", "").split(", ")
            AllTags = []
            for eachTag in seperatedByCommas:
                AllTags.append(eachTag.strip())
            # print("block: ",AllTags)
            vid.tags = AllTags
        except :
            pass
        
        # Find All Images:
        allPhotos = mainPartOfPage.xpath('*//img')
        # print(allPhotos)
        for x in allPhotos:
            url = x.get("src")
            if "poster.jpg" in url:
                # print(url)
                vid.mainImage = url
            else:
                fullSizeImage = x.getparent().get("href")
                if "images" in fullSizeImage:
                    vid.images.append(fullSizeImage)
            
        vid.site = siteURL

        movies.append(vid)
    return movies


startURL = 'http://www.hardtied.com/hogtied/bondage/gallery.php?type=full&page=&page='
startIndex = 1
endIndex = 202
movies = []
for x in range(startIndex,endIndex+1):
    eachSetOfMovies = parseHardtiedPage(startURL+str(x))
    for eachMovie in eachSetOfMovies:
        requests.get(eachMovie.createAddMovieUrl())
    movies+= eachSetOfMovies
    time.sleep(8)
# print(movies)
# for eachMovie in movies:
#     requests.get(eachMovie.createAddMovieUrl())