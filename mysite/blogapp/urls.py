from django.urls import path
from .views import ArticlesListView, ArticleCreateView


app_name = 'blogapp'

urlpatterns = [
    path("article/", ArticlesListView.as_view(), name="articles_list"),
    path("article/create/", ArticleCreateView.as_view(), name="article_create")
]
