from django.contrib import admin
from django import forms
from django.forms import BaseInlineFormSet
from .models import Movie, Serie, Chapter, Season, Genre, ListContent, MovieContent, SerieContent


class BaseContentFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Validar que solo haya un contenido por tipo en la lista
        movie_count = 0
        serie_count = 0

        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                continue

            content_type = form.cleaned_data.get('content_type')

            if content_type == MovieContent.content_type:
                movie_count += 1
            elif content_type == SerieContent.content_type:
                serie_count += 1

        if movie_count > 1 or serie_count > 1:
            raise forms.ValidationError("Solo se permite una película y una serie por lista.")

class MovieContentInline(admin.TabularInline):
    model = MovieContent
    extra = 1
    formset = BaseContentFormSet

class SerieContentInline(admin.TabularInline):
    model = SerieContent
    extra = 1
    formset = BaseContentFormSet

class ListContentAdminForm(forms.ModelForm):
    class Meta:
        model = ListContent
        fields = '__all__'

class ListContentAdmin(admin.ModelAdmin):
    form = ListContentAdminForm
    inlines = [MovieContentInline, SerieContentInline]


# Register your models here.
admin.site.register(Movie)
admin.site.register(Serie)
admin.site.register(Season)
admin.site.register(Chapter)
admin.site.register(Genre)
admin.site.register(ListContent, ListContentAdmin)