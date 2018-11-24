import random
from flask import Flask
from flask import render_template
from random import shuffle
from imgrequest import build_links_for_name

"""
Вход: файл guess.txt содержащий имена для угадывания 

(например из http://www.biographyonline.net/people/famous-100.html можно взять имена)


Написать игру "Угадай по фото"

3 уровня сложности:
1) используются имена только 1-10
2) имена 1-50
3) имена 1-100

- из используемых имен случайно выбрать одно
- запустить поиск картинок в Google по выбранному
- получить ~30-50 первых ссылок на найденные по имени изображения
- выбрать случайно картинку и показать ее пользователю для угадывания
  (можно выбрать из выпадающего списка вариантов имен)
- после выбора сказать Правильно или Нет

п.с. сделать серверную часть, т.е. клиент играет в обычном браузере обращаясь к веб-серверу.

п.с. для поиска картинок желательно эмулировать обычный пользовательский запрос к Google
или можно использовать и Google image search API
https://ajax.googleapis.com/ajax/services/search/images? или др. варианты
НО в случае API нужно предусмотреть существующие ограничения по кол-ву запросов
т.е. кешировать информацию на случай исчерпания кол-ва разрешенных (бесплатных)
запросов или другим образом обходить ограничение. Т.е. игра не должна прерываться после N запросов (ограничение API)


п.с. желательно "сбалансировать" параметры поиска (например искать только лица, 
использовать только первые 1-30 найденных и т.п.)
для минимизации того что найденная картинка не соответствует имени


"""


def get_names(filename):
    f = open(filename, 'r')
    data = f.read()
    return list(map(lambda x: x.split('(')[0].strip(), data.splitlines()))


names = get_names("names.txt")
picture_urls = dict()

def get_urls(name):
    if name not in picture_urls.keys():
        print("Building img cache for " + name)
        picture_urls[name] = build_links_for_name(name)
    return picture_urls[name]

def get_random_name(lower_bound):
    idx = random.randint(0, lower_bound)
    entry = names[idx]
    return entry


app = Flask(__name__, static_url_path='/static')


@app.route('/randomname')
def randomname():
    return get_random_name(99)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/game/<up_to>")
def game(up_to="9"):
    up_to = int(up_to)
    idx_to_guess = random.randint(0, up_to)
    name_options = names[:up_to]
    shuffle(name_options)
    image_links = get_urls(names[idx_to_guess])[:5]
    shuffle(image_links)
    return render_template('game.html',
                           difficulty=str(up_to + 1) + "%",
                           names=name_options,
                           name_index=idx_to_guess,
                           image_links=image_links)

@app.route("/guess/<id>/<name>")
def guess(id="-1", name=""):
    id = int(id)
    if id == -1:
        return "Bad rq"
    print("Someone is guessing that " + str(id) + " is " + name + "")
    if names[id] == name:
        print("This is true")
        return "True"
    print("Actually, " + name + " is " + str(names.index(name)))
    print("And, " + str(id) + " is " + names[id])
    return "False"

if __name__ == '__main__':
    app.run(debug=True)
