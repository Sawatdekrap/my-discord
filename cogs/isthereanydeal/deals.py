from urllib.parse import quote
import requests
import bs4


BASE_URL = "https://isthereanydeal.com"
SEARCH_URL = BASE_URL + "/search/?q="


def get_info_from_search_html(html):
    """Return first search result's info in the following format
    {
        'game_title': '...',
        'thumbnail_link': '...',
        'info_link': '<BASE_URL>/game/<game_title>/info',
        'current_best': {
            'store': '...',
            'value': '$...',
            'discount': '%...'
        },
        'historic_best': {
            'store': '...',
            'value': '$...',
            'discount': '%...'
        }
    }
    """
    info = {}
    soup = bs4.BeautifulSoup(html, 'html.parser')
    if soup.find("div", class_='widget__nodata') is not None:
        return info

    # Get first result with a picture or return
    containers = [c for c in soup.find_all('div', class_='card--list') if c.a.div.get('data-img-sm')]
    if not containers:
        return info

    # Get the parent container and fill the info dict
    container = containers[0]
    for row in container.find_all('div', class_='card__row'):
        # If this row is a title row, store the game title
        title_a = row.find('a', class_='card__title')
        if title_a is not None:
            info['thumbnail_link'] = container.a.div['data-img-sm']  # We know this is present as this is what we filter
            info['game_title'] = title_a.text
            info['info_link'] = BASE_URL + title_a['href']
            continue

        # Row should be a discount listing, get the section name
        section_span = row.find('span', class_='card__rowlabel')
        if section_span is None:
            continue
        section = section_span.text.lower()

        # Fill in value and percent values
        sub_dict = {}
        value_div = row.find('div', class_='numtag__primary')
        if value_div is not None:
            sub_dict['value'] = value_div.text
        percent_div = row.find('div', class_='numtag__second')
        if percent_div is not None:
            sub_dict['percent'] = percent_div.text
        store_span = row.find('span', class_='shopTitle')
        if store_span is not None:
            sub_dict['store'] = store_span.text.replace('&nbsp', '')
        # Insert sub-dict
        if 'current' in section:
            info['current_best'] = sub_dict
        elif 'historic' in section:
            info['historic_best'] = sub_dict
        else:
            pass

    return info


def get_info_from_game_title(game_title):
    """Return deal info about game if possible, otherwise return None

    Adds 'search_url' key to dictionary returned from get_info_from_search_html
    """
    quoted_title = quote(game_title)
    search_url = SEARCH_URL + quoted_title
    r = requests.get(search_url, cookies={'cookieConsent': '1'})
    if r.ok:
        info = get_info_from_search_html(r.content)
        info['search_url'] = search_url
    else:
        info = None
    return info
