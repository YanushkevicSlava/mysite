from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "title", "content", "author", "category", "tags", "pub_date"
