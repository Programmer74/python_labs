from mytest import test


# 1.
# Вх: список чисел, Возвр: список чисел, где 
# повторяющиеся числа урезаны до одного 
# пример [0, 2, 2, 3] returns [0, 2, 3].
def rm_adj(nums):
    ans = []
    for num in nums:
        if num not in ans:
            ans.append(num)
    return ans


# 2. Вх: Два списка упорядоченных по возрастанию, Возвр: новый отсортированный объединенный список 
def build_two(lista, listb):
    ans = []
    i = 0
    j = 0
    while i < len(lista) and j < len(listb):
        if lista[i] < listb[j]:
            ans.append(lista[i])
            i += 1
        else:
            ans.append(listb[j])
            j += 1
    ans += lista[i:]
    ans += listb[j:]
    return ans


def main():
    print('lab2.2')
    test(rm_adj([0, 2, 2, 3]), [0, 2, 3])
    test(rm_adj([1, 3, 3, 7, 4]), [1, 3, 7, 4])
    test(build_two([1, 3, 3, 4, 7], [2, 3, 5]), [1, 2, 3, 3, 3, 4, 5, 7])


if __name__ == '__main__':
    main()
