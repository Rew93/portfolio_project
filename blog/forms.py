from django import forms

from blog.models import BlogModel, CategoryModel, CommentsModel


class CommentsForm(forms.ModelForm):
    text_comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': "form-control",
        'placeholder': "COMMENT",
        "rows": "4",
    }))

    class Meta:
        model = CommentsModel
        fields = ['text_comment']


class BlogForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Title"
    }))
    text_story = forms.CharField(widget=forms.Textarea(attrs={
        'class': "form-control", 'rows': '4', 'placeholder': "Write you story"
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': "form-control",
    }), required=False)
    image_2 = forms.ImageField(widget=forms.FileInput(attrs={
        'class': "form-control",
    }), required=False)
    video = forms.FileField(widget=forms.FileInput(attrs={
        'class': "form-control",
    }), required=False)
    category = forms.ModelMultipleChoiceField(queryset=CategoryModel.objects.all(),
                                              widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = BlogModel
        fields = ['title', 'text_story', 'image', 'image_2', 'video', 'category']


class UpdateBlogForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Title"
    }))
    text_story = forms.CharField(widget=forms.Textarea(attrs={
        'class': "form-control", 'rows': '4', 'placeholder': "Write you story"
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': "form-control",
    }), required=False)
    image_2 = forms.ImageField(widget=forms.FileInput(attrs={
        'class': "form-control",
    }), required=False)
    video = forms.FileField(widget=forms.FileInput(attrs={
        'class': "form-control",
    }), required=False)
    category = forms.ModelMultipleChoiceField(queryset=CategoryModel.objects.all(),
                                              widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = BlogModel
        fields = ['title', 'text_story', 'image', 'image_2', 'video', 'category']
