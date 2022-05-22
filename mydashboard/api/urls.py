from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes,name="routes"),
    path('syncdata/',views.syncData,name="sync"),
    path('connect/',views.connectFyer,name="connect"),
    path('stock/<str:symbol>/',views.showStock,name="show-data"),
    # path('notes/<str:pk>/update/',views.updateNote,name="update-note"),
    # path('notes/<str:pk>/delete/',views.deleteNote,name="delete-note"),
    # path('notes/<str:pk>/',views.getNote,name="note"),
    
] 