import json


def main():
    with open('data/bible.json', 'r+', encoding='utf-8') as ce:
        with open('rubib/bible.json', 'r+', encoding='utf-8') as ru:
            ce_data = json.load(ce)
            ru_data = json.load(ru)

            for key in ce_data.keys():
                if key not in ru_data.keys():
                    print(key)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
