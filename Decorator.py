import datetime
import os
import requests
from bs4 import BeautifulSoup

filepath = os.path.join(os.getcwd())

def logger(_filepath):

    def habr(function):
        nonlocal _filepath

        func_name = None
        func_time = None
        func_args = None
        func_kwargs = None
        func_result = None

        def replaced_func(*args, **kwargs):
            nonlocal func_name
            nonlocal func_time
            nonlocal func_args
            nonlocal func_result
            nonlocal func_kwargs
            func_name = function.__name__
            func_time = datetime.datetime.now()
            func_args = args
            func_kwargs = kwargs
            func_result = function(*args, **kwargs)

            return f'Результат работы декоратора: \n' \
                   f'Имя функции:    {func_name}  \n' \
                   f'Время запуска функции:    {func_time} \n' \
                   f'Аргументы функции:    {func_args}    {func_kwargs} \n' \
                   f'Результат работы функции:    {func_result}'

        with open(f'{_filepath}\\result.txt', 'w') as f:
            date = replaced_func()
            f.write(date)
        f.close()

        return replaced_func

    return habr

@logger(filepath)
def habrParser():
    response = requests.get('https://habr.com/ru/all/')
    KEYWORDS = {'дизайн', 'фото', 'Программирование', 'python', 'Сетевое оборудование'}
    href = 'Ссылка по умолчанию: https://habr.com/ru/all/'

    if not response.ok:
        raise ValueError('No response')

        text = response.text
        soup = BeautifulSoup(text, features="html.parser")
        articles = soup.find_all('article')
        for article in articles:
            hubs = {h.text for h in article.find_all('a', class_='tm-article-snippet__hubs-item-link')}
            if KEYWORDS & hubs:
                time_post = article.find(class_="tm-article-snippet__datetime-published").time.get('title')[:10]
                header = article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").text
                href = article.find('a', class_="tm-article-snippet__title-link").attrs.get('href')
    return href

if __name__ == '__main__':
    habrParser()