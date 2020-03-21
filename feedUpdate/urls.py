from django.conf.urls import url
from . import views

app_name = "feedUpdate"
urlpatterns = [
    url(r'^(?P<mode>())$', views.feedUpdateIndexView.as_view(), name="main"),  # main fU feed with modes
    url(r'^index:(?P<mode>(index|force|more))$', views.feedUpdateIndexView.as_view(), name="index"),  # main fU feed with modes
    url(r'^other:(?P<mode>(index|force|more))', views.otherView.as_view(), name="other"),  # list other

    # pages
    url(r'^feeds:(?P<mode>(index|other|all))$', views.feedIndexView.as_view(), name="feeds"),  # list feeds
    url(r'^rss$', views.feedUpdateFeed(), name="rss"),  # RSS feed
    url(r'^tests$', views.feedTestsView.as_view(), name="tests"),  # testing page
    
    url(r'^feed/(?P<feeds>([0-9|а-я|ё|А-Я|Ё|a-z|A-Z|_|+|—])*):(?P<mode>(index|force|more))?$', views.feedUpdateIndexView.as_view(), name="feed"),  # view custom feed
]
