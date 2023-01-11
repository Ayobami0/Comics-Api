# Asura scans
# Mangakakalot
# ReaperScans
# Flamescans
import re

from bs4 import BeautifulSoup
import soupsieve as sv
import requests

pageUrl = "https://manganato.com/advanced_search?s=all&page=1"

webData = requests.get(pageUrl).content

soup = BeautifulSoup(webData, 'html.parser')

comicData = sv.select(".content-genres-item", soup)


def extract_meta_data(div):
    comic_img = div.find(class_="img-loading")['src']
    comic_name_info = div.find(class_="genres-item-name")
    comic_name = comic_name_info.get_text()
    comic_link = comic_name_info['href']
    comic_author = div.find(class_="genres-item-author").get_text()
    comic_description = div.find(class_="genres-item-description").get_text()
    comic_views = div.find(class_="genres-item-view").get_text()

    return {
        'name': comic_name,
        'image': comic_img,
        'link': comic_link,
        'author': comic_author,
        'views': comic_views,
        'description': comic_description
    }


def extract_comic_pages(comic_page_link):
    comic_page_data = requests.get(comic_page_link).content

    comic_soup = BeautifulSoup(comic_page_data, "html.parser")

    comic_chapter_data = comic_soup.find_all('a', class_="chapter-name")

    full_chapters = []

    for chapters in comic_chapter_data:
        chapter_name = chapters['title']
        chapter_link = chapters['href']
        full_chapters.append({'name': chapter_name, 'link': chapter_link})

    return full_chapters


def extract_comic_images(chapter_link):
    comic_image_data = requests.get(chapter_link).content

    image_soup = BeautifulSoup(comic_image_data, "html.parser")

    image_urls = image_soup.find_all('img', src=re.compile('mkklcdnv'))

    for url in image_urls:
        print(requests.get(
                  url['src'],
                  headers={"referer": chapter_link}
              ).url)

    return image_urls


extract_comic_images(extract_comic_pages(extract_meta_data(comicData[0])['link'])[0]['link'])
