import typing

import bs4


def parse_skills(html: str) -> typing.List[typing.Dict]:
    soup = bs4.BeautifulSoup(html, features="html.parser")
    result = []
    first_header = soup.select_one('h2#skills')

    categories = [c for c in first_header.find_all_next('h3')]
    categories.append(soup.select_one('h2#traits'))
    categories.append(soup.select_one('h2#extraordinary'))

    for category in categories:
        for element in category.findNextSiblings():
            if element.name in ['h3', 'h2']:
                break
            if element.name == 'p':
                continue
            skill_name = element.text.strip().capitalize()
            skill_description = str(element.findNext('p'))
            category_name = category.text.strip().title().replace('Skills', '')
            skill = {'name': skill_name, 'description': skill_description, 'category': category_name}
            result.append(skill)

    return result
