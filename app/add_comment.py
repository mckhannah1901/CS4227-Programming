from app import abstract_factory


def add_comment(post_id, content, comment_type):
    if comment_type == "text":
        abstract_factory.add_text_comment(post_id, content)
    elif comment_type == "emoji":
        abstract_factory.add_emoji_comment(post_id, content)

