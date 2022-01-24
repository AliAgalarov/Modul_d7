from django.urls import path
from .views import NewsList, NewsDetailView, NewsAddView, AddNews, NewsEditView, NewsDeleteView, NewsSearch, add_subscribe, \
    del_subscribe


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='newsPort_detail'),  # Ссылка на детали новости
    path('add/', NewsAddView.as_view(), name='news_add'),  # Ссылка на создание новости
    path('edit/<int:pk>', NewsEditView.as_view(), name='newsP_edit'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='delete'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
]

