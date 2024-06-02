import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',

  'DNT': '1',
  'Upgrade-Insecure-Requests': '1',
}

def get_data(url: str) -> str:
    answer = list()
    response = requests.get(url, headers=headers)
    qs_first = parse_qs(urlparse(url).query)
    print(f'FIRST: {qs_first}')
    final_url = response.url
    qs = parse_qs(urlparse(final_url).query)
    print(f'TWO: {qs}')
    if not qs:
        qs = qs_first
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    ans = soup.find_all('h2', id=qs[next(iter(qs))][0])
    print(ans)
    if ans:
        card = ans[0].find_parent('article')
        # Извлекаем текст из найденного элемента article
        card_text = card.get_text(separator='\n', strip=True)
        return f'"{card_text}"'
    print('ERROR! CARD IS NULL')
    return 'Not found information'
# def main():
#
#     adta = get_data('https://www.tinkoff.ru/business/help/business-payout/jump/about/recipient/')
#     with open('out.txt','w', encoding='utf-8') as f:
#         f.write(' '.join(adta))
#
#     pass