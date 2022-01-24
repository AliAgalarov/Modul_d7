from django.forms import ModelForm, BooleanField
from .models import Post


class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'categoryType', 'category', 'title', 'text']