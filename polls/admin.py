from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ['text']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]
    list_display = ('text', 'pub_date', 'was_published_recently')
    list_filter = ('pub_date', )
    search_fields = ('text', )
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
