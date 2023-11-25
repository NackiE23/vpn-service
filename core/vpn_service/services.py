from bs4 import ResultSet
from django.urls import reverse


def change_tags_link(site_pk: int, site_slug: str, tag_items: ResultSet, link_prop: str):
    for tag in tag_items:
        link = tag.get(link_prop)

        if link and link.startswith('/'):
            tag[link_prop] = reverse(
                'site',
                kwargs={
                    'site_pk': site_pk,
                    'site_slug': site_slug,
                    'domain_url': link
                }
            )
