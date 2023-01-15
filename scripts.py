import json


def main():
    with open('data/bible.json', 'r+', encoding='utf-8') as ce:
        with open('rubib/bible.json', 'r+', encoding='utf-8') as ru:
            with open('data_ce_ru.txt', 'w+', encoding='utf-8') as data_ce_ru:
                with open('data_ru_ce.txt', 'w+', encoding='utf-8') as data_ru_ce:
                    ce_data = json.load(ce)
                    ru_data = json.load(ru)

                    amount = len(ce_data.keys())

                    for key in ce_data.keys():
                        data_ce_ru.write(f'{ce_data[key]}\t{ru_data[key]}\n')
                        data_ru_ce.write(f'{ru_data[key]}\t{ce_data[key]}\n')

                        print(f'Amount of verses: {amount}')
                        amount -= 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
