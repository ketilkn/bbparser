import typing

import bs4


def parse_inducements(html: str) -> typing.List[typing.Dict]:
    soup = bs4.BeautifulSoup(html, features="html.parser")

    inducements = []

    for h3 in soup.find_all("h3"):
        print(h3.text)
        if h3.text.startswith('INDUCEMENTS IN'):
            continue
        count, title = h3.text.strip().split(' ', maxsplit=1)
        inducement_type = 'Other'
        if ':' in title:
            inducement_type, title = title.split(':', maxsplit=1)

        if count == 'UNLIMITED':
            max_count = 0
        else:
            max_count = int(count.split('-')[-1])
        first_paragraph = h3.next_sibling.next_sibling
        available_to = first_paragraph.text[first_paragraph.text.find('AVAILABLE TO'):]

        try:
            price = int(available_to.split(',', maxsplit=1)[0]) * 1000
        except ValueError:
            price = 10000
        special_rules = []
        require_apothecary = False
        if title == 'Star players':
            special_rules.append('Any Team')
        if 'ANY TEAM THAT CAN INCLUDE AN APOTHECARY' in available_to:
            special_rules.append('Any (not undead)')
            require_apothecary = True
        if available_to.endswith('AVAILABLE TO ANY TEAM'):
            special_rules = ['Any Team']
        if available_to.endswith("AVAILABLE TO ANY TEAM WITH THE 'LOW COST LINEMEN' SPECIAL RULE"):
            special_rules = ['Low Cost Linemen']
        if "AVAILABLE TO ANY TEAM WITH THE 'FAVOURED OF NURGLE' SPECIAL RULE" in available_to:
            special_rules = ['Favoured of Nurgle']
        if 'AVAILABLE TO ANY TEAM BELONGING TO TIER 3' in available_to:
            special_rules = ['Tier 3']
        if 'ELVEN KINGDOMS LEAGUE' in available_to:
            special_rules.append('Elven Kingdoms League')
        if 'LUSTRIAN SUPERLEAGUE' in available_to:
            special_rules.append('Lustrian Superleague')
        if 'WORLDS EDGE SUPERLEAGUE' in available_to:
            special_rules.append('Worlds  Edge Superleague')
        if 'OLD WORLD CLASSIC' in available_to:
            special_rules.append('Old World Classic')
        if 'FAVOURED OF...' in available_to:
            special_rules.append('Favoured of Khorne')
            special_rules.append('Favoured of Nurgle')
            special_rules.append('Favoured of Tzeentch')
            special_rules.append('Favoured of Slaanesh')
        if 'UNDERWORLD CHALLENGE' in available_to:
            special_rules.append('Underworld Challenge')
        if 'BADLANDS BRAWL' in available_to:
            special_rules.append('Badlands Brawl')
        if 'SYLVANIAN SPOTLIGHT' in available_to:
            special_rules.append('Sylvanian Spotlight')


        description = ''
        for next_element in first_paragraph.next_siblings:
            if next_element.name == 'h3':
                break
            description += str(next_element)
        inducement = {'title': title.capitalize(),
                      'slug': h3['id'],
                      'inducment_type': inducement_type.capitalize(),
                      'price': price,
                      'max_count': max_count,
                      'description': description,
                      'require_apothecary_access': require_apothecary,
                      'special_rules': special_rules}
        if not special_rules and inducement['title']!='Star players':
            raise ValueError(f'No special rules for {title}')
        yield inducement

    return inducements