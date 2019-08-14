# from django.shortcuts import render
from .models import feedUpdate, feed
from django.views.generic import ListView
from django.contrib.syndication.views import Feed
# import socket
# from django.shortcuts import redirect
# from django.urls import reverse
from django.db.models import Count
import re


class feedTestsView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/tests.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        header = "Результаты тестирования"
        # TODO: good testing page

        # calculations
        feed_list = feed.objects.all()

        # feed testing
        errors_regexp = []
        pattern = re.compile("^([0-9|а-я|ё|А-Я|Ё|a-z|A-Z|_|+|—])+$")
        for each in feed_list:
            if not pattern.match(each.title):
                errors_regexp.append(each.title)

        errors_duplicates = []
        for each in feed.objects.values('title').annotate(name_count=Count('title')).filter(name_count__gt=1):
            errors_duplicates.append(each['title'] + " x" + str(each['name_count']) + "; ")

        # results
        return {
            'page': {
                'title': header,
            },
            'errors': {
                'regexp': errors_regexp,
                'duplicates': errors_duplicates,
            }
        }


class feedIndexView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/feeds.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        header = "Ленты обновлений"

        # calculations
        feed_list = feed.objects.all()

        # results
        return {
            'page': {
                'title': header,
                'showAll': True,
            },
            'feed_list': feed_list,
        }


class feedIndexFullView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/feeds.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        header = "Ленты обновлений"

        # calculations
        feed_list = feed.objects.all()

        # results
        return {
            'page': {
                'title': header,
                'showAll': False,
            },
            'feed_list': feed_list,
        }


class myActivityView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/index.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        header = "Моя активность"
        multibook = True
        result_size_limit = 42
        feed_emoji_filter = '👤'

        # calculations

        # mode configuration
        feedUpdate_list = []
        feed_list = feed.feeds_by_emoji(feed_emoji_filter)

        if self.kwargs.get('mode', False) == "index" or self.kwargs.get('mode', False) == "":
            feed_title_list = []
            for each in feed_list:
                feed_title_list.append(each.title)

            feedUpdate_list = list(feedUpdate.objects.filter(title__in=feed_title_list)[:result_size_limit])
        elif self.kwargs['mode'] == "force":
            header += ": Forced"
            for each in feed_list:
                for feedUpdate_item in feed.parse(each):
                    feedUpdate_list.append(feedUpdate_item)
            feedUpdate_list.sort(key=lambda feedUpdate_list_item: str(feedUpdate_list_item.datetime), reverse=True)


        # results
        return {
            'title': header,
            'feedUpdate_list': feedUpdate_list,
            'multibook': multibook,
        }


class feedUpdateIndexView(ListView):
    model = feedUpdate
    template_name = "feedUpdate/index.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        items_limit = 1400
        items_limit_select = items_limit*8

        # calculations
        # multibook checker
        if not self.kwargs.get('feeds', False):
            multibook = True
        elif len(self.kwargs['feeds'].split("+")) > 1:
            multibook = True
        else:
            multibook = False
        # print("multibook: " + str(multibook))

        # page_title generation
        page_title = "Обновления"
        if not multibook:
            feed_one = feed.find(self.kwargs['feeds'])
            if feed_one.title_full:
                page_title = feed_one.title_full
            else:
                page_title = feed_one.title
        elif self.kwargs.get('feeds', False):
            page_title = self.kwargs['feeds']
        # print("page_title: " + str(page_title))

        # feedName generation for buttons
        try:
            feedName = self.kwargs['feeds']
        except KeyError:
            feedName = "Обновления"
        # print("feedName: " + str(feedName))

        # feed_list generation
        feed_list = []
        if not multibook:
            feed_list.append(feed.find(feedName))
        elif not self.kwargs.get('feeds', False):
            feed_list = feed.feeds_by_emoji()
        else:
            feed_list = feed.objects.filter(title__in=page_title.split("+"))
        # print("feed_list: " + str(list(feed_list)))


        # get feedUpdate_list
        feedUpdate_list = []
        if self.kwargs.get('mode', False) == "index" or self.kwargs.get('mode', False) == "":
            if page_title == "Обновления":
                feed_titles = []
                for each in feed.feeds_by_emoji():
                    feed_titles.append(each.title)

                feedUpdate_list = []
                for each in feedUpdate.objects.all()[:items_limit_select]:
                    if each.title in feed_titles:
                        feedUpdate_list.append(each)

                feedUpdate_list = feedUpdate_list[:items_limit]
            else:
                feedUpdate_list = list(feedUpdate.objects.filter(title__in=self.kwargs['feeds'].split("+"))[:items_limit])
        elif self.kwargs['mode'] == "force":
            page_title += ": Forced"
            for each in feed_list:
                for feedUpdate_item in feed.parse(each):
                    feedUpdate_list.append(feedUpdate_item)
            feedUpdate_list.sort(key=lambda feedUpdate_list_item: str(feedUpdate_list_item.datetime), reverse=True)

        return {
            'page_title': page_title,
            'feedName': feedName,
            'feedUpdate_list': feedUpdate_list,
            'multibook': multibook,
        }


class feedUpdateFeed(Feed):
    title = "Обновления RSS"
    link = "/feedUpdate/rss"
    description = "RSS feed of items shown at feedUpdate main page"

    def items(self):
        items_limit = 42

        feed_titles = []

        for each in feed.feeds_by_emoji():
            feed_titles.append(each.title)
        feedUpdate_list = list(feedUpdate.objects.filter(title__in=feed_titles)[:items_limit])

        return feedUpdate_list

    def item_title(self, item):
        return item.title + ": " + item.name

    def item_description(self, item):
        result = item.title + ": " + item.name
        return result

    def item_link(self, item):
        return item.href
