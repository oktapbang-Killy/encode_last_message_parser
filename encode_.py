
import json
import requests
from bs4 import BeautifulSoup

# Кусок кода который делает проверку последних доступных сообщений
# т.е так мы проверяем появились ли новые сообщения и ссылки
base_url = 'https://encode.su/threads/?p={}&pp=1'
start_page = 81630 # начиная с жтой страницы
current_page = start_page

while True:
    url = base_url.format(current_page)
    response = requests.get(url)
    # идея была в том что-бы перебирать до тех пор пока на встретим класс ошибки от Администратора
    # а именно <div class="standard_error">
    soup = BeautifulSoup(response.text, 'html.parser')
    error_message = soup.find('div', class_='standard_error')

    if error_message:
        print(f"Последняя доступная страница: {current_page - 1}")
        break

    current_page += 1
# Кусок кода отвечающий за парсинг сообщений в JSON файл
start_page = 81630 # с какой страницы
end_page = 81638 # по какую парсить сообщения

base_url = 'https://encode.su/threads/?p={}&pp=1'#специальная ссылка через которую я могу поллить следующий номер поста
current_page = start_page
messages = []
while current_page <= end_page:
    url = base_url.format(current_page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content_divs = soup.find_all('div', class_='content')

    for content_div in content_divs:
        message_blockquote = content_div.find('blockquote', class_='postcontent restore')
        if message_blockquote:
            message_text = message_blockquote.get_text(strip=True)
            messages.append({"message": message_text})#class="message"
    current_page += 1  # инкрементирование, переход к следующей странице
with open('last_messages.json', 'w', encoding='utf-8') as json_file: # записываю всё JSON файл
    json.dump(messages, json_file, ensure_ascii=False, indent=2)
with open('last_page.txt', 'w', encoding='utf-8') as page_file: #запомнить последнюю страницу
    page_file.write(str(current_page - 1))
print("Done: Все сообщения записаны в файл last_messages.json")
