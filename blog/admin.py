from django.contrib import admin

# Register your models here.
from .models import AuthorInfo,AuthorSocial,BlogContext,Category,Tags,BlogImage,Comment,Contact,Carousel

admin.site.register(AuthorSocial)
admin.site.register(Category)

admin.site.register(AuthorInfo)
admin.site.register(BlogContext)
admin.site.register(Tags)
admin.site.register(BlogImage)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Carousel)