def parse_txt():
    data_dict = {}
    with open('data.txt', 'r', encoding='utf-8') as data_file:
        for line in data_file.readlines():
            line_data = line.replace('\n', '').split(':')
            data_dict[line_data[0].strip()] = line_data[1].strip()
    return data_dict


def main():
    data_dict = parse_txt()
    with open('dict.txt', 'w', encoding='utf-8') as dict_file:
        dict_file.write(data_dict.__repr__())


if __name__ == '__main__':
    main()
