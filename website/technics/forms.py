from django import forms

from .models import Comments


class CommentForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Comments
        fields = ('name', 'email', 'text')
