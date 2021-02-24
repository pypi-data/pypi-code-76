from django_discord_connector.models import DiscordToken
from django.contrib.auth.models import User 

class PlatformResolutionException(Exception):
    pass 

class EveOnlineResolutionException(Exception):
    pass 

def resolve_username_from_discord_user_id(discord_user_id):
    try:
        user = DiscordToken.objects.get(discord_user=discord_user).user 
    except DiscordToken.DoesNotExist:
        raise PlatformResolutionException(f"Missing Discord Token for {discord_user_id}")
    return user.username 

def resolve_eve_online_identifiers_from_discord_user_id(discord_user_id):
    from django_eveonline_connector.models import PrimaryEveCharacterAssociation
    try:
        user = DiscordToken.objects.get(discord_user=discord_user).user 
        character = PrimaryEveCharacterAssociation.objects.get(user=user).character
        return {
            "character": character.name, 
            "corporation": character.corporation.ticker, 
            "alliance": character.corporation.alliance.ticker
        }
    except PrimaryEveCharacterAssociation.DoesNotExist:
        raise EveOnlineResolutionException(f"Missing Primary Character for {discord_user_id}")


def calculate_nickname_from_discord_user_id(discord_user_id):
    nickname = DiscordClient.get_instance().name_enforcement_schema

    try: 
        username = resolve_username_from_discord_user_id(discord_user_id)
    except PlatformResolutionException:
        return None 

    try: 
        eve_identifiers = resolve_eve_online_identifiers_from_discord_user_id(discord_user_id)
    except EveOnlineResolutionException:
        return None 

    if '%username' in nickname:
        nickname = nickname.replace("%username", user.username)
    if '%character' in nickname:
        nickname = nickname.replace("%character", character.name)
    if '%corporation' in nickname:
        nickname = nickname.replace("%corporation", character.corporation.ticker)
    if '%alliance' in nickname:
        nickname = nickname.replace("%alliance", character.corporation.alliance.ticker)

    return nickname

