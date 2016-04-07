

import re


def read_data(filename):
    pattern = re.compile('\s+')
    result_ls = []
    with open(filename) as handle:
        for line in handle:
            line = re.sub(pattern, '', line)
            result_ls.append(line)
    return result_ls


if __name__ == '__main__':
    data = 'data\\br-phono-test.txt'