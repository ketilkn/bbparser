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
            if element.name in['p', 'ul']:
                continue
            skill_name = element.text.strip().capitalize()
            skill_description = ''
            for next_element in element.find_next_siblings():
                if next_element.name not in ['p', 'ul']:
                    break
                skill_description = skill_description + '\n' +str(next_element)

            category_name = category.text.strip().title().replace('Skills', '')
            if category_name == 'Traints':
                category_name = 'Trait'
            skill = {'name': skill_name.strip(),
                     'description': skill_description.strip(),
                     'category': category_name.strip()}
            result.append(skill)

    return result
