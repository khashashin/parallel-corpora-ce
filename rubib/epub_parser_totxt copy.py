import json
from ebooklib import epub
from bs4 import BeautifulSoup

import time

book = epub.read_epub('rubib/Bible_RST.epub')


def write_to_json(obj, filename):
    if "13-26-0" in obj.keys():
        print("13-26-0")
    if "13-25-0" in obj.keys():
        print("13-25-0")

    with open(f'rubib/{filename}', 'r+', encoding='utf-8') as f:
        data = {}
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            json.dump({}, f)

        data.update(obj)

        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)


def remove_unused_parts(paragraph):
    paragraph = paragraph.replace('\n', '')
    paragraph = paragraph.replace('     ', '')
    paragraph = paragraph.replace('    ', '')
    paragraph = paragraph.replace('   ', '')
    paragraph = paragraph.replace('  ', '')
    paragraph = paragraph.replace('\xa0', '')
    if paragraph[0] == ' ':
        paragraph = paragraph[1:]
    if paragraph[-1] == ' ':
        paragraph = paragraph[:-1]

    return paragraph


def get_section_number(title):
    number_part = title.split(' ')[1]
    numbers = number_part.split('.')
    if numbers[0] == '0' and len(numbers) == 2:
        return int(numbers[0]) + 1
    if numbers[0] == '0' and len(numbers) == 3:
        return int(numbers[1]) + 1
    if numbers[0] != '0' and len(numbers) != 3 and int(numbers[0]) < 46:
        section_number = int(numbers[0])
        if section_number >= 15 and section_number < 23:
            section_number -= 3
        if section_number >= 23 and section_number < 28:
            section_number -= 5
        if section_number >= 28 and section_number < 33:
            section_number -= 7
        if section_number >= 33 and section_number < 41:
            section_number -= 8
        if section_number >= 41 and section_number < 46:
            section_number -= 8
        if section_number >= 46 and section_number < 47:
            section_number -= 12

        return 5 + section_number
    if int(numbers[0]) == 46 and len(numbers) == 3:
        section_number = 39 + int(numbers[1])
        return section_number

    if int(numbers[0]) == 47 and len(numbers) == 2:
        return 43
    if int(numbers[0]) == 48 and len(numbers) == 2:
        return 44
    if int(numbers[0]) == 48 and len(numbers) == 3 and int(numbers[1]) <= 3:
        return 44 + int(numbers[1])
    if int(numbers[0]) == 49 and len(numbers) == 2:
        return 48
    if int(numbers[0]) == 49 and len(numbers) == 3 and int(numbers[1]) <= 11:
        return 48 + int(numbers[1])
    if int(numbers[0]) == 49 and len(numbers) == 3 and int(numbers[1]) >= 13:
        return 47 + int(numbers[1])
    if int(numbers[0]) == 50 and len(numbers) == 2:
        return 61

def parse_content(content):
    # Parse content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    title = remove_unused_parts(soup.find('title').text)
    section = get_section_number(title)
    h1 = remove_unused_parts(soup.find('div', {'class': 'title2'}).text)
    header = h1.split(' ')[1]
    paragraphs = [remove_unused_parts(p.next_sibling) for p in soup.find_all('i') if p.text.isnumeric()]
    data = {
        'section': section,
        'header': header,
        'chapters': paragraphs,
    }
    return data


def is_item_valid(item):
    if not isinstance(item, epub.EpubHtml):
        return False

    content = item.content.decode('utf-8')
    validators = ['Псалом', 'Глава']
    if not any(validator in content for validator in validators):
        return False

    return True


def main():
    data = {}
    for item in book.items:
        if is_item_valid(item):
            content = parse_content(item.content.decode('utf-8'))
            for index, chapter in enumerate(content['chapters']):
                key = f"{content['section']}-{content['header']}-{index}"
                data[key] = chapter

            # time.sleep(1)
    write_to_json(data, 'bible.json')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
