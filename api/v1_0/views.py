import datetime

from flask import g, url_for, request

import errors
from ..auth import auth
from api import api
from ..decorators import json
from ..models import db, User, BucketList, BucketListItem


@api.route('/bucketlists/', methods=['POST'])
@auth.login_required
@json
def bucketlists():
    # import pdb; pdb.set_trace()
    bucketlist = BucketList().from_json(request.json)
    now = datetime.datetime.now()
    bucketlist.date_created = now
    bucketlist.date_modified = now
    g.user.bucketlist.append(bucketlist)
    try:
        db.session.add(bucketlist)
        db.session.add(g.user)
        db.session.commit()
    except:
        db.session.rollback()
    return {}, 201, {'Location': bucketlist.get_url()}


@api.route('/bucketlists/', methods=['GET'])
@auth.login_required
def get_bucketlists():
    return BucketList.query.all()


@api.route('/bucketlists/<int:id>', methods=['GET'])
@auth.login_required
@json
def get_bucketlist(id):
    return BucketList.query.get_or_404(id)


@api.route('/bucketlists/<int:id>', methods=['PUT'])
@auth.login_required
@json
def edit_bucketlist(id):
    bucketlist = BucketList.query.get_or_404(id)
    import pdb; pdb.set_trace()
    bucketlist.from_json(request.json)
    bucketlist.date_modified = datetime.datetime.now()
    db.session.add(bucketlist)
    db.session.commit()
    return {}


@api.route('/bucketlists/<int:id>', methods=['DELETE'])
@auth.login_required
@json
def delete_bucketlist(id):
    bucketlist = BucketList.query.get_or_404(id)
    db.session.delete(bucketlist)
    db.session.commit()
    return {'result': True}
