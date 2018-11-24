import re
# for regexp magic
from mytest import test

# 1.
# Вх: строка. Если длина > 3, добавить в конец "ing", 
# если в конце нет уже "ing", иначе добавить "ly".


def fx4(word):
    if len(word) > 3:
        if not word.endswith('ing'):
            word = word + 'ing'
        else:
            word = word + 'ly'
    return word


# 2. 
# Вх: строка. Заменить подстроку от 'not' до 'bad'. ('bad' после 'not')
# на 'good'.
# Пример: So 'This music is not so bad!' -> This music is good!

def fx5(word):
    return re.sub(r'not.*bad', 'good', word)

def main():
    print('lab1.2')
    test(fx4('test'), 'testing')
    test(fx4('hi'), 'hi')
    test(fx4('testing'), 'testingly')

    test(fx5('This music is not so bad!'), 'This music is good!')
    test(fx5('This music is bad!'), 'This music is bad!')
    test(fx5('This music is not so good!'), 'This music is not so good!')


if __name__ == '__main__':
    main()
