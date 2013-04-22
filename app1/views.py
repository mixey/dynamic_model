import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import get_app, get_models
from django.db import models
from app1 import helper


def main(request):
    tables = []
    try:
        app = get_app('app1')
        for model in get_models(app):
            tables.append(model._meta.verbose_name_plural)

    except:
        pass

    return render_to_response("index.html",
                              {"tables": tables})

def get_details(request):
    table = request.POST.get("p_name", "")
    app = get_app('app1')
    store = []
    cols = []
    model = None
    for m in get_models(app):
        if table == m._meta.verbose_name_plural:
            model = m
            break

    for field in model._meta.fields:
        t = "char"
        if (type(field) == models.IntegerField):
            t = "int"
        elif (type(field) == models.DateField):
            t = "date"

        cols.append({"name": field.name, "title": field.verbose_name, "type": t})

    return HttpResponse(json.dumps({"store": helper.toJson(model.objects.values()), "cols": cols}), mimetype="application/json")

def edit_row(request):
    table = request.POST.get("p_table_name", "")
    app = get_app('app1')
    for model in get_models(app):
        if table != model._meta.verbose_name_plural: continue

        row = json.loads(request.POST.get("p_edit_row", ""))
        if (row.has_key("id")):
            item = model.objects.get(id=row["id"])
        else:
            item = model.objects.create()
        item.__dict__.update(row)
        item.save()

    return HttpResponse(json.dumps({"status": "OK"}), mimetype="application/json")
