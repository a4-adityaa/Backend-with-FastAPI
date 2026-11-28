import pytest
from apps.Connection_Through_ORM import models

@pytest.fixture
def test_vote(test_posts, Session, test_user):
   new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
   Session.add(new_vote)
   Session.commit()

def test_vote_on_post(authorized_client, test_posts):
   res = authorized_client.post("/vote", json={"post_id": test_posts[3].id, "dir": 1})

   assert res.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_vote): 
   res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir":1})

   assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
   res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir":0})

   assert res.status_code == 201