from itertools import chain
from django.shortcuts import  render,redirect
from blogs.models import Category, NoteCategory,Post, Subscriber,Contact_form
from django.http import HttpResponse
# Create your views here.
def home(request):
    cat=Category.objects.all()
    post=Post.objects.all()[:12]
    return render(request,'home.html',{ "posts":post,'cats':cat,})


def contact(request):
    cat = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        messages = request.POST.get('sms')

        try:
            Contact_form.objects.create(name=name, email=email, messages=messages)
            # Store success message in session
            request.session['message'] = 'Send Successfully!'
        except Exception as e:
            request.session['message'] = 'Failed! Try Again!'

        # Redirect to GET after processing POST (PRG pattern)
        return redirect('contact')

    # Fetch message if exists
    message = request.session.pop('message', None)

    return render(request, 'contact.html', {'cats': cat, 'message': message})


def about(request):
    cat=Category.objects.all()
    return render(request,'about.html',{'cats':cat})



from django.db.models import Q
from blogs.models import Post, Category

from django.db.models import Q
from blogs.models import Post, NotePost, Category, NoteCategory

def Search(request):
    query = request.GET.get('q', '').strip()
    post_results = []
    note_results = []

    if query:
        keywords = query.split()
        post_filter = Q()
        note_filter = Q()

        for word in keywords:
            post_filter |= Q(title__icontains=word)
            note_filter |= Q(note_post_title__icontains=word)

        post_results = Post.objects.filter(post_filter).distinct()
        note_results = NotePost.objects.filter(note_filter).distinct()

    context = {
        'query': query,
        'post_results': post_results,
        'note_results': note_results,
        'cats': Category.objects.all(),
    }
    return render(request, 'search_result.html', context)



def trans(request,url):
    try:  
        cat=Category.objects.all()
        posts1=Post.objects.all()
        post= Post.objects.get(url=url)
        return render(request,'trans.html',{'post':post,'cats':cat,'post1':posts1})
    except Post.DoesNotExist:
        return render(request,"trans.html",{'Page not Found !'},status=404)

def category(request,url):
    cats=Category.objects.all()
    cat=Category.objects.get(url=url)
    post=Post.objects.filter(cat=cat)
    return render(request,'category.html',{'cat':cat,'post':post,'cats':cats})   




#email notification integration
# views.py
def subscriber_user(request):
    if request.method =='POST':
        email=request.POST.get('email')
        if email:
           subscriber,create=Subscriber.objects.get_or_create(email=email)
           return HttpResponse("<script>alert('Subscription Successfully !');window.location.href='/'</script>") 
        return HttpResponse("<script>alert('Please enter a valid email !');window.location.href='/'</script>")
    return render(request,'subscribe.html')     







# #note views


from blogs.models import Category
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from blogs.models import NotePost,NoteCategory


def notes(request):
    uploader_id = request.GET.get('uploader')
    search_query = request.GET.get('search')

    posts = NotePost.objects.all()

    if uploader_id:
        posts = posts.filter(uploader_id=uploader_id)
        
    if search_query:
        search_words = search_query.strip().split()
        search_filter = Q()
        for word in search_words:
            search_filter |= Q(note_post_title__icontains=word)
        posts = posts.filter(search_filter)

    context = {
        'post': posts,
        'uploaders': NoteCategory.objects.all(),
        'selected_uploader': uploader_id,
        'search_query': search_query,
        'cats':Category.objects.all(),
    }

    return render(request, 'notes.html', context)




def dox_details(request, url):
    # Get category object
    cat=Category.objects.all()
    category = get_object_or_404(NoteCategory, url=url)
    posts = NotePost.objects.filter(uploader=category)
   

    return render(request, 'dox_details.html', {'post': posts, 'category': category,'cats':cat})

