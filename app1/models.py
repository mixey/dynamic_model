#-*- coding:UTF-8 -*-
from django.db import models
import yaml


class DynamicModels(object):
    store = {}

    def _create_model(self, fields = None, meta_opts = None):

        table_name = "dynamic_table_" + meta_opts["verbose_name"]

        class Meta:
            app_label = 'app1'
            db_table = table_name

        if meta_opts is not None:
            for key, value in meta_opts.iteritems():
                setattr(Meta, key, value)

        attrs = {'__module__': self.__class__.__module__,
                 'Meta' : Meta,
                 'objects' : models.Manager()}

        if fields:
            attrs.update(fields)

        self.__class__.store["dynamic_model_" + table_name] = type(table_name, (models.Model,), attrs)

    def create(self, template):
        for name in template:
            m = template[name]

            fields = {}
            for f in m["fields"]:
                if f["type"] == "int":
                    fields[f["id"]] = models.IntegerField(verbose_name=f["title"], null=True)
                elif f["type"] == "date":
                    fields[f["id"]] = models.DateField(verbose_name=f["title"], null=True)
                else:
                    fields[f["id"]] = models.CharField(max_length=100, verbose_name=f["title"], null=True)

            self._create_model(fields, {"verbose_name": name,
                                        "verbose_name_plural": m["title"]})


f = open("models.yaml", 'r')
templ = yaml.load(f)
f.close()

DynamicModels().create(templ)
