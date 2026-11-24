from typing import List
from apps.Connection_Through_ORM import schemas

def test_get_all_post(authorized_client, test_post):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    post_map= map(validate, res.json())
    # print(list(post_map))

    assert len(res.json()) == len(test_post)
    assert res.status_code == 200