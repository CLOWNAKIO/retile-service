from django.http import JsonResponse
from django.urls import re_path, path, register_converter
from django.conf.urls import handler404
from .views import *

class extend_int:
    regex = "[-+]?\d+"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value


register_converter(extend_int, 'ext_int')

urlpatterns = [
    path('<str:provider>/<ext_int:level>/<int:resolution>/<int:z>/<int:x>/<int:y>.png/', IndexAPI.as_view(), name='index'),
    re_path('^(?P<path>.*)$', handler422, name='error422'),
]

