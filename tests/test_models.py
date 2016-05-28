import unittest
import datetime

from api.models import User, BucketList


class BucketListApiModelsTestSuite(unittest.TestCase):
    """Tests the models of the bucket list api"""
    def setup(self):
        self.user = User(
            username="lively_paranha",
            password_hash="razzletabi",
            date_of_birth=datetime.date.today()
        )
        self.bucket_list = BucketList(
            title="Live the life",
            description=" ",
            date_created=datetime.date.today(),
            date_last_modified=datetime.date.today()
        )

    def test_user_model(self):
        """Test that user object is properly created"""
        self.assertTrue((type(self.user) is User),
                        msg="User object was not created!!!")

    def test_bucket_list_model(self):
        """Test that Bucket List object is properly created"""
        self.assertTrue((type(self.bucket_list) is BucketList),
                        msg="Bucket List object was not created!!!")
        self.assertEqual(True, self.bucket_list.done,
                         msg="Done is not given a default value of 'False'")

    def test_user_bucket_list_relationship(self):
        """Test that relationship between user and bucketlist exists"""
        self.user.bucketlist.append(self.bucket_list)
        self.assertEqual("Live the life", self.user.bucket_list[0].title,
                         msg="Live the life != {0}".
                         format(self.user.bucket_list[0].title))
