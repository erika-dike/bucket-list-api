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
def create_bucketlist():
    import pdb; pdb.set_trace()
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
    return bucketlist, 201, {'Location': bucketlist.get_url()}


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
    bucketlist.from_json(request.json)
    bucketlist.date_modified = datetime.datetime.now()
    db.session.add(bucketlist)
    db.session.commit()
    return {'name': bucketlist.name}


@api.route('/bucketlists/<int:id>', methods=['DELETE'])
@auth.login_required
@json
def delete_bucketlist(id):
    bucketlist = BucketList.query.get_or_404(id)
    db.session.delete(bucketlist)
    db.session.commit()
    return {'result': True}


@api.route('/bucketlists/<int:id>/items/', methods=['POST'])
@auth.login_required
@json
def create_bucketlist_item(id):
    bucketlist_item = BucketListItem().from_json(request.json)
    now = datetime.datetime.now()
    bucketlist_item.date_created = now
    bucketlist_item.date_modified = now
    bucketlist = BucketList.query.get_or_404(id)
    bucketlist.items.append(bucketlist_item)
    db.session.add(bucketlist_item)
    db.session.add(bucketlist)
    db.session.commit()
    return {}, 201


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['GET'])
@auth.login_required
@json
def get_bucketlist_item(id, item_id):
    return BucketListItem.query.get_or_404(item_id)


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@auth.login_required
@json
def edit_bucketlist_item(id, item_id):
    bucketlist_item = BucketListItem.query.get_or_404(item_id)
    bucketlist_item.from_json(request.json)
    bucketlist_item.date_modified = datetime.datetime.now()
    db.session.add(bucketlist_item)
    db.session.commit()
    return {}

@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
@json
def delete_bucketlist_item(id, item_id):
    bucketlist_item = BucketListItem.query.get_or_404(item_id)
    db.session.delete(bucketlist_item)
    db.session.commit()
    return {'result': True}
