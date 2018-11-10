class movie:
    """Represents a Video from a Porn Site"""

    def __init__(self,):
        self.title = ""
        self.actors = []
        self.date = "" # This should eventually be a time field I think?
        self.rating = 0
        self.summary = ""
        self.tags = []
        self.site = ""
        self.images = []
        self.mainImage = ""

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
