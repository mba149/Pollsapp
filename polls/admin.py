from django.contrib import admin
from .models import Question, Choice

# To add multiple choices on add question page
# Creating class and inheriting tabularinline
# overriding choices option
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3



class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),    
        ('Date information', {'fields': ['pub_date']}),
        ('Published By',     {'fields': ['author']}),
        ]

    # To add multiple choices on add question page
    inlines = [ChoiceInline]    
    
    #list_display admin option, which is a tuple 
    # of field names to display, as columns, on 
    # the change list page for the object:
    list_display = ('question_text','author','pub_date','was_published_recently')

    # This adds filter sidebar that lets u change list by pub_date field:
    list_filter = ['pub_date']

    # Adds search box at the top of the change list
    # uses LIKE querry behind, limiting search fields  
    # to limited number of results
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)



# Register your models here.
