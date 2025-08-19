from django import forms
from .models import Post, Comment, Category, Tag


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

class SearchForm(forms.Form):
    q = forms.CharField(max_length=256,required=False,label="Search",
                        widget=forms.TextInput(attrs={"class": "form-control"}))
    category_id = forms.ModelChoiceField(required=False,queryset=Category.objects.all(),label="Category",
                        widget=forms.Select(attrs={"class": "form-select"}))
    tag = forms.ModelMultipleChoiceField(required=False,queryset=Tag.objects.all(),label="Tag",
                        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 5 }))
    orderings = (
        ("created_at", "По дате создания"),
        ("title", "По названию"),
        ("-created_at", "По дате создания (убывание)"),
        ("-title", "По названию (убывание)"),
        ("updated_at", "По дате обновления"),
        ("-updated_at", "По дате обновления (убывание)"),
        ("rate", "По рейтингу"),
        ("-rate", "По рейтингу (убывание)"),
        ("None", "Без сортировки"),
    )
    ordering = forms.ChoiceField(choices=orderings, required=False, label="Сортировка",
                                  widget=forms.Select(attrs={"class": "form-select"}))