import datetime
from typing import List, Optional, Union

from discord import Embed, Colour, Message, Color


class EmbedField(object):
    def __init__(self, name: str = None, value: str = None, inline: bool = False):
        """
        Wrapper class used to create :class:`Embed` Fields. Mainly used to add Fields to :class:`EmbedWrapper` objects.

        :param name: The Name or Title of the Field
        :param value: The Value or Description of the Field
        :param inline: Flag to denote if the Field should be displayed inline or not. Default is False
        """
        self.name = name
        self.value = value
        self.inline = inline


class EmbedWrapper(object):
    """
    Wrapper class for storing :class:`Embed` data and creating Embeds.
    """
    def __init__(
            self,
            author_name: str = None, author_url: str = None, author_icon_url: str = None,
            color: Union[Colour, Color] = None, colour: Union[Colour, Color] = None,
            description: str = None,
            fields: List[EmbedField] = None,
            footer_text: str = None, footer_icon_url: str = None,
            image_url: str = None,
            thumbnail_url: str = None,
            timestamp: datetime.datetime = datetime.datetime.now(),
            title: str = None,
            embed_type: str = "rich",
            url: str = None
    ):
        """
        Discords :class:`Embed` object does have more attributes, but the ones given here are the only ones that have setters.

        :param author_name: The name attribute of Embed.author. Default is None
        :param author_url: The url attribute of Embed.author. Default is None
        :param author_icon_url: The icon_url attribute of Embed.author. Default is None
        :param color: The Embeds color. Default is None
        :param colour: The Embeds color. Default is None
        :param description: The Embeds Description or Content. Default is None
        :param fields: A List of EmbedField objects. Default is None
        :param footer_text: The text attribute of Embed.footer. Default is None
        :param footer_icon_url: The icon_url attribute of Embed.footer. Default is None
        :param image_url: URL to the Image to use as the Image for the Embed. Default is None
        :param thumbnail_url: URL to the Image to use as the Thumbnail for the Embed. Default is None
        :param timestamp: Timestamp to be displayed on the Embed. Default is datetime.datetime.now()
        :param title: The Embeds Title. Default is None
        :param embed_type: The Embeds Type. Default is "rich" and probably shouldn't be changed.
        :param url: The URL to use as a link on the Embeds Title. Default is None
        """
        self.author_name = author_name
        self.author_url = author_url
        self.author_icon_url = author_icon_url
        self.description = description
        self.fields = fields
        self.footer_text = footer_text
        self.footer_icon_url = footer_icon_url
        self.image_url = image_url
        self.thumbnail_url = thumbnail_url
        self.timestamp = timestamp
        self.title = title
        self.embed_type = embed_type
        self.url = url
        if color:
            self.color = color
        elif colour:
            self.color = colour
        else:
            self.color = None

    @property
    def embed(self) -> Embed:
        """
        Takes the objects given attributes and creates an :class:`Embed` from them.

        :return: The created Embed
        """
        embed = Embed(
            title=self.title,
            description=self.description,
            colour=self.color,
            url=self.url,
            timestamp=self.timestamp,
            type=self.embed_type
        )

        if self.author_name or self.author_icon_url or self.author_url:
            embed.set_author(
                name=self.author_name,
                icon_url=self.author_icon_url,
                url=self.author_url
            )

        if self.footer_text or self.footer_icon_url:
            embed.set_footer(
                text=self.footer_text,
                icon_url=self.footer_icon_url
            )

        if self.thumbnail_url:
            embed.set_thumbnail(url=self.thumbnail_url)

        if self.image_url:
            embed.set_image(url=self.image_url)

        if self.fields:
            for field in self.fields:
                field_name = field.name
                field_value = field.value
                field_inline = field.inline

                embed.add_field(name=field_name, value=field_value, inline=field_inline)

        return embed
