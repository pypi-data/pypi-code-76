import re


class ParseIdentityHyperlink:
    def __init__(self, identity_type: str, data=None):
        """ Creates a new instance of ParseIdentityHyperlink to get
        entity identity from href (pk or slug).

        :param identity_type:  Name of the identity type. pk or slug
        :param data: list data
        """
        self.identity_type = identity_type
        self.data = data

    def get_entity_list_identity(self):
        """ Returns the ids of existing product promo that should be updated.
        """
        return [
            self.parse_identity_from_href(s['href']) for s in self.data
            if s.get('href')
        ]

    def parse_identity_from_href(self, href: str):
        """ Given an href (url string), return the entity identity.
        """
        if self.identity_type == "slug":
            regex = re.compile(r'.+?(?P<slug>[a-zA-Z0-9-_]+)/$')
        else:
            regex = re.compile(r'.+?(?P<pk>[a-zA-Z0-9-_]+)/$')

        # make sure href is always a string
        if isinstance(href, str):
            match = regex.search(href)
            if match:
                return match.groupdict()[self.identity_type]
