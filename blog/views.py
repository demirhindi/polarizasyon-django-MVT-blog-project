from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from accounts.models import User
from django.contrib.auth.decorators import login_required
from .models import Category,AuthorInfo,BlogContext,Tags,BlogImage,Carousel
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.db.models import Q
from .forms import CommentForm
from .models import Comment
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from accounts.models import SubscriberUser
from .forms import ContactForm
from django.core.cache import cache
from django.views.decorators.cache import cache_page



def home(request):
    # Anahtar oluşturma
    cache_key = "home_data"

    # Önbellekten verileri alma
    data_to_cache = cache.get(cache_key)
    if data_to_cache is not None:
        return render(request, 'pages/mainpage.html', data_to_cache)

    # Önbellekte veri yoksa, veritabanından verileri getirme
    carousels = Carousel.objects.all().order_by('-id')
    homeCategory = Category.objects.all().order_by('title')
    popular_posts = BlogContext.objects.all().order_by('-click_count')[:10]
    homeAuthors = AuthorInfo.objects.all().order_by('slug')
    hometags = Tags.objects.all().order_by('slug')
    homeBlog = BlogContext.objects.all().order_by('-created_field')
    paginator = Paginator(homeBlog, 6)
    page = request.GET.get('page')
    pagedblog = paginator.get_page(page)

    # Önbellekte saklama
    data_to_cache = {
        "carousels": carousels,
        "homeCategory": homeCategory,
        "homeAuthors": homeAuthors,
        "homeBlog": homeBlog,
        "pagedblog": pagedblog,
        "hometags": hometags,
        "popular_posts": popular_posts
    }
    cache.set(cache_key, data_to_cache, timeout=20)

    return render(request, 'pages/mainpage.html', data_to_cache)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            homeCategory=Category.objects.all().order_by('title')
            homeAuthors=AuthorInfo.objects.all().order_by('slug')
            carousels= Carousel.objects.all().order_by('-id')
            popular_posts = BlogContext.objects.all().order_by('-click_count')[:10]
            hometags=Tags.objects.all().order_by('slug')
            homeBlog= BlogContext.objects.order_by('-title').filter( Q(title__icontains=keyword) | Q(tags__title__icontains=keyword) | Q(author__user__first_name__icontains=keyword) | Q(author__user__last_name__icontains=keyword) | Q(author__user__username__icontains=keyword))
            
            paginator=Paginator(homeBlog ,6)
            page= request.GET.get('page')
            pagedblog= paginator.get_page(page)

            
           
    context = {
        "carousels":carousels,
        "homeCategory":homeCategory,
        "homeAuthors":homeAuthors,
        "homeBlog":homeBlog,
        "pagedblog":pagedblog,
        "hometags":hometags,
        "popular_posts":popular_posts,


    }
    return render(request,'pages/mainpage.html',context)





@cache_page(60 * 1) # cache 1 dakika
def detail(request,blog_slug=None):
    detailforcomment = get_object_or_404(BlogContext, slug=blog_slug)
    detailBlog=BlogContext.objects.filter(slug=blog_slug)
    
    detailforcomment.save()

    
    
    imagesdetail = get_object_or_404(BlogContext, slug=blog_slug)
    detailimage  = BlogImage.objects.filter(user=imagesdetail)

    user = request.user
    comments = Comment.objects.filter(post=detailforcomment).order_by('-date')
    commentsCount=Comment.objects.filter(post=detailforcomment).count()


    

    if request.method == 'POST':
        forms = CommentForm(request.POST)
        if forms.is_valid():
            comment = forms.save(commit=False)
            comment.post = detailforcomment
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('detail', args=[blog_slug]))
    else:
        forms = CommentForm()
    
    context= {   
        "detailBlog":detailBlog,
        "detailimage":detailimage,
        'comments': comments,
        'forms':forms,
        'commentsCount':commentsCount,
    }

    return render(request, 'pages/detailpage.html', context)





def author(request,author_slug=None):
    detailAuthor=AuthorInfo.objects.filter(slug=author_slug)
    context= {   
        "detailAuthor":detailAuthor,         
        
    }
    return render(request,'pages/authorpage.html',context)


def category(request,category_slug=None):
    carousels= Carousel.objects.all().order_by('-id')
    homeCategory=Category.objects.all().order_by('title')
    homeAuthors=AuthorInfo.objects.all().order_by('slug')
    hometags=Tags.objects.all().order_by('slug')
    popular_posts = BlogContext.objects.all().order_by('-click_count')[:10]

    categories = get_object_or_404(Category, slug=category_slug)
    homeBlog  = BlogContext.objects.filter(category=categories).order_by('-created_field') 

  

    paginator=Paginator(homeBlog ,6)
    page= request.GET.get('page')
    pagedblog= paginator.get_page(page)

           
        
    context= {  
        "carousels":carousels,
        "homeCategory":homeCategory,
        "homeAuthors":homeAuthors,
        "homeBlog":homeBlog,
        "pagedblog":pagedblog,
        "hometags":hometags,
        "popular_posts": popular_posts,

        
        
    }
    return render(request,'pages/mainpage.html',context)


def tags(request, tags_slug=None):
    # Anahtar oluşturma
    cache_key = f"tags_data_{tags_slug}"

    # Önbellekten verileri alma
    data_to_cache = cache.get(cache_key)
    if data_to_cache is not None:
        return render(request, 'pages/mainpage.html', data_to_cache)

    carousels = Carousel.objects.all().order_by('-id')
    homeCategory = Category.objects.all().order_by('title')
    homeAuthors = AuthorInfo.objects.all().order_by('slug')
    hometags = Tags.objects.all().order_by('slug')
    popular_posts = BlogContext.objects.all().order_by('-click_count')[:10]

    tags = get_object_or_404(Tags, slug=tags_slug)
    homeBlog = BlogContext.objects.filter(tags=tags).order_by('-created_field')
    paginator = Paginator(homeBlog, 6)
    page = request.GET.get('page')
    pagedblog = paginator.get_page(page)

    # Önbellekte saklama
    data_to_cache = {
        "carousels":carousels,
        "homeCategory":homeCategory,
        "homeAuthors":homeAuthors,
        "homeBlog":homeBlog,
        "pagedblog":pagedblog,
        "hometags":hometags,
        "popular_posts": popular_posts,
    }
    cache.set(cache_key, data_to_cache, timeout=60)

    return render(request, 'pages/mainpage.html', data_to_cache)
    


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if user with this email already exists
        if SubscriberUser.objects.filter(email=email).exists():
            messages.error(request, 'Bu mail zaten mevcut')
            return redirect('home')
        # Create new user with email as username
        user = SubscriberUser.objects.create(email=email)
        user.set_unusable_password()
        user.save()
        
        messages.success(request, 'Abonelik Tamamlandı')
        return redirect('home')
    return redirect('home')





def unsubscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Find user with given email
        try:
            user = SubscriberUser.objects.get(email=email)
        except SubscriberUser.DoesNotExist:
            messages.error(request, 'Bu kullanıcı mevcut değil')
            return redirect('unsubscribe')
        # Delete the user
        user.delete()
        messages.success(request, 'Abonelik Sonlandı')
        return redirect('unsubscribe')
    return render(request, 'managers/unsub.html')









def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Mesaj gönderildi')
        form = ContactForm()

    context = {'form': form}
    return render(request, 'pages/contact.html', context)



