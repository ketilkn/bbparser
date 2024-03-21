import logging
import typing

import bs4


LOG = logging.getLogger('main')


class BBParseError(Exception):
    pass


def parse_player_card(soup):
    name = soup.text.strip()
    player_table = soup.findNext('table')

    first_column = len(player_table.select('td')) - 5
    player_price = player_table.select('th')[0].text.replace('K', '').strip() if first_column == 1 else None
    player_mv = player_table.select('td')[first_column].text.strip()
    player_st = player_table.select('td')[first_column + 1].text.strip()
    player_ag = player_table.select('td')[first_column + 2].text.strip()
    player_pa = player_table.select('td')[first_column + 3].text.strip()
    player_av = player_table.select('td')[first_column + 4].text.strip()
    player_skill_list = soup.findNext('ul')
    player_skills = [el.text.strip() for el in player_skill_list.select('li')]
    player_special_skill = player_skills[-1]
    player_special_skill_description = player_skill_list.findNext('p').text.strip()
    player_card = {'name': name,
                   'price': player_price,
                   'mv': player_mv,
                   'st': player_st,
                   'ag': player_ag,
                   'pa': player_pa,
                   'av': player_av,
                   'skills': player_skills,
                   'special_skill': player_special_skill,
                   'special_skill_description': player_special_skill_description}
    return player_card


def parse_players(soup):
    tables = soup.select('table')
    if len(tables) == 1:
        LOG.debug('Found 1 table for player card')
        price = tables[0].select('th')[0].text.strip()
        return price, [parse_player_card(soup.select_one('h1'))]
    elif len(tables) == 2:
        LOG.debug('Found 2 tables for player card')
        player_headings = soup.select('h4')
        price = soup.select('.md-content__inner > p:nth-child(3)')[0].text.strip()
        if len(player_headings) == 1:
            player_headings.append(player_headings[0].findNext('h5'))
        return price, [parse_player_card(player_soup) for player_soup in player_headings]
    raise BBParseError('Did not recognize any players in soup')


def parse_starplayer(html: str) -> typing.Dict:
    soup = bs4.BeautifulSoup(html, features="html.parser")
    heading = soup.select('h1')
    title = heading[0].text.strip()
    slug = heading[0]['id']
    if 1 < len(soup.select('table')) > 2:
        raise BBParseError(
            f'Assumption of 1 or 2 table tag(s) (for the player card(s)) is not holding up. Got {len(soup.select("table"))}')
    price, player_cards = parse_players(soup)

    special_rules = ['Any Team']
    if not soup.select('#special-rules'):
        if title == "Morg'n Thorg":
            special_rules = ['Any (not Undead)']
        else:
            LOG.warning('No special rules for %s', title)
            raise BBParseError(f'No special rules for {title}')
    else:
        special_rules = [el.text.strip() for el in soup.select('#special-rules')[0].findNext('ul').select('li a')]
    plays_for_any_team = True if len(special_rules) == 16 else False

    return {'title': title,
            'slug': slug,
            'price': price,
            'player_cards': player_cards,
            'plays_for_any_team': plays_for_any_team,
            'special_rules': special_rules,
            'special_skill': player_cards[-1]['special_skill'],
            'special_skill_description': player_cards[-1]['special_skill_description']}