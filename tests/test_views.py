"""
Tests for bucketlist api routes
"""
import json
import os
import unittest

from flask import url_for, g

from api.app import create_app, db
from api.models import User, BucketList, BucketListItem
from helpers import create_api_headers


class TestAPI(unittest.TestCase):
    default_username = 'rikky_dyke'
    default_password = 'password'
    another_user = 'sage_of_six_paths'
    bucketlist_name = 'Bucketlist_A'
    bucketlist_item_name = 'Live a charged life.'
    bucketlist2_name = 'Bucketlist_B'
    bucketlist_item2_name = 'Love openly.'
    bucketlist3_name = 'Bucketlist_C'
    bucketlist_item3_name = 'Free my mind from all or most lies'

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        user = User(username=self.default_username,
                    password=self.default_password)
        user2 = User(username=self.another_user,
                     password=self.default_password)
        db.session.add_all([user, user2])
        db.session.commit()
        g.user = user

        bucketlist = BucketList(name=self.bucketlist_name, creator_id=user.id)
        bucketlist2 = BucketList(name=self.bucketlist2_name,
                                 creator_id=user2.id)
        bucketlist3 = BucketList(name=self.bucketlist3_name,
                                 creator_id=user.id)
        db.session.add_all([bucketlist, bucketlist2, bucketlist3])
        db.session.commit()

        bucketlist_item = BucketListItem(
            name=self.bucketlist_item_name, bucketlist_id=bucketlist.id
        )
        bucketlist_item2 = BucketListItem(
            name=self.bucketlist_item2_name, bucketlist_id=bucketlist2.id
        )
        bucketlist_item3 = BucketListItem(
            name=self.bucketlist_item3_name, bucketlist_id=bucketlist3.id
        )
        db.session.add_all([bucketlist_item, bucketlist_item2,
                            bucketlist_item3])
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls):
        pwd = os.getcwd()
        os.remove(pwd + '/bucketlistdb-test.sqlite')

    def get_token(self):
        """Calls the login function and returns the token generated"""
        response = self.client.post(
            url_for('api.login'),
            headers=create_api_headers('rikky_dyke', 'password'),
            data=json.dumps({'username': 'rikky_dyke',
                             'password': 'password'}))
        token = json.loads(response.data)['Token']
        return token

    def test_get_bucketlists(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlists'),
            headers=create_api_headers(token, ''))
        self.assertEquals(response.status_code, 200)

    def test_get_bucketlists_with_limit(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlists'), query_string={'limit': '1'},
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['meta']['limit'], 1)

    def test_get_bucketlists_with_max_limit(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlists'), query_string={'limit': '200'},
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['meta']['limit'], 100)

    def test_get_bucketlists_with_search(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlists'), query_string={'q': 'bucket'},
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['bucketlists'][0]['name'], 'Bucketlist_A')

    def test_user_would_only_get_bucketlists_owned(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlists'),
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        print data
        self.assertEquals(len(data['bucketlists']), 2)
        self.assertEquals(data['bucketlists'][0]['created_by'], 'rikky_dyke')

    def test_get_single_bucketlist(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlist', id=1),
            headers=create_api_headers(token, ''))
        self.assertEquals(response.status_code, 200)

    def test_get_non_existent_bucketlist(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlist', id=10),
            headers=create_api_headers(token, ''))
        self.assertEquals(response.status_code, 404)

    def test_user_cannot_access_bucketlist_of_another(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlist', id=2),
            headers=create_api_headers(token, ''))
        self.assertEquals(response.status_code, 403)

    def test_create_bucketlist(self):
        token = self.get_token()
        response = self.client.post(
            url_for('api.create_bucketlist'),
            headers=create_api_headers(token, ''),
            data=json.dumps({'name': self.bucketlist3_name}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 201)
        self.assertEquals(data['name'], self.bucketlist3_name)

    def test_that_api_throws_error_if_keyword_name_not_provided(self):
        token = self.get_token()
        response = self.client.post(
            url_for('api.create_bucketlist'),
            headers=create_api_headers(token, ''),
            data=json.dumps({'raziel': self.bucketlist3_name}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['error'], 'bad request')

    def test_edit_bucketlist(self):
        token = self.get_token()
        response = self.client.put(
            url_for('api.edit_bucketlist', id=1),
            headers=create_api_headers(token, ''),
            data=json.dumps({'name': self.bucketlist3_name}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['name'], self.bucketlist3_name)

    def test_user_cannot_edit_anothers_bucketlist(self):
        token = self.get_token()
        response = self.client.put(
            url_for('api.edit_bucketlist', id=2),
            headers=create_api_headers(token, ''),
            data=json.dumps({'name': self.bucketlist3_name}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['message'],
                          'You do not have permission to access this resource')

    def test_delete_bucketlist(self):
        token = self.get_token()
        response = self.client.delete(
            url_for('api.delete_bucketlist', id=1),
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['result'], 'Successful')

    def test_user_cannot_delete_anothers_bucketlist(self):
        token = self.get_token()
        response = self.client.delete(
            url_for('api.delete_bucketlist', id=2),
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['error'], 'forbidden')

    def test_create_bucketlist_item(self):
        token = self.get_token()
        response = self.client.post(
            url_for('api.create_bucketlist_item', id=1),
            headers=create_api_headers(token, ''),
            data=json.dumps({'name': self.bucketlist_item3_name}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 201)
        self.assertEquals(data['name'], self.bucketlist_item3_name)

    def test_create_bucketlist_item_fails_on_invalid_argument(self):
        token = self.get_token()
        response = self.client.post(
            url_for('api.create_bucketlist_item', id=1),
            headers=create_api_headers(token, ''),
            data=json.dumps({'nemesis': self.bucketlist_item3_name}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['error'], 'bad request')

    def test_user_cannot_create_item_in_anothers_bucketlist(self):
        token = self.get_token()
        response = self.client.post(
            url_for('api.create_bucketlist_item', id=2),
            headers=create_api_headers(token, ''),
            data=json.dumps({'name': self.bucketlist_item3_name}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['error'], 'forbidden')

    def test_get_bucketlist_item(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlist_item', id=1, item_id=1),
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['name'], self.bucketlist_item_name)

    def test_user_cannot_get_anothers_bucketlist_item(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlist_item', id=2, item_id=2),
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['error'], 'forbidden')

    def test_only_item_belonging_to_a_bucketlist_id_can_be_viewed(self):
        token = self.get_token()
        response = self.client.get(
            url_for('api.get_bucketlist_item', id=1, item_id=3),
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['error'], 'forbidden')

    def test_edit_bucketlist_item(self):
        token = self.get_token()
        response = self.client.put(
            url_for('api.edit_bucketlist_item', id=1, item_id=1),
            headers=create_api_headers(token, ''),
            data=json.dumps({'name': 'Reach a state of balance'}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['name'], 'Reach a state of balance')

    def test_edit_bucketlist_items_done_attribute(self):
        token = self.get_token()
        response = self.client.put(
            url_for('api.edit_bucketlist_item', id=1, item_id=1),
            headers=create_api_headers(token, ''),
            data=json.dumps({'done': 'True'}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['done'], True)

    def test_user_cannot_edit_anothers_bucketlist_item(self):
        token = self.get_token()
        response = self.client.put(
            url_for('api.edit_bucketlist_item', id=2, item_id=2),
            headers=create_api_headers(token, ''),
            data=json.dumps({'name': self.bucketlist3_name}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['message'],
                          'You do not have permission to access this resource')

    def test_edit_only_works_for_items_with_appropriate_bucketlist_id(self):
        token = self.get_token()
        response = self.client.put(
            url_for('api.edit_bucketlist_item', id=1, item_id=3),
            headers=create_api_headers(token, ''),
            data=json.dumps({'name': self.bucketlist3_name}))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['message'],
                         'You do not have permission to access this resource')

    def test_delete_bucketlist_item(self):
        token = self.get_token()
        response = self.client.delete(
            url_for('api.delete_bucketlist_item', id=1, item_id=1),
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['result'], 'Successful')

    def test_user_cannot_delete_anothers_bucketlist_item(self):
        token = self.get_token()
        response = self.client.delete(
            url_for('api.delete_bucketlist_item', id=2, item_id=2),
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['error'], 'forbidden')

    def test_delete_only_works_for_items_with_appropriate_bucketlist_id(self):
        token = self.get_token()
        response = self.client.delete(
            url_for('api.delete_bucketlist_item', id=1, item_id=3),
            headers=create_api_headers(token, ''))
        data = json.loads(response.get_data(as_text=True))
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['error'], 'forbidden')
