import datetime
import os
import requests
from bs4 import BeautifulSoup

filepath = os.path.join(os.getcwd())

def logger(_filepath):
    def habr(func):
        def replaced_func(*args, **kwargs):
            func_name = func.__name__
            func_time = datetime.datetime.now()
            func_args = args
            func_kwargs = kwargs
            func_result = func(*args, **kwargs)
            data = f'Результат работы декоратора: \n' \
                   f'Имя функции:    {func_name}  \n' \
                   f'Время запуска функции:    {func_time} \n' \
                   f'Аргументы функции:    {func_args}    {func_kwargs} \n' \
                   f'Результат работы функции:    {func_result}'

            with open(f'{_filepath}\\result.txt', 'w') as f:
                f.write(data)
            f.close()
            return data
        return replaced_func
    return habr

@logger(filepath)
def habrparser():
    response = requests.get('https://habr.com/ru/all')
    KEYWORDS = {'IT-инфраструктура', 'Блог компании АйПиМатика', 'PHP *', 'Python *', 'Стандарты связи'}
    href = []

    if not response.ok:
        raise ValueError('No response')
    else:
        text = response.text
        soup = BeautifulSoup(text, features="html.parser")
        articles = soup.find_all('article')
        for article in articles:
            hubs = {h.text for h in article.find_all('a', class_='tm-article-snippet__hubs-item-link')}
            if KEYWORDS & hubs:
                href.append(article.find('a', class_="tm-article-snippet__title-link").attrs.get('href'))
    return href

if __name__ == '__main__':
    result = habrparser()
    print(result)
