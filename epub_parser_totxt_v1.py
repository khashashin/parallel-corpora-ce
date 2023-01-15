import json
from ebooklib import epub
from bs4 import BeautifulSoup

book = epub.read_epub('Vsya-Bibliya-chechenskiy.epub')


def write_to_json(obj, filename):
    with open(f'data/{filename}', 'r+', encoding='utf-8') as f:
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
    paragraph = paragraph.replace('qac*', '')
    paragraph = paragraph.replace('qac ', '')
    if paragraph[0] == ' ':
        paragraph = paragraph[1:]
    if paragraph[-1] == ' ':
        paragraph = paragraph[:-1]

    return paragraph


PREVIOUS_SECTION = ''
SECTION_COUNTER = 0
def get_section_number(title):
    global PREVIOUS_SECTION
    global SECTION_COUNTER
    if title is None:
        return SECTION_COUNTER
    if title == PREVIOUS_SECTION:
        return SECTION_COUNTER
    else:
        SECTION_COUNTER += 1
        PREVIOUS_SECTION = title
        return SECTION_COUNTER


def parse_content(content):
    # Parse content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    chapters = soup.prettify().split('<h3')
    data = []
    for chapter in chapters:
        if '</h3>' not in chapter:
            continue
        chapter = f"<h3{chapter}"
        chapter = BeautifulSoup(chapter, 'html.parser')
        header = f"{remove_unused_parts(chapter.find('h3').find('strong').text)}",
        section = remove_unused_parts(soup.find('h2').text) if soup.find('h2') else None
        section = get_section_number(section)
        data.append({
            'section': section,
            'header': header[0],
            'chapters': [
                remove_unused_parts(sup.next_sibling) for sup in chapter.find_all('sup')
            ],
        })
    return data


def is_item_valid(item):
    if not isinstance(item, epub.EpubHtml):
        return False

    content = item.content.decode('utf-8')
    if '<sup' not in content:
        return False

    return True


def main():
    current_section = None
    section_count = 0
    data = {}
    for item in book.items:
        if is_item_valid(item):
            content = parse_content(item.content.decode('utf-8'))
            for cont in content:
                if cont['section'] is None:
                    pass
                if current_section != cont['section']:
                    current_section = cont['section']
                    section_count += 1
                if len(cont['chapters']) > 1:
                    for index, chapter in enumerate(cont['chapters']):
                        key = f"{section_count}-{cont['header']}-{index}"
                        data[key] = chapter

    write_to_json(data, 'bible.json')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
