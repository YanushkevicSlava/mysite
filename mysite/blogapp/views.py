from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Article


class ArticlesListView(ListView):
    queryset = (
        Article.objects.
        defer("content").
        select_related("author").
        prefetch_related("tags")
    )


class ArticleCreateView(CreateView):
    model = Article
    fields = "title", "content", "author", "category", "tags",
    success_url = reverse_lazy("blogapp:articles_list")

