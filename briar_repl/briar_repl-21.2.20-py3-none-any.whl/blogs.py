from .start_up import URLS
from .network import req_get, req_post


async def get_blog_posts():
    resp = await req_get(
        url=URLS.blogs,
        topic="get_blogs",
    )
    return resp


async def show_blog_posts():
    """
    lists blog posts
    """
    posts = await get_blog_posts()
    if posts:
        print(f"  > showing {len(posts)} blog posts:")
        for blog_post in posts:
            print(f"{blog_post}")


async def post_blog_entry(blog_text):
    """
    posts blog entry
    """
    resp = await req_post(
        url=URLS.blogs,
        json_data={"text": blog_text},
        topic="post_blog_entry",
    )
    return resp.json()

