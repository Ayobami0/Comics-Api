import re
import asyncio
import aiohttp
import time

from bs4 import BeautifulSoup
import requests

# DEAFAULTS
"""
page = 1
orby = ''  az, newest, topview
keyw = ''  keyword to search for comic title
"""


def format_url(page=1, orby='', keyw=''):
    page_url = f"https://manganato.com/advanced_search?s=all&page={page}&orby={orby}&keyw={keyw}"
    return page_url


async def extract_meta_data(url):
    all_comic_list = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            webData = await resp.text()

        soup = BeautifulSoup(webData, 'html.parser')

        comicData = soup.find_all("div", class_="content-genres-item")
        for div in comicData[:2]:
            comic_img = div.find(class_="img-loading")['src']
            comic_name_info = div.find(class_="genres-item-name")
            comic_name = comic_name_info.get_text()
            comic_link = comic_name_info['href']
            comic_author = div.find(class_="genres-item-author").get_text()
            comic_description = div.find(class_="genres-item-description").get_text()
            comic_views = div.find(class_="genres-item-view").get_text()

            chapter_list = await extract_comic_pages(session, comic_link)

            all_comic_list.append({
                'title': comic_name,
                'metadata': {
                    'image': comic_img,
                    'link': comic_link,
                    'author': comic_author,
                    'views': comic_views,
                    'description': comic_description
                },
                'chapters': chapter_list,
            })
    return all_comic_list


async def extract_comic_pages(session, comic_page_link):
    async with session.get(comic_page_link) as resp:
        comic_page_data = await resp.text()
        comic_soup = BeautifulSoup(comic_page_data, "html.parser")

        comic_chapter_data = comic_soup.find_all('a', class_="chapter-name")

        full_chapters = []

        for chapters in comic_chapter_data:
            chapter_name = chapters['title']
            chapter_link = chapters['href']
            full_chapters.append({'name': chapter_name, 'link': chapter_link})

    return full_chapters


async def extract_comic_images(session, chapter_link):
    async with session.get(chapter_link) as resp:
        comic_image_data = resp.text()
        image_soup = BeautifulSoup(comic_image_data, "html.parser")

        image_tags = image_soup.find_all('img', src=re.compile('mkklcdnv'))

        image_urls = {}

        for page_no, url in enumerate(image_tags):
            image_urls[page_no] = url['src']

    return image_urls
