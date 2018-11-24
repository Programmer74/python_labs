import sys
import re


def extr_name(filename):
    """
    Вход: nameYYYY.html, Выход: список начинается с года, продолжается имя-ранг в алфавитном порядке.
    '2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' и т.д.
    """

    ans = []

    f = open(filename, 'r')
    data = f.read()

    yearg = re.search(r'Popularity in (([0-9]){4})', data)
    if not yearg:
        print('None for file' + filename)
        return ans

    year = yearg.group(1)

    print('Parsing year ' + year)

    ans.append(str(year))

    male_name_to_rank_map = dict()
    female_name_to_rank_map = dict()
    name_to_rank_map = dict()

    results = re.findall(r'<td>[0-9]+</td><td>[A-Z][a-z]+</td><td>[A-Z][a-z]+</td>', data, re.MULTILINE)
    for result in results:
        nameg = re.search(r'<td>([0-9]+)</td><td>([A-Z][a-z]+)</td><td>([A-Z][a-z]+)</td>$', result)
        if nameg:
            rank = nameg.group(1)
            malename = nameg.group(2)
            femalename = nameg.group(3)
            male_name_to_rank_map[malename] = int(rank)
            female_name_to_rank_map[femalename] = int(rank)
            name_to_rank_map[malename] = int(rank)
            name_to_rank_map[femalename] = int(rank)

    male_rank_to_name_map = {v: k for k, v in male_name_to_rank_map.items()}
    female_rank_to_name_map = {v: k for k, v in female_name_to_rank_map.items()}

    print('Top ten male names:')
    for i in range(1, 10):
        print(male_rank_to_name_map[i])

    print('Top ten female names:')
    for i in range(1, 10):
        print(female_rank_to_name_map[i])

    sortednames = sorted(name_to_rank_map.keys())
    for name in sortednames:
        ans.append(name + " " + str(name_to_rank_map[name]))

    return ans

def main():
    args = sys.argv[1:]
    if not args:
        print('usage: [--file] file [file ...]')
        sys.exit(1)
    for filename in args:
        print(extr_name(filename))


# для каждого переданного аргументом имени файла, вывести имена  extr_name
# напечатать ТОП-10 муж и жен имен из всех переданных файлов


if __name__ == '__main__':
    main()
