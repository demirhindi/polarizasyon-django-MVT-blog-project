from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from django.urls import reverse
from .validators import file_size

from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from accounts.models import SubscriberUser
from django.conf import settings


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150,blank=True,unique=True)
    slug = models.SlugField(max_length=150,unique=True,blank=True)
    

    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

    def get_url(self):
        return reverse('category',kwargs={"category_slug":self.slug})

    def __str__(self):
        return self.title
    


class Tags(models.Model):
    title = models.CharField(max_length=150,blank=True,unique=True)
    slug = models.SlugField(max_length=150,unique=True,blank=True)
    

    class Meta:
        verbose_name='tag'
        verbose_name_plural='tags'

    def get_url(self):
        return reverse('tag',kwargs={"tag_slug":self.slug})

    def __str__(self):
        return self.title
    


class AuthorInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150,blank=True)
    birthyear= models.CharField(max_length=150,blank=True)
    bio=models.TextField(max_length=40000,blank=True)
    photo = models.ImageField(upload_to="author/profile",blank=True,default="carousel/Images/no-image.png")    
    

    class Meta:
        verbose_name='AuthorInfo'
        verbose_name_plural='AuthorsInfos'

    def get_url(self):
        return reverse('author',kwargs={"author_slug":self.slug})

    def __str__(self):
        return self.user.username
    
    @property
    def social(self):
        return self.social
    
    @property
    def authors(self):
        return self.authors
    

class AuthorSocial(models.Model):
    title = models.CharField(max_length=150,blank=True)
    user = models.ForeignKey(AuthorInfo,on_delete=models.CASCADE,related_name="social")
    url = models.CharField(max_length=1500,blank=True)
    alias= models.CharField(max_length=150,blank=True) 
    
    

    class Meta:
        verbose_name='AuthorSocial'
        verbose_name_plural='AuthorsSocials'   

    def __str__(self):
        return self.title
    

    


class BlogContext(models.Model):
    title = models.CharField(max_length=150,blank=True, unique=True)  
    slug = models.SlugField(max_length=150,blank=True)  
    category=models.ManyToManyField(Category,related_name="categories")
    tags=models.ManyToManyField(Tags,related_name="tags")
    author=models.ManyToManyField(AuthorInfo,related_name="authors")
    created_at = models.DateField(auto_now_add=True)
    created_field = models.DateTimeField(auto_now_add=True,blank=True)
    is_published=models.BooleanField(default=True)
    context=models.TextField(max_length=100000000,blank=True)
    thumbnail = models.ImageField(upload_to="blog/thumbnails",blank=True,default="carousel/Images/no-image.png")       
    click_count = models.PositiveIntegerField(default=0)


    def get_url(self):
        return reverse('detail',kwargs={"blog_slug":self.slug})

    def __str__(self):
        return self.title
    
   
    
    def save(self, *args, **kwargs):
        self.click_count += 1
        super(BlogContext, self).save(*args, **kwargs)

    



class BlogImage(models.Model):
    title = models.CharField(max_length=150,blank=True)
    user = models.ForeignKey(BlogContext,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog/Images",blank=True,default="carousel/Images/no-image.png")    
    
    

    class Meta:
        verbose_name='BlogImage'
        verbose_name_plural='BlogImages'   

    def __str__(self):
        return self.title





class Comment(models.Model):

    post = models.ForeignKey(BlogContext, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=20000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

        
        
	


class Contact(models.Model):
    email = models.CharField(max_length=150,blank=True)  
    subject = models.CharField(max_length=300,blank=True)  
    message = models.TextField(max_length=10000,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email  
    
    class Meta:
        ordering = ['-id']
        get_latest_by = 'id'

    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)
        # Delete old contacts and keep only the latest 10 contacts
        Contact.objects.all().exclude(id__in=Contact.objects.order_by('-id')[:10].values_list('id', flat=True)).delete()


class Carousel(models.Model):
    title = models.CharField(max_length=150,blank=True)
    url = models.CharField(max_length=350,blank=True)
    image = models.ImageField(upload_to="carousel/Images",blank=True, default="carousel/Images/no-image.png")   


    def __str__(self):
        return self.title  
    
    def save(self, *args, **kwargs):
        super(Carousel, self).save(*args, **kwargs)
        # Delete old contacts and keep only the latest 10 contacts
        Carousel.objects.all().exclude(id__in=Carousel.objects.order_by('-id')[:6].values_list('id', flat=True)).delete()





def pre_save_category(sender,instance,*args, **kwargs):
    if instance.title and (not instance.slug or instance.title != instance.slug):
        instance.slug = slugify(instance.title)
pre_save.connect(pre_save_category,sender=Category)


def pre_save_tag(sender,instance,*args, **kwargs):
    if instance.title and (not instance.slug or instance.title != instance.slug):
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_tag,sender=Tags)


def pre_save_blogcontext(sender,instance,*args, **kwargs):
    if instance.title and (not instance.slug or instance.title != instance.slug):
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_blogcontext,sender=BlogContext)

def pre_save_authorinfo(sender,instance,*args, **kwargs):
    if instance.user.username and (not instance.slug or instance.user.username != instance.slug):
        instance.slug = slugify(instance.user.username)

pre_save.connect(pre_save_authorinfo,sender=AuthorInfo)



@receiver(post_save, sender=BlogContext)
def notify_users(sender, instance, created, **kwargs):
    if created:
        users = SubscriberUser.objects.filter(is_active=True)
        email_list = [user.email for user in users]
        subject = 'Yeni bir blog yazısı eklendi!'
        message = f"{instance.title} başlıklı yeni bir blog yazısı yayınlandı! Anasayfaya dönmek için: {settings.SITE_URL}\n\nAboneliğinizden çıkmak için lütfen bu bağlantıya tıklayın: {settings.SITE_URL}unsubscribe/"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, email_list, fail_silently=False)
        print('mail sended')