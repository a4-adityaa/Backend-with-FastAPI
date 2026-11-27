import pytest
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


@pytest.mark.parametrize("title, content, published", [
    ("first post title", "first post content", True),
    ("second post title", "second post content", False),
    ("third post title", "third post content", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    create_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published
    assert create_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "arbitary post", "content": "arbitary content"})
    
    create_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert create_post.title == "arbitary post"
    assert create_post.content == "arbitary content"
    assert create_post.published == True
    assert create_post.owner_id == test_user['id']


def test_unauthorized_create_post(client,test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitary post", "content": "arbitary content"})

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_delete_non_existing_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/555")

    assert res.status_code == 404


def test_delete_others_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403

def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")

    res.status_code == 401


def test_update_non_existing_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/555", json=data)

    assert res.status_code == 404
