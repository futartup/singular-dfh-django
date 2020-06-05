from .models import *
import elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Text, Date
from elasticsearch_dsl.connections import connections

connections.create_connection()

class VideoContentIndex(Document):    
    title = Text()    
    posted_date = Date()      
    text = Text()

    class Meta:        
        index = 'VideoContent-index'


def bulk_indexing():    
    BlogPostIndex.init()    
    es = Elasticsearch()    
    bulk(client=es, actions=(b.indexing() for b in VideoContent.objects.all().iterator()))


# Add indexing method to BlogPost
def indexing(self):   
    obj = BlogPostIndex(meta={'id': self.id}, title=self.title, posted_date=self.posted_date, text=self.text)   
    obj.save()   
    return obj.to_dict(include_meta=True)
