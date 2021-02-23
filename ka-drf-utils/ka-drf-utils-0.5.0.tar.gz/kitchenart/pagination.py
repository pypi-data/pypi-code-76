from gramedia.common.http import LinkHeaderField, LinkHeaderRel
from gramedia.django.drf import LinkHeaderPagination as GramediaLinkHeaderPagination
from rest_framework.response import Response


class LinkHeaderPagination(GramediaLinkHeaderPagination):
    def get_paginated_response(self, data):

        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        link_parts = []

        if next_url is not None:
            link_parts.extend([
                LinkHeaderField(
                    url=next_url,
                    rel=LinkHeaderRel.next,
                    title=str(self.page.number + 1)),
                LinkHeaderField(
                    url=self.get_last_url(),
                    rel=LinkHeaderRel.last,
                    title=self.page.paginator.num_pages),
            ])

        # if we have a previous page, then we know we have a first page, too.
        if previous_url is not None:
            link_parts.extend([
                LinkHeaderField(
                    url=previous_url,
                    rel=LinkHeaderRel.prev,
                    title=str(self.page.number - 1)),
                LinkHeaderField(
                    url=self.get_first_url(),
                    rel=LinkHeaderRel.first,
                    title=str(1)),
            ])

        headers = {
            'X-Total-Results': self.page.paginator.count,
            'X-Page-Size': self.get_page_size(self.request),
            'X-Page': self.page.number
        }

        if link_parts:
            headers['Link'] = ", ".join([str(link) for link in link_parts])

        return Response(data, headers=headers)
