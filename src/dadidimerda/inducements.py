import typing

import bs4

def parse_inducements(txt: str) -> typing.List[typing.Dict[str, typing.Any]]:
    soup = bs4.BeautifulSoup(txt, features="html.parser")

    for row in soup.select('#bb16TableInducements tbody tr'):
        inducement_name = row.select_one('th').text.capitalize()
        inducement_type = row.findChild(attrs={'data-title': 'Type'}).text
        inducement_quantity = row.findChild(attrs={'data-title': 'Qty'}).text
        inducement_edition = row.findChild(attrs={'data-title': 'Edition'}).text
        inducement_team = row.findChild(attrs={'data-title': 'Team'}).text
        inducement_cost = row.findChild(attrs={'data-title': 'Cost'}).get_text()
        inducement_description = row.findChild(attrs={'data-title': 'Description'}).text

        teams = map(str.strip, inducement_team.split(','))
        print(inducement_name, teams)
        inducement_price = None
        try:
            inducement_price = int(inducement_cost.split('\n')[0].replace(',', ''))
        except ValueError:
            pass

        yield {'title': inducement_name,
               'type': inducement_type,
               'quantity': inducement_quantity,
               'edition': inducement_edition,
               'team':  inducement_team,
               'cost': inducement_cost,
               'description': inducement_description,
               'price': inducement_price }