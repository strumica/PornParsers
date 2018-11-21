from lxml import html
import requests
from Movie import movie
from datetime import date
from dateutil.parser import parse
import time

# http://www.societysm.com/updates07/updates.html


def parseSocietySmPage(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # This will create a list of Videos on that page:
    movies = []
    #                   '//*[@id="updates"]/tbody/tr/td/table[*]/tbody/tr/td/table[4]/tbody/tr/td[1]/a'
    # allLinks = tree.xpath('//a')#/table[*]/tbody/tr/td/table[4]/tbody/tr/td[1]/a')
    
    allDateAndModels = tree.xpath('//*[@class="updatename"][@align="left"]')
    # print(allDateAndModels)
    for eachDateAndModel in allDateAndModels:
        dateAndModelString = eachDateAndModel.text_content()
        dateUnparsed, actorUnparsed = dateAndModelString.split(" - ")
        print(dateUnparsed)
        
        actors = []
        if "," in actorUnparsed:
            actorsSplit = actorUnparsed.split(",")
            for actor in actorsSplit:
                actors.append(actor.strip())
        else:
            actors.append(actorUnparsed.strip())
        print(actors)

        # up 4 parents
        FourUp = eachDateAndModel.getparent().getparent().getparent().getparent()
        # print(FourUp)
        par = FourUp.xpath('.//*[@class="p1"]')[0]
        summary = par.text_content()
        print(summary)

        hasMovieLink = False
        movieUrl = ""
        # Lets Find a link if it exists.
        allLinks = FourUp.xpath('.//a')
        for eachLink in allLinks:
            movieUrl = eachLink.get("href")
            if "http://www.societysm.com/updates" in movieUrl:
                siteID = movieUrl.split("/")[-2]
                print("{}".format(movieUrl))
                print("{}".format(siteID))
                hasMovieLink = True
        
        if hasMovieLink:
            moviePage = requests.get(movieUrl)
            movieTree = html.fromstring(moviePage.content)
            titleTag = movieTree.xpath('//td[@class="heading"]')[0]
            titleTagText = titleTag.text_content()
            if 'Preview for "' in titleTagText:
                movieTitle = titleTagText.split('Preview for "')[1].split('"')[0]
                print(movieTitle)
                # sleep(5)
        
        print("\n")

    # print(len(dateAndModel))
    # for link in allLinks: 
    #     urlOfLink = link.get("href")
    #     textOfLink = link.text_content()
    #     if "http://www.societysm.com/updates" in urlOfLink:
    #         print(urlOfLink)
    #         print(textOfLink)
    #     vid = movie()

    #     siteURL = "http://www.societysm.com"
        # lets find a perMovie url
        # postUrl = eachVideo.xpath('//*[@id="updates"]/tbody/tr/td/table[*]/tbody/tr/td/table[4]/tbody/tr/td[1]/a')#[0].get("href")

        # uniqueVidUrl = siteURL+postUrl
        # # print(uniqueVidUrl)
        # uniquePage = requests.get(uniqueVidUrl)
        # uniquePageTree = html.fromstring(uniquePage.content)
        # mainPartOfPage = uniquePageTree.xpath('//table[@class="articleWrapper"]')[0]
        
        # # Find Title and Actress(es)
        # for x in mainPartOfPage.xpath('*//span[@class="articleTitleText"]'):
        #     # print(x.text_content())
        #     innerTextSplit = x.text_content().split("|")
        #     vid.title = innerTextSplit[0].strip()
        #     # print(innerTextSplit)
        #     for eachActor in innerTextSplit[1:]:
        #         vid.actors.append(eachActor.strip())
        # # Find Date of Video
        # uglyDate = mainPartOfPage.xpath('*//span[@class="articlePostDateText"]')[0].text_content()
        # vid.date = parse(uglyDate)

        # # Find Summary:
        # for x in mainPartOfPage.xpath('*//*[@class="articleCopyText"]'):
        #     # print(x.text_content())
        #     vid.summary = x.text_content()
        
        # # Find Tags:
        # try:
        #     tagBlock = uniquePageTree.xpath('//*[@class="articleTagsText"]')[0].text
        #     strippedBeginning = tagBlock[5:]
        #     seperatedByCommas = strippedBeginning.replace("\t", "").replace("\n", "").split(", ")
        #     AllTags = []
        #     for eachTag in seperatedByCommas:
        #         AllTags.append(eachTag.strip())
        #     # print("block: ",AllTags)
        #     vid.tags = AllTags
        # except :
        #     pass
        
        # # Find All Images:
        # allPhotos = mainPartOfPage.xpath('*//img')
        # # print(allPhotos)
        # for x in allPhotos:
        #     url = x.get("src")
        #     if "poster.jpg" in url:
        #         # print(url)
        #         vid.mainImage = url
        #     else:
        #         fullSizeImage = x.getparent().get("href")
        #         if "images" in fullSizeImage:
        #             vid.images.append(fullSizeImage)
            
        # vid.site = siteURL

        # movies.append(vid)
    return movies


startURL = 'http://www.societysm.com/updates07/updates{}.html'
startIndex = 1
endIndex = 1
movies = []
for x in range(startIndex,endIndex+1):
    eachSetOfMovies = parseSocietySmPage(startURL.format(x))
    # for eachMovie in eachSetOfMovies:
    #     requests.get(eachMovie.createAddMovieUrl())
    movies+= eachSetOfMovies
    # time.sleep(8)
print(movies)
