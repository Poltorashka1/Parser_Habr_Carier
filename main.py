import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv


CSV = 'vacancy.csv'
ua = UserAgent()
url = 'https://career.habr.com/vacancies?q=Python&type=all'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': ua.random
}


def get_html(url, params=None):
    respons = requests.get(url, headers=headers, params=params)
    return respons


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all('div', class_='vacancy-card__inner')
    vacancy = []
    for item in content:
        vacancy.append(
            {
                'Name': item.find('a', class_='vacancy-card__title-link').get_text(),
                'Company': item.find('a', class_='link-comp--appearance-dark').get_text(),
                'Info': f"{item.find('div', class_='vacancy-card__skills').get_text()} • {item.find('div', class_='vacancy-card__meta').get_text()}",
                'Link': f"https://career.habr.com{item.find('a', class_='vacancy-card__title-link').get('href')}",
                'Date': item.find('time', class_='basic-date').get_text()
            }
        )
    return vacancy


def save_doc(items, path):
    with open(path, 'w', encoding='UTF-8', newline='') as file:
        write = csv.writer(file, delimiter=';')
        write.writerow(['Name', 'Company', 'Info', 'Link', 'Date'])
        for item in items:
            write.writerow([item['Name'], item['Company'], item['Info'], item['Link'], item['Date']])


def main():
    print('Parser v0.1')
    page = input('Specify the number of pages to parse:')
    page = int(page)
    html = get_html(url)
    if html.status_code == 200:
        vacancy = []
        for page_ in range(1, page + 1):
            print(f'Loading... {page_} : {page}')
            html = get_html(url, params={'page': page_})
            vacancy.extend(get_content(html.text))
            save_doc(vacancy, CSV)
        count = 1
        for i in vacancy:
            print(count, i)
            count += 1
    else:
        print('ERROR')


if __name__ == '__main__':
    main()
