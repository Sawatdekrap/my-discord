import datetime

import discord

from .deals import BASE_URL, SEARCH_URL


AUTHOR_NAME = "IsThereAnyDeal"
THUMBNAIL_URL = "https://pbs.twimg.com/profile_images/1169691692892655619/TbXBDxfj_400x400.jpg"
COLOR = 2123412


def add_deal_field(embed_dict, info_dict, field_key, heading):
    """Helper function to add a field to an embed object best on a field in the info_dict"""
    if field_key in info_dict:
        field_dict = info_dict[field_key]
        field = {
            'name': heading,
            'value': "{value} ({percent} off) on {store}".format(
                value=field_dict.get('value', '??'),
                percent=field_dict.get('percent', '0%'),  # TODO don't default to 0% off
                store=field_dict.get('store', '_unknown_')
            ),
        }
        embed_dict['fields'].append(field)


def get_info_embed(info_dict, searched_title):
    """Build an Embed object with the deal information provided"""

    if info_dict is None:
        info_dict = {}

    base_dict = {
        'title': info_dict.get('game_title', '_Unknown Title_'),
        'type': 'rich',
        'description': "Not what you wanted? [Click here]({}) to try a full search".format(BASE_URL),
        'url': info_dict.get('info_link', BASE_URL),
        # 'timestamp': '',
        'color': COLOR,
        'footer': {
            'text': "Deal info from isthereanydeal.com"
        },
        # 'image': {'url': '', 'height': '', 'width': ''},
        'thumbnail': {
            'url': info_dict.get('thumbnail_link', THUMBNAIL_URL),
        },
        'author': {
            'name': 'IsThereAnyDeal',
            'url': BASE_URL,
            'icon_url': THUMBNAIL_URL,
        },
        'fields': [],
    }

    # Change description if the search was successful
    if 'search_url' in info_dict:
        base_dict['description'] = (
            'Not what you wanted? [Click here]({}) to see the full search.'
            .format(info_dict['search_url'])
        )

    # Add fields for current/historic best if they exist
    add_deal_field(base_dict, info_dict, 'current_best', 'Current Best')
    add_deal_field(base_dict, info_dict, 'historic_best', 'Historic Best')

    return discord.Embed.from_dict(base_dict)
