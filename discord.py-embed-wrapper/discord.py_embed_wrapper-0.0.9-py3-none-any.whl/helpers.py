import datetime
from typing import List, Union, Optional

from discord import Embed, Message, Reaction, User, Member, Role, DMChannel

from embed_wrapper.wrapper import EmbedField, EmbedWrapper


def embeds_from_message(message: Message) -> Optional[List[Embed]]:
    """
    Creates a :class:`List` of Embeds from a given :class:`Message`.

    :param message: The Message whose Embeds should be recreated
    :return: None if the given Message didn't have any Embeds. A List of recreated Embeds if any were present.
    """
    if len(message.embeds) < 1:
        return None

    return_list = []
    for embed in message.embeds:
        author_name = embed.author.name
        author_url = embed.author.url
        author_icon_url = embed.author.icon_url

        embed_type = embed.type
        title = embed.title
        url = embed.url
        color = embed.color
        description = embed.description
        timestamp = embed.timestamp

        fields = embed.fields

        footer_text = embed.footer.text
        footer_icon_url = embed.footer.icon_url

        image_url = embed.image.url
        thumbnail_url = embed.thumbnail.url

        values = [
            author_name, author_url, author_icon_url,
            embed_type, title, url, color, description, timestamp,
            fields,
            footer_text, footer_icon_url,
            image_url, thumbnail_url
        ]
        for value in values:
            if value == Embed.Empty:
                value = None

        wrapped_fields = []
        if fields:
            for field in fields:
                embed_field = EmbedField(
                    name=field.name if field.name is not Embed.Empty else None,
                    value=field.value if field.value is not Embed.Empty else None,
                    inline=field.inline if field.inline else False,
                )
                wrapped_fields.append(embed_field)

        return_list.append(EmbedWrapper(
            author_name=author_name, author_url=author_url, author_icon_url=author_icon_url,
            embed_type=embed_type, title=title, url=url, color=color, description=description,
            timestamp=timestamp if timestamp else datetime.datetime.now(),
            footer_text=footer_text, footer_icon_url=footer_icon_url,
            image_url=image_url, thumbnail_url=thumbnail_url,
            fields=wrapped_fields if fields else None
        ).embed)

    return return_list


async def send_embed_message(
        embed: Embed,
        invoking_message: Message,
        as_reply: bool = False,
        as_dm: bool = False,
        dm_channel: DMChannel = None,
        pin: bool = False,
        message_content: str = "",
        reactions: List[str] = None,
        mentions: List[Union[User, Member, Role]] = None,
        append_mentions: bool = False
) -> Message:
    """
    Helper Function for sending an :class:`Embed` :class:`Message`

    :param embed: The Embed to append to the Message. Required
    :param invoking_message: The message that the bot is replying to. Required
    :param as_reply: Flag to denote if the sent Embed Message should be sent as a reply. as_replay and as_dm are mutually exclusive. Default is False
    :param as_dm: Flag to denote if the sent Embed Message should be sent as a DM. as_replay and as_dm are mutually exclusive. Default is False
    :param dm_channel: The DMChannel to send the Message to. Only used if as_dm is True. Default is None
    :param pin: Flag to denote if the sent Embed Message should be pinned or not. Default is False
    :param message_content: Contents of the Message send in addition to the Embed. Default is an empty String
    :param reactions: List of Emoji Strings to be added as Reactions to the sent Embed Message. Default is None
    :param mentions: List of Users, Members or Roles to mention in the Message send in addition to the Embed. Default is None
    :param append_mentions: Flag to denote if the defined mentions should be appended or prepended to the Message. Default is to prepend (False).
    :return: The sent Message
    """
    if mentions:
        mentions_list = []
        for user in mentions:
            mentions_list.append(user.mention)
        mentions_str = " ".join(mentions_list)

    if append_mentions and mentions and mentions_str:
        message_content = f"{message_content}\n{mentions_str}"
    elif not append_mentions and mentions and mentions_str:
        message_content = f"{mentions_str}\n{message_content}"

    if as_reply and not (as_dm and dm_channel):
        return_message = await invoking_message.reply(content=message_content, embed=embed)
    elif as_dm and dm_channel and not as_reply:
        return_message = await dm_channel.send(content=message_content, embed=embed)
    else:
        return_message = await invoking_message.channel.send(content=message_content, embed=embed)

    if pin:
        await return_message.pin()

    if reactions:
        for emote in reactions:
            await return_message.add_reaction(emote)

    return return_message


async def edit_embed_message(
        embed: Embed,
        message: Message,
        message_content: Optional[str],
) -> Message:
    """
    Edits a given :class:`Message` with an :class:`Embed` and optionally new Content.

    :param embed: The Embed to add to the Message
    :param message: The Message to be edited.
    :param message_content: Optional new Message Content. Defaults to the old Message Content.
    :return: The edited Message
    """
    message_content = message.content if not message_content else message_content
    await message.edit(
        content=message_content,
        embed=embed
    )
    return message
