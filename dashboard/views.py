from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AuthorInfoForm,AuthorSocialForm, TagsForm,CategoryForm,BlogContextForm,BlogImageForm,CarouselForm
from django.shortcuts import redirect

from blog.models import Contact, AuthorInfo,BlogContext,BlogImage,AuthorSocial,Category,Tags,Carousel
from accounts.models import SubscriberUser
from django.contrib import messages


@login_required(login_url='login')
def dashboard(request):
    if request.user.is_author:
        authors=AuthorInfo.objects.filter(user=request.user)    
        contacts=Contact.objects.all().order_by("-id")
        subscribers=SubscriberUser.objects.all().order_by("-id")    
        blogs=BlogContext.objects.all().order_by('-created_field')

        context= {   
            "contacts":contacts,
            "subscribers":subscribers,
            'authors': authors,
            'blogs':blogs,           
        }
        return render(request,'managers/dashboard.html',context)
    else:
        return render(request,'managers/403Forbidden.html')
    

@login_required(login_url='login')
def create_author_info(request):
    if request.user.is_author:
        if request.method == 'POST':
            form = AuthorInfoForm(request.POST, request.FILES)
            if form.is_valid():
                author = form.save(commit=False)
                author.user = request.user
                author.save()
                messages.success(request, 'Author Info has created')
                return redirect('dashboard')
        else:
            form = AuthorInfoForm()

        context = {'form': form}
        return render(request, 'create/create_author_info.html', context)
    else:
        return render(request,'managers/403Forbidden.html')


@login_required(login_url='login')
def create_social(request):
    if request.user.is_author:
        if request.method == 'POST':
            form = AuthorSocialForm(request.POST, request.FILES)
            myauth=AuthorInfo.objects.get(user=request.user)
            if form.is_valid():
                author = form.save(commit=False)
                author.user = myauth
                author.save()
                messages.success(request, 'Social Info has created')
                return redirect('dashboard')
        else:
            form = AuthorSocialForm()

        context = {'form': form}
        return render(request, 'create/create_social.html', context)
    else:
        return render(request,'managers/403Forbidden.html')


@login_required(login_url='login')
def create_category(request):
    if request.user.is_author:
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has created')
            return redirect('dashboard')
        context = {'form': form}
        return render(request, 'create/create_category.html', context)
    else:
        return render(request,'managers/403Forbidden.html')

@login_required(login_url='login')
def create_tags(request):
    if request.user.is_author:
        form = TagsForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'tag has created')
            return redirect('dashboard')
        context = {'form': form}
        return render(request, 'create/create_tags.html', context)
    else:
        return render(request,'managers/403Forbidden.html')

@login_required(login_url='login')
def create_blog(request):
    if request.user.is_author:
        if request.method == "POST":
            form = BlogContextForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.save()
                form.save_m2m()  # Save many-to-many fields (categories and tags)
                blog.author.set([request.user.authorinfo])  # Add the author using the many-to-many relationship
                messages.success(request, 'Blog Context has created')
                return redirect('dashboard')
        else:
            form = BlogContextForm()
        return render(request, 'create/create_context.html', {'form': form})
    else:
        return render(request,'managers/403Forbidden.html')


@login_required(login_url='login')
def create_blog_image(request):
    if request.user.is_author:
        if request.method == 'POST':
            form = BlogImageForm(request.POST, request.FILES)
            if form.is_valid():
                blog_image = form.save(commit=False)
                blog_slug = form.cleaned_data['blog_context'].slug
                blog_context = BlogContext.objects.get(slug=blog_slug)
                images = request.FILES.getlist('image')
                for img in images:
                    BlogImage.objects.create(
                        title=form.cleaned_data['title'],
                        user=blog_context,
                        image=img,
                    )
                messages.success(request, 'Images has created')
                return redirect('dashboard')
        else:
            form = BlogImageForm()
        return render(request, 'create/create_blog_image.html', {'form': form})
    
    else:
        return render(request,'managers/403Forbidden.html')


