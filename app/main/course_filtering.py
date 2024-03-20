from flask import request
from sqlalchemy import Integer, cast, func
from app.models import Course, School, Technology


def filter_courses(filter_dict, selected_filters, query=None):
    if query is None:
        query = Course.query
    price_from = request.args.get('price_from')
    price_to = request.args.get('price_to')
    duration_from = request.args.get('duration_from')
    duration_to = request.args.get('duration_to')
    search_str = request.args.get('search')
    select_filter_dict = {key: [] for key in filter_dict.keys()}
    for item in selected_filters:
        for key, value in filter_dict.items():
            if item in value:
                select_filter_dict[key].append(item)
                break
    if price_from:
        query = query.filter(Course.price >= float(price_from))
    if price_to:
        query = query.filter(Course.price <= float(price_to))
    if duration_from:
        query = query.filter(cast(Course.duration, Integer) >= int(duration_from))
    if duration_to:
        query = query.filter(cast(Course.duration, Integer) <= int(duration_to))
    if search_str:
        query = query.filter(Course.name.ilike(f'%{search_str}%'))
        # query = query.filter(func.similarity(Course.name, search_str) > 0.5)
    if select_filter_dict["Школа"]:
        query = query.join(School).filter(
            School.title.in_(select_filter_dict["Школа"]))
    if select_filter_dict["Направления"]:
        query = query.filter(Course.technologies.any(Technology.title.in_(select_filter_dict["Направления"])))
    return query
