from django import forms

from .models import Book, Publisher


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'edition', 'quantity', 'rating', 'publisher', 'authors']
        widgets = {
            'authors': forms.CheckboxSelectMultiple(),
        }


class BookFilterForm(forms.Form):
    keyword = forms.CharField(required=False)
    min_price = forms.FloatField(required=False, min_value=0)
    publisher = forms.ModelChoiceField(required=False, queryset=Publisher.objects.all())
