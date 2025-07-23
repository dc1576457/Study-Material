import email
from email import message
from tkinter import CASCADE
from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.urls import reverse




# Create your models here.
class Category(models.Model):
    cat_id =models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    description= HTMLField()
    url=models.CharField(max_length=100)
    image=models.ImageField(upload_to="Category/")
    add_date=models.DateField(auto_now_add=True, null=True)
    
    def image_tag(self):
        return format_html('<img src="/media/{}" style="width:40px;height:40px; border-radius:50%;"/>'.format(self.image))
    def __str__(self):
        return self.title
   

class Post(models.Model):
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    content= HTMLField()
    cat=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='Post/')
    auther_name=models.CharField(max_length=50) 
    url=models.CharField(max_length=100)
    
    STATUS_CHOICES=(
        ('private','private'),
        ('public','public'),
        )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='public')
    def __str__(self):
        return self.title
    
     # ✅ Insert this method inside Post model

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None

        if not is_new:
            old_status = Post.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        if self.status == 'public' and (is_new or old_status != 'public'):
            subscribers = Subscriber.objects.all()

            # ✅ Generate post detail URL using the slug
            post_url = f'http://yourdomin.com:8000/{reverse("trans", args=[self.url])}'

            # ✅ 200-word content snippet
            content_words = self.content.split()
            excerpt = ' '.join(content_words[:200]) + ('...' if len(content_words) > 200 else '')

            # ✅ Email HTML content
            html_message = f"""
                <h2><a href="{post_url}" target="_blank" style="text-decoration:none;color:#2a2a2a;">{self.title}</a></h2>
                <a href="{post_url}" target="_blank">
                    <img src="/media/{self.image.url}" alt="Post Image" style="max-width:40%;height:auto;border-radius:8px;" />
                </a>
                <p style="font-size:14px;color:#444;margin-top:10px;">{excerpt}</p>
                <p><a href="{post_url}" target="_blank" style="color:#007bff;">Read more...</a></p>
            """

            # ✅ Plain text fallback for non-HTML email clients
            plain_message = strip_tags(html_message)

            for sub in subscribers:
                send_mail(
                    subject=f'New Post Published: {self.title}',
                    message=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[sub.email],
                    fail_silently=False,
                    html_message=html_message,
                )

    
    
    #email notification integration
class Subscriber(models.Model):
    email = models.EmailField(unique=True, null=False, blank=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES=(
        ('private','private'),
        ('public','public'),
        )

    def __str__(self):
        return self.email
    
    
    

    
    #notes models 


# Create your models here.
    
class NoteCategory(models.Model):
    note_id=models.AutoField(primary_key=True)
    note_title=models.CharField(max_length=100)
    add_to=models.DateField(auto_now_add=True,null=True)
    note_image=models.ImageField(upload_to='Note_category')
    url=models.CharField(max_length=100)
    
    def __str__(self):
        return self.note_title


class NotePost(models.Model):
    note_post_id=models.AutoField(primary_key=True)
    note_post_title=models.CharField(max_length=100)
    url=models.CharField(max_length=100)
    note_post_des=HTMLField(max_length=200)
    note_file=models.FileField(upload_to='notes_post/')
    add_to_date=models.DateField(auto_now_add=True,null=True)
    note_post_image=models.ImageField(upload_to='Note_post/')
    uploader=models.ForeignKey(NoteCategory, on_delete=models.CASCADE)
    
    
    STATUS_CHOICES=(
        ('private','private'),
        ('public','public'),
        )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='public')
    
    def __str__(self):
        return self.note_post_title
    
class Contact_form(models.Model):
    cont_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    messages=models.CharField(max_length=300)
    def __str__(self):
        return self.name        