import re
import aiohttp

from bs4 import BeautifulSoup

# DEAFAULTS
"""
page = 1
orby = ''  az, newest, topview
keyw = ''  keyword to search for comic title
"""
"""Obscene contents are removed by default"""


def format_url(page=1, orby="", keyw=""):
    page_url = f"https://manganato.com/advanced_search?s=all&page={page}&orby={orby}&keyw={keyw}"
    return page_url


async def fetch(site):
    """Fetch data from url"""
    async with aiohttp.ClientSession() as session, session.get(site) as response:
        return await response.text()


async def extract_meta_data(url):
    all_comic_list = []

    webData = await fetch(url)

    soup = BeautifulSoup(webData, "html.parser")

    comicData = soup.find_all("div", class_="content-genres-item")
    for div in comicData:
        comic_img = div.find(class_="img-loading")["src"]
        comic_name_info = div.find(class_="genres-item-name")
        comic_name = comic_name_info.get_text()
        comic_link = comic_name_info["href"]
        comic_id = re.compile(r"manga-\w+").findall(comic_link)[0]
        comic_author = div.find(class_="genres-item-author").get_text()
        comic_description = div.find(
            class_="genres-item-description").get_text()
        comic_views = div.find(class_="genres-item-view").get_text()
        comic_last_updated = div.find(class_="genres-item-time").get_text()

        all_comic_list.append(
            {
                "title": comic_name,
                "id": comic_id,
                "metadata": {
                    "image": comic_img,
                    "author": comic_author,
                    "views": comic_views,
                    "description": comic_description,
                    "last_update_time": comic_last_updated,
                },
            }
        )
    return all_comic_list


async def extract_comic_pages(comic_id, chapter=None):
    comic_page_link = f"https://chapmanganato.com/{comic_id}"

    if chapter is not None:
        read_chapter = await extract_comic_images(comic_page_link, chapter)
        return read_chapter

    comic_page_data = await fetch(comic_page_link)
    comic_soup = BeautifulSoup(comic_page_data, "html.parser")

    comic_chapter_data = comic_soup.find_all("a", class_="chapter-name")
    info = comic_soup.find_all("td", class_="table-value")
    comic_alternative_name = info[0].get_text()
    comic_authors = [author.get_text() for author in info[1].find_all("a")]
    comic_status = info[2].get_text()
    comic_genres = [genre.get_text() for genre in info[3].find_all("a")]

    comic_rating = comic_soup.find(
        "em", attrs={"property": "v:average"}).get_text()
    comic_updated_time = comic_soup.find(
        "span", class_="stre-value").get_text()
    comic_description = comic_soup.find(
        "div", class_="panel-story-info-description"
    ).get_text()

    full_chapters = {
        "rating": comic_rating,
        "chapters": [],
        "description": comic_description,
        "updated_time": comic_updated_time,
        "alternative": comic_alternative_name,
        "authors": comic_authors,
        "status": comic_status,
        "genres": comic_genres
    }

    # loops through chapter
    for chapters in comic_chapter_data:
        chapter_name = chapters["title"]
        chapter_link = chapters["href"]
        full_chapters["chapters"].append(
            {"name": chapter_name, "link": chapter_link})
    return full_chapters


async def extract_comic_images(chapter_link, chapter):
    comic_image_data = await fetch(f"{chapter_link}/chapter-{chapter}")
    image_soup = BeautifulSoup(comic_image_data, "html.parser")

    image_tags = image_soup.find_all("img", src=re.compile("mkklcdnv"))

    image_urls = {}

    for page_no, url in enumerate(image_tags):
        image_urls[page_no] = url["src"]

    return image_urls
