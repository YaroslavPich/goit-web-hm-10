import os
import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hm10.settings")
django.setup()

from quotes.models import Quote, Tag, Author

client = MongoClient("mongodb+srv://userweb8:8426@cluster0.ue8ckn7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.homework

authors = db.authors.find()

for author in authors:
    author_obj, created = Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        tag_obj, created = Tag.objects.get_or_create(name=tag)
        tags.append(tag_obj)

    if not Quote.objects.filter(text=quote['quote']).exists():
        author_fullname = quote.get('author')
        if author_fullname:
            author_obj = Author.objects.filter(fullname=author_fullname).first()
            if author_obj:
                quote_obj = Quote.objects.create(
                    text=quote['quote'],
                    author=author_obj
                )
                quote_obj.tags.set(tags)
                quote_obj.save()
