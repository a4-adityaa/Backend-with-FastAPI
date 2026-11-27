from typing import List
from apps.Connection_Through_ORM import schemas

def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    post_map= map(validate, res.json())
    # print(list(post_map))

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get("posts/")

    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    Post = schemas.PostOut(**res.json())

    assert Post.post.id == test_posts[0].id   # the second post is comming from schemas.Postout.post
    assert Post.post.content == test_posts[0].content
    assert Post.post.title == test_posts[0].title