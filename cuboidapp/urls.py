from django.urls import path
from . import views
from cuboidapp.views import *

urlpatterns = [
    path("add", views.add_box, name="add"),
    path("update", views.update_box, name="update"),
    path("delete", views.delete_box, name="delete"),
    path("listall", views.box_list, name="listall"),
    path("listmybox", views.list_my_boxes, name="listmybox"),
]