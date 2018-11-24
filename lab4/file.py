
"""
Прочитать из файла (имя - параметр командной строки)
все слова (разделитель пробел)

Создать "Похожий" словарь который отображает каждое слово из файла
на список всех слов, которые следуют за ним (все варианты).

Список слов может быть в любом порядке и включать повторения.
например "and" ['best", "then", "after", "then", ...] 

Считаем , что пустая строка предшествует всем словам в файле.

С помощью "Похожего" словаря сгенерировать новый текст
похожий на оригинал.
Т.е. напечатать слово - посмотреть какое может быть следующим 
и выбрать случайное.

В качестве теста можно использовать вывод программы как вход.парам. для следующей копии
(для первой вход.парам. - файл)

Файл:
He is not what he should be
He is not what he need to be
But at least he is not what he used to be
  (c) Team Coach


"""
import random


def generate_dictionary(filename):
    file = open(filename, "r")
    words = file.read().split()
    # print(words)
    my_dict = dict()
    for (idx, word) in enumerate(words):
        if idx == len(words) - 1:
            break
        words_after_this = words[idx + 1:]
        if word not in my_dict:
            my_dict[word] = words_after_this
    # print(my_dict)
    return my_dict


def change_phrase(phrase):
    my_dict = generate_dictionary("1.txt")
    words = phrase.split()
    new_phrase = ""
    for word in words:
        new_phrase += word + " "
        if word in my_dict.keys():
            i = random.randint(0, len(my_dict[word]) - 1)
            new_phrase += my_dict[word][i] + " "
    return new_phrase


def main():
    for i in range(0, 10):
        print(change_phrase("Team is used"))


if __name__ == '__main__':
    main()
