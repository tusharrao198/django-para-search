from django.urls import path
from . import views
from cuboidapp.views import *

urlpatterns = [
    path("check", views.example_view, name="check"),
    path("adminview", views.adminview, name="adminview"),
    
    path("addbox", views.add_box, name="addbox"),
    path("updatebox", views.update_box, name="updatebox"),
    path("deletebox/<int:box_id>/", views.delete_box, name="deletebox"),
    path("listall", views.box_list, name="listall"),
    path("listmybox", views.list_my_boxes, name="listmybox"),
]