@login_required(login_url='login')
def blog_images(request, slug):
    blog = get_object_or_404(BlogContext, slug=slug)
    author_info = blog.author.first() 
    if request.user.is_authenticated and request.user.id == author_info.user_id:    
        blog_context = get_object_or_404(BlogContext, slug=slug)
        blog_images = BlogImage.objects.filter(user=blog_context)
        return render(request, 'update/blog_images.html', {'blog_context': blog_context, 'blog_images': blog_images})
    else:
        return render(request,'managers/403Forbidden.html')


@login_required(login_url='login')
def update_blog_image(request, image_id):
    if request.user.is_author:
        blog_image = get_object_or_404(BlogImage, id=image_id)
        if request.method == 'POST':
            form = BlogImageForm(request.POST, request.FILES, instance=blog_image)
            if form.is_valid():
                form.save()
                messages.success(request, 'blog image has been updated.')
                return redirect('dashboard')
        else:
            form = BlogImageForm(instance=blog_image)
        return render(request, 'update/update_blog_image.html', {'form': form})
    else:
        return render(request,'managers/403Forbidden.html')


@login_required(login_url='login')
def update_author_info(request):
    if request.user.is_author:
        author_info = get_object_or_404(AuthorInfo, user=request.user)
        
        if request.method == 'POST':
            form = AuthorInfoForm(request.POST, request.FILES, instance=author_info)
            if form.is_valid():
                form.save()
                messages.success(request, 'Author  information has been updated.')
                return redirect('dashboard')
        else:
            form = AuthorInfoForm(instance=author_info)
            
        return render(request, 'update/update_author_info.html', {'form': form})
    else:
        return render(request,'managers/403Forbidden.html')

@login_required(login_url='login')
def update_author_social(request):
    if request.user.is_author:
        user = request.user
        socials = user.authorinfo.social.all()

        if request.method == 'POST':
            social_id = request.POST.get('social')
            social = get_object_or_404(AuthorSocial, pk=social_id, user=user.authorinfo)
            form = AuthorSocialForm(request.POST, instance=social)
            if form.is_valid():
                form.save()
                messages.success(request, 'Author social information has been updated.')
                return redirect('dashboard')
        else:
            form = AuthorSocialForm()
        
        context = {
            'form': form,
            'socials': socials,
        }
        
        return render(request, 'update/update_author_social.html', context)
    else:
        return render(request,'managers/403Forbidden.html')



