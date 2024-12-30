from django.contrib.sitemaps import Sitemap
from taggit.models import Tag
from django.urls import reverse
from blog.models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated


class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Get only tags that are actually used in posts
        return Tag.objects.filter(post__status="PB").distinct()

    def location(self, obj):
        return reverse("blog:post_list_by_tag", args=[obj.slug])

    # def lastmod(self, obj):
    #     # Get the most recent post for this tag
    #     return obj.post_set.filter(status="PB").latest("updated").updated


def lastmod(self, obj):
    # Get the most recent post for this tag using taggit's reverse relation
    return (
        obj.taggit_taggeditem_items.filter(content_object__status="PB")
        .latest("content_object__updated")
        .content_object.updated
    )
