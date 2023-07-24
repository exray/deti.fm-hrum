import requests
import re, os
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def collect_data():
    today_date = datetime.now().strftime('%d-%m-%Y')
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': UserAgent().random
    }
    response = requests.get(url='https://detifm.ru/fairy_tales/id/120', headers=headers)
    with open(f'index.html', 'w', encoding='UTF8') as file:
        file.write(response.text)

    with open(f'index.html', encoding='UTF8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    tales = soup.find_all('button', class_='podcast__play ym')
    tales_count = re.search(r'\d+', soup.find('div', class_='tale-episodes__dop-info').h2.text).group()
    
    tale_number = 1
    mp3_folder = 'files'
    for tale in tales:
        tale_title = tale['data-track-title']
        tale_mp3_url = tale['data-track']
        tale_fullname = f'{mp3_folder}/{tale_title}.mp3'
        
        try:
            if not os.path.exists(tale_fullname):
                mp3_file = requests.get(tale_mp3_url)
                with open(tale_fullname, 'wb') as mp3:
                    mp3.write(mp3_file.content)
                print(f'[{tale_number}/{tales_count}] Файл "{tale_title}" успешно скачан.')
            else:
                print(f'[{tale_number}/{tales_count}] Файл "{tale_title}" уже существует')
        except:
            pass
        finally:
            tale_number += 1


def main():
    collect_data()

if __name__ == '__main__':
    main()