@login_required(login_url='login')
def update_blog(request, blog_slug):
    blog = get_object_or_404(BlogContext, slug=blog_slug)
    author_info = blog.author.first() 
    if request.user.is_authenticated and request.user.id == author_info.user_id:
        blog = get_object_or_404(BlogContext, slug=blog_slug)

        if request.method == "POST":
            form = BlogContextForm(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                form.save()
                messages.success(request, 'Blog post updated successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'There was an error while updating the blog post.')
        else:
            form = BlogContextForm(instance=blog)

        context = {
            'form': form,
            'blog': blog
        }

        return render(request, 'update/update_blog.html', context)
    else:
        return render(request,'managers/403Forbidden.html')


@login_required(login_url='login')
def categories(request):
    if request.user.is_author:
        cats=Category.objects.all()
        context = {'cats': cats}
        return render(request, 'update/categories.html', context)
    else:
        return render(request,'managers/403Forbidden.html')



@login_required(login_url='login')
def update_category(request, category_slug):
    if request.user.is_author:
        category = get_object_or_404(Category, slug=category_slug)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category updated successfully.')
                return redirect('dashboard')
        else:
            form = CategoryForm(instance=category)
        context = {'form': form}
        return render(request, 'update/update_category.html', context)
    else:
        return render(request,'managers/403Forbidden.html')


@login_required(login_url='login')
def tags(request):
    if request.user.is_author:
        tags=Tags.objects.all()
        context = {'tags': tags}
        return render(request, 'update/tags.html', context)
    else:
        return render(request,'managers/403Forbidden.html')

@login_required(login_url='login')
def update_tags(request, tag_slug):
    if request.user.is_author:
        tag = get_object_or_404(Tags, slug=tag_slug)

        if request.method == 'POST':
            form = TagsForm(request.POST, instance=tag)
            if form.is_valid():
                form.save()
                messages.success(request, f"{tag.title} tag updated successfully.")
                return redirect('dashboard')
        else:
            form = TagsForm(instance=tag)

        return render(request, 'update/update_tags.html', {'form': form})
    else:
        return render(request,'managers/403Forbidden.html')


@login_required(login_url='login')
def delete_category(request, id):
    if request.user.is_author:
        category = get_object_or_404(Category, id=id)
        category.delete()
        messages.success(request, 'Category has deleted')
        return redirect('dashboard')
    else:
        return render(request,'managers/403Forbidden.html')

@login_required(login_url='login')
def delete_tag(request, id):
    if request.user.is_author:
        tag = get_object_or_404(Tags, id=id)
        tag.delete()
        messages.success(request, 'tag has deleted')
        return redirect('dashboard')
    else:
        return render(request,'managers/403Forbidden.html')

@login_required(login_url='login')
def delete_author(request, id):
    if request.user.is_author:
        author = get_object_or_404(AuthorInfo, id=id)
        author.delete()
        return redirect('author-list')
    else:
        return render(request,'managers/403Forbidden.html')





@login_required(login_url='login')
def delete_blog(request, id):
    blog = get_object_or_404(BlogContext, id=id)
    author_info = blog.author.first() 
    if request.user.is_authenticated and request.user.id == author_info.user_id:
        blog = get_object_or_404(BlogContext, id=id)
        blog.delete()
        messages.success(request, 'Blog Context has deleted')
        return redirect('dashboard')
    else:
        return render(request,'managers/403Forbidden.html')

@login_required(login_url='login')
def delete_blog_image(request, id):
    if request.user.is_author:
        blog_image = get_object_or_404(BlogImage, id=id)
        blog_image.delete()
        messages.success(request, 'Blog Image has deleted')
        return redirect('dashboard')
    else:
        return render(request,'managers/403Forbidden.html')



@login_required(login_url='login')
def carousel(request):
    if request.user.is_author:
        carousel=Carousel.objects.all()
        context = {'carousel': carousel}
        return render(request, 'update/carousel.html', context)
    else:
        return render(request,'managers/403Forbidden.html')  

@login_required(login_url='login')
def create_carousel(request):
    if request.user.is_author:
        if request.method == 'POST':
            form = CarouselForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'carousel item has created')
                return redirect('dashboard')
        else:
            form = CarouselForm()
        return render(request, 'create/create_carousel.html', {'form': form})
    else:
        return render(request,'managers/403Forbidden.html')
    


@login_required(login_url='login')
def update_carousel(request, id):
    if request.user.is_author:
        carousel = get_object_or_404(Carousel, id=id)

        if request.method == 'POST':
            form = CarouselForm(request.POST, instance=carousel)
            if form.is_valid():
                form.save()
                messages.success(request, f"{carousel.title} carousel updated successfully.")
                return redirect('dashboard')
        else:
            form = CarouselForm(instance=carousel)

        return render(request, 'update/update_tags.html', {'form': form})
    else:
        return render(request,'managers/403Forbidden.html')
    

@login_required(login_url='login')
def delete_carousel(request, id):
    if request.user.is_author:
        author = get_object_or_404(Carousel, id=id)
        author.delete()
        messages.success(request, " carousel item has deleted")
        return redirect('dashboard')
    else:
        return render(request,'managers/403Forbidden.html')


   
