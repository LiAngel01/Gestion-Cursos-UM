from django.urls import path
from . import views

urlpatterns = [
   path("",views.index,name="index"),
   path("horario-del-dia",views.ordenDelDia,name="ordendeldia"),
   path("pcdc/", views.pcdc, name="pcdc"),
   path("historico/",views.histórico, name="historico"),
   path("galeria/", views.galeria, name="galeria"),
   path("eventos/",views.eventos, name="eventos"),
   
   path("user-list/", views.list_users, name="list_users"),
   path("newuser",views.new_user,name="new_user"),
   path("delete/<id>",views.delete_user,name="delete_user"),
   path("modify_user/<id>/",views.change_user,name="change_user"),
   path("customedForm/", views.useCustomedForm, name="customedForm"),
   path("user_data/<id>", views.user_data, name="oficer_data"),
]