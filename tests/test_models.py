import unittest
import datetime

from api.app import db
from api.models import User, BucketList


class BucketListApiModelsTestSuite(unittest.TestCase):
    """Tests the models of the bucket list api"""
    def setUp(self):
        self.user = User(
            username="lively_paranha",
            password_hash="razzletabi",
        )

    def test_password_attribute_is_inaccessible(self):
        with self.assertRaises(AttributeError):
            self.user.password
