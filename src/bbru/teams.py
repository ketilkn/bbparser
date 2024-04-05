import typing

import bs4


def parse_team(html: str) -> typing.Dict[str, typing.Any]:
    def find_staff(heading: bs4.Tag):
        heading.findNext('ul').select('li')
        staff_li = heading.findNext('ul').select('li')
        result = {}
        for staff in staff_li:
            name = staff.text.rsplit('-', 1)[0].strip().lower()
            price = staff.text.rsplit('-', 1)[-1].replace('K', '').strip()
            result[name] = price
        return result

    soup = bs4.BeautifulSoup(html, features="html.parser")
    heading = soup.select('h1')
    team_name = heading[0].text.strip()
    if team_name == 'Norses':
        team_name = 'Norse'

    team_tier = None
    tier_paragraph = heading[0].findNext('p')
    if tier_paragraph and tier_paragraph.text.lower().strip().startswith('tier'):
        team_tier = int(tier_paragraph.text.lower().replace('tier', '').strip())

    positional_heading = soup.select_one('h3#positionals')
    positional_table = positional_heading.findNext('table')
    team_positionals = parse_positionals(positional_table)
    max_big_guy_count = 0

    next_paragraph = positional_heading.findNext('p')
    if next_paragraph:
        if 'may include up to three big guys' in next_paragraph.text.lower():
            max_big_guy_count = 3
        elif 'may include up to two big guys' in next_paragraph.text.lower():
            max_big_guy_count = 2
        elif 'may include a single big guy' in next_paragraph.text.lower():
            max_big_guy_count = 1

    staff_heading = soup.select_one('h3#staff')
    staff_list = find_staff(staff_heading)

    rerolls = staff_list.get('re-roll', 'not found')
    apothecary = staff_list.get('apothecary', None)

    special_rules_heading = soup.select_one('h3#special-rules')
    special_rules_paragraph = special_rules_heading.findNext() if special_rules_heading.findNext().name == 'p' else None
    choose_favour = False
    if special_rules_paragraph:
        choose_favour = special_rules_paragraph.text.lower().strip().startswith('choose either:')

    favored_of_choice = [r.text for r in special_rules_heading.findNext('ul').select('li') if
                         r.text.startswith('Favoured of')]
    special_rules = [r.text for r in special_rules_heading.findNext('ul').select('li')]
    if choose_favour:
        special_rules = list(filter(lambda r: r not in favored_of_choice, special_rules))

    the_team = {'name': team_name,
                'tier': team_tier,
                'positionals': team_positionals,
                'max_big_guy_count': max_big_guy_count,
                'reroll': rerolls,
                'special_rules': special_rules,
                'favored_of_choice': favored_of_choice,
                'choose_favour': choose_favour,
                'staff': {
                    'cheerleader': '10',
                    'assistant_coach': '10',
                    'apothecary': apothecary}
                }
    return the_team


def parse_positionals(positional_table):
    team_positionals = []
    for positional_row in positional_table.select('tbody tr'):
        columns = positional_row.select('td')
        primary_skills = [s for s in columns[8].text.split() if s]
        secondary_skills = [s for s in columns[9].text.split() if s]
        the_position = columns[1].text
        big_guy = True if '*' in the_position else False
        the_position = the_position.replace('*', '').strip()
        columns = positional_row.select('td')
        team_positionals.append({
            'position': the_position,
            'max_count': int(columns[0].text.split('-')[-1]),
            'big_guy': big_guy,
            'ma': columns[2].text,
            'st': columns[3].text,
            'ag': columns[4].text,
            'skills': [s.strip() for s in columns[7].text.split('•') if s],
            'skill_access': {'primary': primary_skills,
                             'secondary': secondary_skills},
            'price': columns[10].text.replace('K', '').strip()})
    return team_positionals
