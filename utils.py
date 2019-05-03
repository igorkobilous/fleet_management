import re

from flask_restful import abort
from werkzeug.exceptions import NotFound

from user.models import User


def valid_email(email_str):
    if email_str:
        return bool(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
                             email_str))
    return False


def get_object_or_abort(model, id):
    obj = model.query.get(id)
    if not obj:
        abort(404, message="Object doesn't exist")
    return obj


def is_user_in_fleet(fleet_id, user_id):
    return User.query.filter(User.fleet_id == fleet_id, User.id == user_id).first()


def get_unique_regex_from_error(err_msg):
    unique_regex = re.match(
        "UNIQUE constraint failed: (.).(.)", err_msg)
    return unique_regex


def get_paginated_list(request, objects, per_page=5):
    response_object = {
        "count": 0,
        "previous": None,
        "next": None,
        "results":[]
    }
    page = request.args.get('page')
    base_url = request.path
    query_string = request.query_string.decode('utf_8')
    query_params = query_string.split('&')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    try:
        pages = objects.paginate(page=page, per_page=per_page)
    except NotFound:
        return response_object

    if len(query_params) > 1 and 'page' in query_string:
        base_url += '?'
        for param in query_params:
            if 'page' not in param:
                base_url += param
        base_url += '&'
    elif query_params and 'page' not in query_string:
        base_url += '?' + query_string + '&'
    else:
        base_url += '?'

    response_object['count'] = pages.total
    prev_url = base_url + 'page={}'.format(pages.prev_num) if pages.has_prev else None
    response_object['previous'] = prev_url
    next_url = base_url + 'page={}'.format(pages.next_num) if pages.has_next else None
    response_object['next'] = next_url
    response_object['results'] = pages.items
    return response_object
