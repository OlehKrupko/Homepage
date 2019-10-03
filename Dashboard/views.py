from django.views.generic import ListView
from .models import PlanetaKino, keyValue
from datetime import datetime, time
from weatherCast.models import weatherCast
from feedUpdate.models import feedUpdate, feed


class DashboardView(ListView):
    template_name = "Dashboard/main.html"
    context_object_name = "fromView"

    def get_queryset(self):
        header_night = "Доброй ночи"
        header_morning = "Доброе утро"
        header_day = "Привет"
        header_evening = "Добрый вечер"

        now = datetime.now().time()
        if now < time(6):
            title_daypart = header_night
        elif now < time(12):
            title_daypart = header_morning
        elif now < time(18):
            title_daypart = header_day
        else:
            title_daypart = header_evening

        title_weather_sum = keyValue.objects.filter(key='weatherNowSumm')[0].value

        title_weather_sup = weatherCast.generate_weather_summary(
            keyValue.objects.filter(key='weatherNowIcon')[0].value,
            keyValue.objects.filter(key='weatherNowTemp')[0].value,
            keyValue.objects.filter(key='weatherNowProb')[0].value
        )

        movies = PlanetaKino.objects.filter(inTheater=True)

        items_limit = 42
        items_limit_select = items_limit*10

        feed_titles = []
        for each in feed.feeds_by_emoji():
            feed_titles.append(each.title)

        feed_titles_not = []
        for each in feed.feeds_by_emoji('🏮'):
            feed_titles_not.append(each.title)

        feedUpdate_list = feedUpdate.objects.filter(title__in=feed_titles)
        feedUpdate_list = feedUpdate_list.exclude(title__in=feed_titles_not)
        feedUpdate_list = feedUpdate_list[:items_limit]
        feedUpdate_list = list(feedUpdate_list)

        return {
            'title': {
                'daypart': title_daypart,
                'weather': {
                    'sum': title_weather_sum,
                    'sup': title_weather_sup,
                }
            },
            'movies': movies,
            'feedUpdate': {
                'list': feedUpdate_list,
            }
        }
