import datetime


def toJson(valuesQuerySet):
    result = []
    for item in valuesQuerySet:
        d = {}
        for key in dict(item).keys():
            if type(item.get(key)) is list:
                d[key] = toJson(dict(item).get(key))
                continue

            d[key] = str(dict(item).get(key)) if type(dict(item).get(key)) is datetime.date else dict(item).get(key)
        result.append(d)
    return result

