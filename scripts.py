import json
import re


def main():
    with open('data/bible.json', 'r+', encoding='utf-8') as ce:
        with open('rubib/bible.json', 'r+', encoding='utf-8') as ru:
            with open('data_ce_ru.txt', 'w+', encoding='utf-8') as data_ce_ru:
                with open('data_ru_ce.txt', 'w+', encoding='utf-8') as data_ru_ce:
                    ce_data = json.load(ce)
                    ru_data = json.load(ru)

                    amount = len(ce_data.keys())

                    for key in ce_data.keys():
                        lower_ce_sentence = ce_data[key].lower()
                        lower_ru_sentence = ru_data[key].lower()

                        lower_ce_sentence = lower_ce_sentence.replace('[', '')
                        lower_ce_sentence = lower_ce_sentence.replace(']', '')
                        lower_ru_sentence = lower_ru_sentence.replace('[', '')
                        lower_ru_sentence = lower_ru_sentence.replace(']', '')

                        lower_ce_sentence = lower_ce_sentence.replace('і', 'ӏ')

                        # replace using regex \s\([\d]+\) with ''
                        lower_ce_sentence = re.sub(r'\s\([\d]+\)', '', lower_ce_sentence)
                        lower_ru_sentence = re.sub(r'\s\([\d]+\)', '', lower_ru_sentence)

                        data_ce_ru.write(f'{lower_ce_sentence}\t{lower_ru_sentence}\n')
                        data_ru_ce.write(f'{lower_ru_sentence}\t{lower_ce_sentence}\n')

                        print(f'Amount of verses: {amount}')
                        amount -= 1


if __name__ == '__main__':
    main()
