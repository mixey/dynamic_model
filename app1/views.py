import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import get_app, get_models, get_model
from django.db import models


def main(request):
    tables = []
    try:
        app = get_app('app1')
        for model in get_models(app):
            tables.append({"name": model._meta.module_name, "title": model._meta.verbose_name_plural})

    except:
        pass

    return render_to_response("index.html",
                              {"tables": tables})

def get_details(request):
    model = get_model("app1", request.POST.get("p_name", ""))
    cols = []
    for field in model._meta.fields:
        t = "char"
        if (type(field) == models.IntegerField):
            t = "int"
        elif (type(field) == models.DateField):
            t = "date"

        cols.append({"name": field.name, "title": field.verbose_name, "type": t})

    return HttpResponse(json.dumps({"store": json.loads(json.dumps(list(model.objects.values()), default=lambda item: str(item))), "cols": cols}), mimetype="application/json")

def edit_row(request):
    model = get_model("app1", request.POST.get("p_table_name", ""))
    row = json.loads(request.POST.get("p_edit_row", ""))
    if (row.has_key("id")):
        item = model.objects.get(id=row["id"])
    else:
        item = model.objects.create()
    item.__dict__.update(row)
    item.save()

    return HttpResponse(json.dumps({"status": "OK"}), mimetype="application/json")
