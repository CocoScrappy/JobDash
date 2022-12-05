from datetime import datetime, timedelta
import re


class ScrapeModel:

    def __init__(self,company,title,location,description,dateCreated,link):
        self.employer=-1
        self.company=company
        self.title=title
        self.location=location
        self.description=description
        self.dateCreated=self.calculatePostDate(dateCreated)
        self.link=link
    
    def calculatePostDate(self,daysAgoStr):
        if daysAgoStr.lower() != "today":
            daysAgoInt=int(re.sub(r'[^0-9]','',daysAgoStr.split()[0]))
            datePosted = datetime.today() - timedelta(days=daysAgoInt)
        else:
            datePosted=datetime.today()
            
        return datePosted.isoformat()

    def __str__(self):
        return f'External employer {self.company}, for {self.title} position in {self.location}.\nPosted on the {self.dateCreated}\nLink:{self.link}'
    
    def remove_html_tags(text):
        """Remove html tags from a string"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)