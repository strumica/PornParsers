from lxml import html
import requests
from Movie import movie

# page to parse: http://www.hardtied.com/hogtied/bondage/gallery.php?type=full&page=&page=201
page = requests.get('http://www.hardtied.com/hogtied/bondage/gallery.php?type=full&page=&page=75')
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
    vid.date = mainPartOfPage.xpath('*//span[@class="articlePostDateText"]')[0].text_content()

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
    
    # Find Main Photo:
    # //img[@height=658]
    mainPhoto = mainPartOfPage.xpath('*//img[@height=658]')
    # print(mainPhoto)
    
    vid.site = siteURL

    movies.append(vid)
print(movies)
