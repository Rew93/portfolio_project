from django import forms

from shop.models import ReviewModel, CouponCodeModel


class ReviewForm(forms.ModelForm):
    CHOICE = [
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5)
    ]
    rating = forms.ChoiceField(choices=CHOICE, widget=forms.Select(attrs={
        'class': 'form_control',
    }))
    text_comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form_control', 'placeholder': 'Review', "rows": "4", "cols": "120",
    }))

    class Meta:
        model = ReviewModel
        fields = ['rating', 'text_comment']


class ReplyReviewForm(forms.ModelForm):
    text_comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form_control', 'placeholder': 'Please enter text', "rows": "4", "cols": "120",
    }))

    class Meta:
        model = ReviewModel
        fields = ['text_comment']


class EditReviewForm(forms.ModelForm):
    CHOICE = [
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5)
    ]
    rating = forms.ChoiceField(choices=CHOICE, widget=forms.Select(attrs={
        'class': 'form_control',
    }))
    text_comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form_control', 'placeholder': 'Review', "rows": "4", "cols": "120",
    }))

    class Meta:
        model = ReviewModel
        fields = ['rating', 'text_comment']


