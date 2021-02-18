# This file is designed to contain variables, lists, etc. to be used by
# the code to make the really important files less cumbersome and
# coupled
import re

#############################
#     INCLUDE FILTERS       #
#############################

tweet_inc = [

    # Single fields
    r'^created_at$',
    r'^id$',
    r'^text$',
    r'^source$',
    r'^truncated$',
    r'^in_reply_to_status_id$',
    r'^in_reply_to_user_id$',
    r'^in_reply_to_screen_name$',
    r'^quoted_status_id$',
    r'^is_quote_status$',
    r'^quote_count$',
    r'^reply_count$',
    r'^retweet_count$',
    r'^favorite_count$',

    # User object
    r'^user\.id$',
    r'^user\.name$',
    r'^user\.scren_name$',
    r'^user\.location$',
    r'^user\.verified$',
    r'^user\.followers_count$',
    r'^user\.friends_count$',
    r'^user\.listed_count$',
    r'^user\.favourites_count$',
    r'^user\.statuses_count$',
    r'^user\.created_at$',
    r'^user\.geo_enabled$',
    r'^user\.lang$',

    # Entities object
    r'^entities\.hashtags\[\d+\]\.text$',
    r'^entities\.urls\[\d+\]\.expanded_url$',
    r'^entities\.user_mentions\[\d+\]\.screen_name$',
    r'^entities\.media\[\d+\]\.media_url$',

    # Place object
    r'^place\.country$',
    r'^place\.country_code$',
    r'^place\.full_name$',
    r'^place\.id$',
    r'^place\.name$',
    r'^place\.place_type$',
    r'^place\.url$',
    r'^place\.bounding_box\.type$',
    r'^place\.bounding_box\.coordinates',

    # Coordinates object
    r'^coordinates\.type',
    r'^coordinates\.coordinates',
    ]


#############################
#     EXCLUDE FILTERS       #
#############################

old_exc = [
    r'entities\.url\.urls\[\d*\]\.(?!expanded_url)',
    r'entities\.urls\[\d*\]\.(?!expanded_url)',
    r'entities\.user_mentions\[\d*\]\.(?!id)',
    r'entities\.user_mentions\[\d*\]\.(?!screen_name)',
    r'entities\.symbols',
    r'entities\.polls',
    r'entities\.media\[\d*\]\.(?!id)',
    r'entities\.media\[\d*\]\.(?!media_url)',
    r'entities\.media\[\d*\]\.(?!type)',
    r'user\..*profile.*',
    ]


def load_include_filter():
    temporary_filter = []
    for item in tweet_inc:
        temporary_filter.append(re.compile(item))

    return temporary_filter
