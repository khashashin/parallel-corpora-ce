def main():
    with open('data_ce_ru.txt', 'r+', encoding='utf-8') as data_ce_ru:
        with open('data_ru_ce.txt', 'r+', encoding='utf-8') as data_ru_ce:
            ce_ru_data = data_ce_ru.readlines()
            ru_ce_data = data_ru_ce.readlines()

            print('The length of CE - RU before removing duplicates is: ', len(ce_ru_data))
            print('The length of RU - CE before removing duplicates is: ', len(ru_ce_data))

            ce_ru_data = list(set(ce_ru_data))
            ru_ce_data = list(set(ru_ce_data))

            for line in ce_ru_data:
                data_ce_ru.write(line)

            for line in ru_ce_data:
                data_ru_ce.write(line)

            print('The length of CE - RU after removing duplicates is: ', len(ce_ru_data))
            print('The length of RU - CE after removing duplicates is: ', len(ru_ce_data))


if __name__ == '__main__':
    main()
