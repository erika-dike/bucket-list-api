import datetime

from flask import g, request

from ..auth import auth
from api_init import api
from ..decorators import json, paginate, authorized
from .. import errors
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
    db.session.add(bucketlist)
    db.session.add(g.user)
    db.session.commit()
    return bucketlist, 201, {'Location': bucketlist.get_url()}


@api.route('/bucketlists/', methods=['GET'])
@auth.login_required
@paginate()
def get_bucketlists():
    """Returns all bucketlists belonging to calling user"""
    if request.args.get('q'):
        return BucketList.query.filter_by(creator_id=g.user.id).filter(
            BucketList.name.contains(request.args.get('q')))
    else:
        return BucketList.query.filter_by(creator_id=g.user.id)


@api.route('/bucketlists/<int:id>', methods=['GET'])
@auth.login_required
@json
@authorized
def get_bucketlist(id):
    """Returns a single bucketlist"""
    bucketlist = BucketList.query.get_or_404(id)
    if bucketlist.creator_id == g.user.id:
        return bucketlist
    else:
        return errors.unauthorized()


@api.route('/bucketlists/<int:id>', methods=['PUT'])
@auth.login_required
@json
@authorized
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
@authorized
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
    return {'result': "Successful"}


@api.route('/bucketlists/<int:id>/items/', methods=['POST'])
@auth.login_required
@json
@authorized
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
@authorized
def get_bucketlist_item(id, item_id):
    """
    Returns a bucketlist item

    Args:
        id -- the bucketlist identifier
        item_id -- the bucketlist item identifier
    Returns:
        BucketList item query
    """
    bucketlist_item = BucketListItem.query.get_or_404(item_id)
    if bucketlist_item.bucketlist_id == id:
        return bucketlist_item
    else:
        return errors.forbidden(
            "You do not have permission toaccess this resource")


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@auth.login_required
@json
@authorized
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
    if bucketlist_item.bucketlist_id != id:
        return errors.forbidden(
            "You do not have permission to access this resource")
    bucketlist_item.from_json(request.json)
    bucketlist_item.date_modified = datetime.datetime.now()
    db.session.add(bucketlist_item)
    db.session.commit()
    return bucketlist_item


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
@json
@authorized
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
    if bucketlist_item.bucketlist_id != id:
        return errors.forbidden(
            "You do not have permission to access this resource")
    db.session.delete(bucketlist_item)
    db.session.commit()
    return {'result': "Successful"}
