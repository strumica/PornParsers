# Porn
import re
import os

# URLS
# EXC_BASEURL = 'http://restrictedsenses.com/'
# EXC_SEARCH_MOVIES = EXC_BASEURL + 'search?q=%s'
# EXC_MOVIE_INFO = EXC_BASEURL + 'main/store/hd-movie-clips/%s'
# EXC_MODEL_INFO = EXC_BASEURL + 'model/%s'

def Start():
    HTTP.CacheTime = CACHE_1DAY
    HTTP.Headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'
    #Log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~start~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def any(s):
    for v in s:
        if v:
            return True
    return False

class PornAgent(Agent.Movies):
    name = 'Porn'
    languages = [Locale.Language.English]
    accepts_from = ['com.plexapp.agents.localmedia']
    primary_provider = True
    Log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~KinkAgentClass~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    
    def search(self, results, media, lang):
        Log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Search~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # Log(media.name)
        # BetterName = media.name.replace(' ', '-').replace('-Movie','').upper()
        # Log(BetterName)
        Log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Search~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        title = media.name
        if media.primary_metadata is not None:
            title = media.primary_metadata.title
            results.Append(MetadataSearchResult(id = "MichaelsID", name = "Michaels Title1", score = 90, lang = lang))
        results.Append(MetadataSearchResult(id = media.name, name = title, score = 91, lang = lang))
        results.Sort('score', descending=True)

    def update(self, metadata, media, lang):
        Log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Update~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #
        #
        path = os.path.dirname(media.items[0].parts[0].file) #movie library:
        Log(path)
        KinkSites = ['Sadistic Rope', 'Whipped Ass', 'Wired Pussy']
        # if any(x in str for x in a):
        if any("PornTestFolder/"+x in path for x in KinkSites):
            Log("Kink.com Video")
            # videoName = "KinkSite"
            # metadata.title = "KinkSite"
            # URLS
            EXC_BASEURL = 'http://www.kink.com/'
            EXC_SEARCH_MOVIES = EXC_BASEURL + 'search?q=%s'
            EXC_MOVIE_INFO = EXC_BASEURL + 'shoot/%s'
            EXC_MODEL_INFO = EXC_BASEURL + 'model/%s'

            test = re.match(r'(?:[A-Za-z]{2,4}-)?(\d{3,})', metadata.title).group(1)
            Log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~test~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            Log(test)
            Log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~test2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            metadata.id = "30438"
            html = HTML.ElementFromURL(EXC_MOVIE_INFO % metadata.id, headers={'Cookie': 'viewing-preferences=straight%2Cgay'})

            # use site name as movie studio
            # add site name to genres
            metadata.genres.clear()
            try:
              sitename = html.xpath('//div[@class="shoot-page"]/@data-sitename')[0]
              for link in html.xpath('//a[contains(@href,"%s")]/text()' % sitename):
                if link.strip():
                  metadata.studio = link.strip()
                  metadata.genres.add(metadata.studio)
                  break
            except:
              pass

            # add channels to genres
            # add other tags to collections
            metadata.collections.clear()
            tags = html.xpath('//div[@class="shoot-info"]//a[starts-with(@href,"/tag/")]')
            for tag in tags:
              if tag.get('href').endswith(':channel'):
                if not metadata.studio:
                  metadata.studio = tag.text_content().strip()
                metadata.genres.add(tag.text_content().strip())
              else:
                metadata.collections.add(tag.text_content().strip())

            # set movie title to shoot title
            metadata.title = html.xpath('//div[@class="shoot-info"]//h1')[0].text_content() + " (" + metadata.id + ")"

            # set content rating to XXX
            metadata.content_rating = 'XXX'

            # set episode ID as tagline for easy visibility
            metadata.tagline = metadata.studio + " – " + metadata.id

            # set movie release date to shoot release date
            try:
              release_date = html.xpath('//div[@class="shoot-info"]//p[starts-with(.,"date:")]')[0].text_content().replace('date: ', '')
              metadata.originally_available_at = Datetime.ParseDate(release_date).date()
              metadata.year = metadata.originally_available_at.year
            except: pass

            # set poster to the image that kink.com chose as preview
            try:
              thumbpUrl = html.xpath('//video/@poster')[0]
              thumbp = HTTP.Request(thumbpUrl)
              metadata.posters[thumbpUrl] = Proxy.Media(thumbp)
            except: pass
            
            # fill movie art with all images, so they can be used as backdrops
            try:
              imgs = html.xpath('//div[@id="previewImages"]//img')
              for img in imgs:
                thumbUrl = re.sub(r'/h/[0-9]{3,3}/', r'/h/830/', img.get('src'))
                thumb = HTTP.Request(thumbUrl)
                metadata.art[thumbUrl] = Proxy.Media(thumb)
            except: pass

            # summary
            try:
              metadata.summary = ""
              summary = html.xpath('//div[@class="shoot-info"]/div[@class="description"]')
              if len(summary) > 0:
                for paragraph in summary:
                  metadata.summary = metadata.summary + paragraph.text_content().strip().replace('<br>',"\n") + "\n"
                metadata.summary.strip()
            except: pass

            # director
            try:
              metadata.directors.clear()
              director_id = html.xpath('//div[@class="shoot-page"]/@data-director')[0]
              director_html = HTML.ElementFromURL(EXC_MODEL_INFO % director_id,
                                                  headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
              director_name = director_html.xpath('//h1[@class="page-title"]')[0].text_content()
              try:
                director = metadata.directors.new()
                director.name = director_name
              except:
                try:
                  metadata.directors.add(director_name)
                except: pass
            except: pass
            
            # starring
            try:
              starring = html.xpath('//p[@class="starring"]/*[@class="names"]/a')
              metadata.roles.clear()
              for member in starring:
                role = metadata.roles.new()
                lename = member.text_content().strip()
                try:
                  role.name = lename
                except:
                  try:
                    role.actor = lename
                  except: pass
            except: pass

            # rating
            try:
              rating_dict = JSON.ObjectFromURL(url=EXC_BASEURL + 'api/ratings/%s' % metadata.id,
                                               headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
              metadata.rating = float(rating_dict['avgRating']) * 2
            except: pass
        elif "PornTestFolder/Restricted Senses" in path:
            Log("RestrictedSenses")
            EXC_BASEURL = 'http://restrictedsenses.com/'
            EXC_SEARCH_MOVIES = EXC_BASEURL + 'search?q=%s'
            EXC_MOVIE_INFO = EXC_BASEURL + 'main/store/hd-movie-clips/%s'
            EXC_MODEL_INFO = EXC_BASEURL + 'model/%s'
            metadata.id = metadata.id.replace(' ', '-').replace('-Movie','').upper()

            html = HTML.ElementFromURL(EXC_MOVIE_INFO % metadata.id) #,headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
            # videoName = html.xpath('//h1[@class="product_title"]')
            videoName = html.xpath('//h1/text()')[0]
            Summary = html.xpath('//div//p/text()')[0]


            MainPhoto = html.xpath('//a[@data-rel="prettyPhoto"]/@href')[0]
                # set poster to the image that kink.com chose as preview
            try:
                thumbpUrl = MainPhoto
                thumbpUrl = "http://restrictedsenses.com/main/wp-content/uploads/2017/11/RS-290-19.jpg"
                thumbp = HTTP.Request(thumbpUrl)
                metadata.posters[thumbpUrl] = Proxy.Media(thumbp)
                Log("PICTURE WAS SET")
            except: pass

            # Log("THIS IS THE PAYLOAD !!!!!!!!!!!!!!!!!!!!!!!" + str(html) + "THIS IS THE PAYLOAD !!!!!!!!!!!!!!!!!!!!!!!")

            # for thing in html:
            #     Log(thing[0])
            # html = HTML.ElementFromURL(EXC_MOVIE_INFO % metadata.id,headers={'Cookie': 'viewing-preferences=straight%2Cgay'})

            # set movie title to shoot title
            metadata.title = videoName[14:] #"Michaels Title" #html.xpath('//div[@class="shoot-info"]//h1')[0].text_content() + " (" + metadata.id + ")"
            # set content rating to XXX
            metadata.content_rating = 'XXX'

            # set episode ID as tagline for easy visibility
            metadata.tagline = "Michaels Tag Line" # metadata.studio + " – " + metadata.id

            # summary
            try:
                metadata.summary = Summary #"This is Michaels Summary"
                metadata.summary.strip()
            except: pass
        else:
            Log("OtherUnknownFolder")
            metadata.title = "UnknownSite"

        ### series library
        #for s in media.seasons:
        #  for e in media.seasons[s].episodes:
        #    dir = os.path.dirname( media.seasons[s].episodes[e].items[0].parts[0].file); break
        #  break
        # metadata.collections.clear() #clear all collection tags
        # reverse_folder_list = list(reversed(Utils.SplitPath(path))) #create 

        # for folder in reverse_folder_list:
            # Log(folder)
            #if len (folder) <= 3: break
            #metadata.collections.add(folder)



#rating_dict = JSON.ObjectFromURL(url=EXC_BASEURL + 'api/ratings/%s' % metadata.id,headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
#director_html = HTML.ElementFromURL(EXC_MODEL_INFO % director_id,headers={'Cookie': 'viewing-preferences=straight%2Cgay'})
#director_name = director_html.xpath('//h1[@class="page-title"]')[0].text_content()