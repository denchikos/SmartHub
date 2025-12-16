from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    query = request.GET.copy()
    existing_values = query.get(field, "")
    values_list = existing_values.split(",") if existing_values else []

    if value in values_list:
        values_list.remove(value)
    else:
        values_list.append(value)

    query[field] = ",".join([v for v in values_list if v])
    return query.urlencode()


