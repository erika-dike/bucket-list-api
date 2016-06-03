import datetime

from flask import g, request

import errors
from ..auth import auth
from api import api
from ..decorators import json, paginate
from ..models import db, BucketList, BucketListItem


@api.route('/bucketlists/', methods=['POST'])
@auth.login_required
@json
def create_bucketlist():
    """Create a bucketlist and saves to database"""
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
@paginate()
def get_bucketlists():
    """Returns all bucketlists"""
    if request.args.get('q'):
        return BucketList.query.filter(BucketList.name.contains(
            request.args.get('q')))
    else:
        return BucketList.query


@api.route('/bucketlists/<int:id>', methods=['GET'])
@auth.login_required
@json
def get_bucketlist(id):
    """Returns a single bucketlist"""
    return BucketList.query.get_or_404(id)


@api.route('/bucketlists/<int:id>', methods=['PUT'])
@auth.login_required
@json
def edit_bucketlist(id):
    """
    Edit the name of a bucketlist

    Args:
        id -- the bucketlist identiier
    Returns:
        a dictionary of the bucketlist
    """
    bucketlist = BucketList.query.get_or_404(id)
    bucketlist.from_json(request.json)
    bucketlist.date_modified = datetime.datetime.now()
    db.session.add(bucketlist)
    db.session.commit()
    return bucketlist


@api.route('/bucketlists/<int:id>', methods=['DELETE'])
@auth.login_required
@json
def delete_bucketlist(id):
    """
    Delete a bucketlist

    Args:
        id -- the bucketlist identifier
    Returns:
        a dictionary of the result status
    """
    bucketlist = BucketList.query.get_or_404(id)
    db.session.delete(bucketlist)
    db.session.commit()
    return {'result': True}


@api.route('/bucketlists/<int:id>/items/', methods=['POST'])
@auth.login_required
@json
def create_bucketlist_item(id):
    """
    Add an item to a bucketlist

    Args:
        id -- the bucketlist identifier
    Returns:
        a tuple of the new item created, status code and a Location header
    """
    bucketlist_item = BucketListItem().from_json(request.json)
    now = datetime.datetime.now()
    bucketlist_item.date_created = now
    bucketlist_item.date_modified = now
    bucketlist = BucketList.query.get_or_404(id)
    bucketlist.items.append(bucketlist_item)
    db.session.add(bucketlist_item)
    db.session.add(bucketlist)
    db.session.commit()
    return bucketlist_item, 201, {'Location': bucketlist_item.get_url()}


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['GET'])
@auth.login_required
@json
def get_bucketlist_item(id, item_id):
    """
    Returns a bucketlist item
    
    Args:
        id -- the bucketlist identifier
        item_id -- the bucketlist item identifier
    Returns:
        BucketList item query
    """
    return BucketListItem.query.get_or_404(item_id)


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@auth.login_required
@json
def edit_bucketlist_item(id, item_id):
    """
    Edit bucketlist item

    Args:
        id -- the bucketlist identifier
        item_id -- the bucketlist item identifier
    Returns:
        a dictionary of the bucketlist item
    """
    bucketlist_item = BucketListItem.query.get_or_404(item_id)
    bucketlist_item.from_json(request.json)
    bucketlist_item.date_modified = datetime.datetime.now()
    db.session.add(bucketlist_item)
    db.session.commit()
    return bucketlist_item


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
@json
def delete_bucketlist_item(id, item_id):
    """
    Delete a bucketlist item
    Args:
        id -- the bucketlist identifier
        item_id -- the bucketlist item identifier
    Returns:
        a dictionary of the result status
    """
    bucketlist_item = BucketListItem.query.get_or_404(item_id)
    db.session.delete(bucketlist_item)
    db.session.commit()
    return {'result': True}
