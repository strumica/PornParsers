from lxml import html
import requests
from Movie import movie

# page to parse: http://www.hardtied.com/hogtied/bondage/gallery.php?type=full&page=&page=201
page = requests.get('http://www.hardtied.com/hogtied/bondage/gallery.php?type=full&page=&page=201')
tree = html.fromstring(page.content)

# This will create a list of Videos on that page:
movies = []
videos = tree.xpath('//table[@class="articleWrapper"]')
for eachVideo in videos:
    vid = movie()
    # Find Title and Actress(es)
    for x in eachVideo.xpath('*//span[@class="articleTitleText"]'):
        # print(x.text_content())
        innerTextSplit = x.text_content().split("|")
        vid.title = innerTextSplit[0].strip()
        # print(innerTextSplit)
        for eachActor in innerTextSplit[1:]:
            vid.actors.append(eachActor.strip())
    # Find Date of Video
    vid.date = eachVideo.xpath('*//span[@class="articlePostDateText"]')[0].text_content()

    # Find Summary:
    for x in eachVideo.xpath('*//*[@class="articleCopyText"]'):
        # print(x.text_content())
        vid.summary = x.text_content()
    
    # Find Main Photo:
    # //img[@height=658]
    mainPhoto = eachVideo.xpath('*//img[@height=658]')
    print(mainPhoto)
    
    print('\n')
    movies.append(vid)
print(movies)
