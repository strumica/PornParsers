from datetime import date

class movie:
    """Represents a Video from a Porn Site"""

    def __init__(self,):
        self.title = ""
        self.actors = []
        self.date = date(1, 1, 1) #"" # This should eventually be a time field I think?
        self.rating = 0
        self.summary = ""
        self.tags = []
        self.site = ""
        self.images = []
        self.mainImage = ""
        self.movieID = ""


    def __repr__(self):
        # return str(self.title)
        output = "\n"
        output += "Title: {}\n".format(self.title)
        output += "Actors: {}\n".format(self.actors)
        output += "Date: {}\n".format(self.date)
        output += "Rating(0-10): {}\n".format(self.rating)
        output += "Summary: {}\n".format(self.summary)
        output += "Tags: {}\n".format(self.tags)
        output += "Site: {}\n".format(self.site)
        output += "Images: {}\n".format(self.images)
        output += "Main Image: {}\n".format(self.mainImage)
        
        return output

    def __str__(self):
        output = "\n"
        output += "Title: {}\n".format(self.title)
        output += "Actors: {}\n".format(self.actors)
        output += "Date: {}\n".format(self.date)
        output += "Rating(0-10): {}\n".format(self.rating)
        output += "Summary: {}\n".format(self.summary)
        output += "Tags: {}\n".format(self.tags)
        output += "Site: {}\n".format(self.site)
        output += "Images: {}\n".format(self.images)
        output += "Main Image: {}\n".format(self.mainImage)
        return output

    def createAddMovieUrl(self):
        output = "http://127.0.0.1:8000/movies/addMovie/"
        output += "?title={}".format(self.title.replace("&", "%26"))
        for eachActor in self.actors:
            output += "&actor={}".format(eachActor.replace("&", "%26"))
        output += "&date={}".format(self.date)
        output += "&rating={}".format(self.rating)
        output += "&summary={}".format(self.summary.replace("&", "%26"))
        for eachTag in self.tags:
            output += "&tag={}".format(eachTag.replace("&", "%26"))
        output += "&site={}".format(self.site)
        for img in self.images:
            output += "&minorImage={}".format(img.replace("&", "%26"))
        if self.mainImage != "":
            output += "&mainImage={}".format(self.mainImage.replace("&", "%26"))
        return output