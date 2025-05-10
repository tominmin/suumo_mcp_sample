import httpx
from bs4 import BeautifulSoup

SUUMO_DETAIL = "https://suumo.jp"

def scrape_suumo_list(url: str):
    res = httpx.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    print(soup)
    results = []

    for b in soup.select(".cassetteitem"):
        title = b.select_one(".cassetteitem_content-title")
        address = b.select_one(".cassetteitem_detail-col1")
        price = b.select_one(".cassetteitem_other-emphasis")
        madori = b.select_one(".cassetteitem_madori")
        manseki = b.select_one(".cassetteitem_menseki")
        url = b.select_one(".js-cassette_link_href")

        results.append({
            "title": title.text.strip() if title else "",
            "address": address.text.strip() if address else "",
            "madori": madori.text.strip() if madori else "",
            "menseki": manseki.text.strip() if manseki else "",
            "price": price.text.strip() if price else "",
            "url": f"{SUUMO_DETAIL}{url.get('href')}" if url else "",
        })
    return {"results": results, "count": len(results)} 