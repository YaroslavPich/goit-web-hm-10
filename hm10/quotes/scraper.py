from quotes.models import Quote, Author, Tag
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.db import IntegrityError

BASE_URL = "https://quotes.toscrape.com"


def scrape_quotes():
    url = BASE_URL
    has_next_page = True
    while has_next_page:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            quotes = soup.find_all("div", class_="quote")
            for quote_element in quotes:
                tags = [tag.text for tag in quote_element.find_all("a", class_="tag")]
                author_name = quote_element.find("small", class_="author").text
                quote_text = quote_element.find("span", class_="text").text

                try:
                    author, _ = Author.objects.get_or_create(fullname=author_name)

                    quote, created = Quote.objects.get_or_create(
                        text=quote_text,
                        author=author
                    )

                    if created:
                        for tag_name in tags:
                            tag, _ = Tag.objects.get_or_create(name=tag_name)
                            quote.tags.add(tag)
                except IntegrityError:
                    print(f"Skipping duplicate quote: {quote_text}")

            next_page = soup.find("li", class_="next")
            has_next_page = next_page is not None
            if has_next_page:
                next_page_url = next_page.find("a").attrs.get("href")
                url = urljoin(BASE_URL, next_page_url)
        except Exception as e:
            print(f"Error scraping quotes: {e}")


def scrape_authors():
    url = BASE_URL
    has_next_page = True
    while has_next_page:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        quotes = soup.find_all("div", class_="quote")
        for quote_element in quotes:
            author_link = quote_element.find("a").attrs.get("href")
            response_author = requests.get(urljoin(url, author_link))
            soup_author = BeautifulSoup(response_author.text, "lxml")
            author_name = soup_author.find("h3", class_="author-title").text.strip()
            born_date = soup_author.find("span", class_="author-born-date").text.strip()
            born_location = soup_author.find("span", class_="author-born-location").text.strip()
            description = soup_author.find("div", class_="author-description").text.strip()

            try:
                Author.objects.get_or_create(
                    fullname=author_name,
                    defaults={
                        'born_date': born_date,
                        'born_location': born_location,
                        'description': description
                    }
                )
            except IntegrityError:
                print(f"Skipping duplicate author: {author_name}")

        next_page = soup.find("li", class_="next")
        has_next_page = next_page is not None
        if has_next_page:
            next_page_url = next_page.find("a").attrs.get("href")
            url = urljoin(BASE_URL, next_page_url)


def scrape_quotes_and_authors():
    scrape_authors()
    scrape_quotes()