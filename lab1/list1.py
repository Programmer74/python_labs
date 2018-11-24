from mytest import test

# 1.
# Вх: список строк, Возвр: кол-во строк
# где строка > 2 символов и первый символ == последнему


def fx1(words):
    count = 0
    for word in words:
        if (len(word) > 2) and (word[0] == word[-1]):
            count += 1
    return count


# 2.
# Вх: список строк, Возвр: список со строками (упорядочено)
# за искл всех строк начинающихся с 'x', которые попадают в начало списка.
# ['tix', 'xyz', 'apple', 'xacadu', 'aabbbccc'] -> ['xacadu', 'xyz', 'aabbbccc', 'apple', 'tix']
def fx2(words):
    return sorted(words, key=lambda word: (word[0] != 'x', word))


# 3.
# Вх: список непустых кортежей,
# Возвр: список сортир по возрастанию последнего элемента в каждом корт.
# [(1, 7), (1, 3), (3, 4, 5), (2, 2)] -> [(2, 2), (1, 3), (3, 4, 5), (1, 7)]

def fx3(tuples):
    return sorted(tuples, key=lambda a: a[-1])


def main():
    print('lab1.1')
    test(fx1(['ds', 'sds', 'ssdds', 'wdewdw', 'hj', 'hh']), 3)

    test(fx2(['tix', 'xyz', 'apple', 'xacadu', 'aabbbccc']), ['xacadu', 'xyz', 'aabbbccc', 'apple', 'tix'])
    test(fx2(['hfj', 'hgfh', 'wqaewq', 'asag', 'xxdsf', 'x', 'sx', 'dgfdg']),
           ['x', 'xxdsf', 'asag', 'dgfdg', 'hfj', 'hgfh', 'sx',
          'wqaewq'])
    test(fx2(['abc', 'rtb', 'cdr', 'iut', 'gxd']), ['abc', 'cdr', 'gxd', 'iut', 'rtb'])

    test(fx3([(1, 7), (1, 3), (3, 4, 5), (2, 2)]), [(2, 2), (1, 3), (3, 4, 5), (1, 7)])


if __name__ == '__main__':
    main()
