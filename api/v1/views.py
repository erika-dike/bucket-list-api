from flask import g, request

from ..auth import token_auth
from api_init import api
from ..decorators import json, paginate, authorized
from .. import errors
from ..models import BucketList, BucketListItem


@api.route('/bucketlists/', methods=['POST'])
@token_auth.login_required
@json
def create_bucketlist():
    """Create a bucketlist and saves to database"""
    bucketlist = BucketList().from_json(request.json)
    g.user.bucketlist.append(bucketlist)
    bucketlist.save()
    return bucketlist, 201


@api.route('/bucketlists/', methods=['GET'])
@token_auth.login_required
@paginate()
def get_bucketlists():
    """Returns all bucketlists belonging to calling user"""
    if request.args.get('q'):
        return BucketList.query.filter_by(creator_id=g.user.id).filter(
            BucketList.name.contains(request.args.get('q')))
    else:
        return BucketList.query.filter_by(creator_id=g.user.id)


@api.route('/bucketlists/<int:id>', methods=['GET'])
@token_auth.login_required
@authorized
@json
def get_bucketlist(id):
    """Returns a single bucketlist"""
    bucketlist = BucketList.query.get_or_404(id)
    if bucketlist.creator_id == g.user.id:
        return bucketlist
    else:
        return errors.unauthorized()


@api.route('/bucketlists/<int:id>', methods=['PUT'])
@token_auth.login_required
@authorized
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
    bucketlist.save()
    return bucketlist


@api.route('/bucketlists/<int:id>', methods=['DELETE'])
@token_auth.login_required
@authorized
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
    bucketlist.delete()
    return {'result': "Successful"}


@api.route('/bucketlists/<int:id>/items/', methods=['POST'])
@token_auth.login_required
@authorized
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
    bucketlist = BucketList.query.get_or_404(id)
    bucketlist.items.append(bucketlist_item)
    bucketlist_item.save()
    bucketlist.save()
    return bucketlist_item, 201


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['GET'])
@token_auth.login_required
@authorized
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
    bucketlist_item = BucketListItem.query.get_or_404(item_id)
    if bucketlist_item.bucketlist_id == id:
        return bucketlist_item
    else:
        return errors.forbidden(
            "You do not have permission to access this resource")


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@token_auth.login_required
@authorized
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
    if bucketlist_item.bucketlist_id != id:
        return errors.forbidden(
            "You do not have permission to access this resource")
    bucketlist_item.from_json(request.json)
    bucketlist_item.save()
    return bucketlist_item


@api.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@token_auth.login_required
@authorized
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
    if bucketlist_item.bucketlist_id != id:
        return errors.forbidden(
            "You do not have permission to access this resource")
    bucketlist_item.delete()
    return {'result': "Successful"}
