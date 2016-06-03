"""
Decorators for the API
"""

import functools

from flask import current_app, jsonify, request, url_for, wrappers


def json(f):
    """Modifies passed in function to return pretty printed JSON"""
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        rv = f(*args, **kwargs)
        status_or_headers = None
        headers = None

        # extract status code and any additional headers
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))
        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None

        # return result if an error occurred
        if isinstance(rv, wrappers.Response) and rv.status_code > 300:
            return rv

        # convert result to json and return
        if not isinstance(rv, dict):
            rv = rv.to_json()
        rv = jsonify(rv)
        if status_or_headers is not None:
            rv.status_code = status_or_headers
        if headers is not None:
            rv.headers.extend(headers)
        return rv
    return wrapped


def paginate():
    """Paginates the result of passed in functions and returns as JSON"""
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            # get the number of the page to be displayed from URL
            page = request.args.get('page', 1, type=int)

            # get the number of items to be displayed per page
            limit = min(request.args.get(
                'limit', current_app.config['DEFAULT_PER_PAGE'], type=int),
                current_app.config['MAX_PER_PAGE'])

            # get query, paginate the query and get content of query
            query = f(*args, **kwargs)
            pagination = query.paginate(page, limit)
            content = pagination.items

            # prepare the meta portion of the json response
            pages = {'page': page, 'limit': limit,
                     'total': pagination.total, 'pages': pagination.pages}
            if pagination.has_prev:
                pages['prev'] = url_for(request.endpoint,
                                        page=pagination.prev_num, limit=limit,
                                        _external=True, **kwargs)
            else:
                pages['prev'] = None
            if pagination.has_next:
                pages['next'] = url_for(request.endpoint,
                                        page=pagination.next_num, limit=limit,
                                        _external=True, **kwargs)
            else:
                pages['next'] = None
            pages['first'] = url_for(request.endpoint, page=1,
                                     limit=limit, _external=True,
                                     **kwargs)
            pages['last'] = url_for(request.endpoint, pages=pagination.pages,
                                    limit=limit, _external=True,
                                    **kwargs)
            return jsonify({
                'meta': pages,
                'bucketlists': [each.to_json() for each in content]
            })
        return wrapped
    return decorator
