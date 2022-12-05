import json
import sys
from channels.generic.websocket import WebsocketConsumer
from job_posting.websocket.scraper.scrape import scraper
from channels.exceptions import StopConsumer

class ScraperConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    
    def disconnect(self, close_code):
        raise StopConsumer()

    def receive(self, text_data):
        text_data_json=json.loads(text_data)
        searchTerm=text_data_json["searchTerm"]
        searchLocation=text_data_json["searchLocation"]
        print(text_data_json,file=sys.stderr)
        scraper(searchTerm,searchLocation,self)
        self.disconnect(0)
        