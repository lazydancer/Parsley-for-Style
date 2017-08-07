from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^recipes/$', views.RecipeListView.as_view(), name='recipes'), 
    url(r'^addrecipe/$', views.addRecipe, name='addRecipe'),
]