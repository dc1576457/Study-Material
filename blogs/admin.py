from django.contrib import admin
from blogs.models import Category, Post,Subscriber,NoteCategory,NotePost,Contact_form
from blogs import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=('image_tag','title','url','add_date',)
    search_fields=('title',)
    


admin.site.register(Category,CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display=('title','url','auther_name',)
    search_fields=('title','note_post_title','note_title',)
    list_per_page=20
    list_filter=('cat',)
admin.site.register(Post,PostAdmin)

admin.site.site_header="STUDY MATERIAL"
admin.site.site_title="STUDY MATERIAL"
admin.site.index_title="WELCOME TO STUDY MATERIAL "


class SubscriberAdmin(admin.ModelAdmin):
    list_display=('email','subscribed_at',)
admin.site.register(Subscriber,SubscriberAdmin)    



#note admin

# Register your models here.
class NoteCategoryAdmin(admin.ModelAdmin):
    list_display=('note_title',)
    search_fields=('title','note_title')
admin.site.register(NoteCategory, NoteCategoryAdmin)


class NotePostAdmin(admin.ModelAdmin):
    list_display=('note_post_title',)
    search_fields=('title','note_title',)
    list_per_page=20
    list_filter=('uploader',)
admin.site.register(NotePost,NotePostAdmin)    


class Contact_formAdmin(admin.ModelAdmin):
    list_display=('name','email',)
admin.site.register(Contact_form,Contact_formAdmin)    