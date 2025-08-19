from django import forms
from .models import Post, Comment


class PostForm(forms.Form):
    img = forms.ImageField(required=False)
    title = forms.CharField(max_length=256)
    content = forms.CharField(max_length=256)

    def clean_title(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title.lower() == "javascript":
            raise forms.ValidationError("Javascript is not allowed")
        return title


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if title and content and (title.lower() == content.lower()):
            raise forms.ValidationError("Title and content should be different")
        return cleaned_data
    


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'img']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and title.lower() == 'javascript':
            raise forms.ValidationError("Javascript is not allowed")
        return title

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title and content and title.lower() == content.lower():
            raise forms.ValidationError("Title and content should be different")
        return cleaned_data
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Напишите комментарий..."})
        }
