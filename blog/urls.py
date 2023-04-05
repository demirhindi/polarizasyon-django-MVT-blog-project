from django.urls import path


from . import views
from dashboard import views as dashview

urlpatterns = [
    
    path('', views.home, name='home'),   
    path('detail/<slug:blog_slug>/',views.detail, name='detail'),
    path('author/<slug:author_slug>/',views.author, name='author'),
    path('category/<slug:category_slug>/',views.category, name='category'),
    path('tags/<slug:tags_slug>/',views.tags, name='tags'),
    path('dashboard/', dashview.dashboard, name='dashboard'),
    path('dashboard/create_author_info/', dashview.create_author_info, name='create_author_info'),
    path('dashboard/create_social/', dashview.create_social, name='create_social'),
    path('dashboard/create_tags/', dashview.create_tags, name='create_tags'),
    path('dashboard/create_category/', dashview.create_category, name='create_category'),
    path('dashboard/create_blog/', dashview.create_blog, name='create_blog'),
    path('dashboard/create_blog_image/', dashview.create_blog_image, name='create_blog_image'),
    path('dashboard/create_carousel/', dashview.create_carousel, name='create_carousel'),

    path('dashboard/update_author_info/', dashview.update_author_info, name='update_author_info'),
    path('dashboard/update_author_social/', dashview.update_author_social, name='update_author_social'),
    path('dashboard/update_blog/<str:blog_slug>/', dashview.update_blog, name='update_blog'),
    path('dashboard/update_category/<str:category_slug>/', dashview.update_category, name='update_category'),
    path('dashboard/update_tags/<str:tag_slug>/', dashview.update_tags, name='update_tags'),
    path('dashboard/update_blog_image/<int:image_id>/', dashview.update_blog_image, name='update_blog_image'),

    path('dashboard/update_carousel/<int:id>/', dashview.update_carousel, name='update_carousel'),


    path('dashboard/blog_images/<str:slug>/', dashview.blog_images, name='blog_images'),
    path('dashboard/tags/', dashview.tags, name='tags'),
    path('dashboard/carousel/', dashview.carousel, name='carousel'),
    path('dashboard/categories/', dashview.categories, name='categories'),

    path('dashboard/delete_blog/<int:id>/', dashview.delete_blog, name='delete_blog'),
    path('dashboard/delete_blog_image/<int:id>/', dashview.delete_blog_image, name='delete_blog_image'),
    path('dashboard/delete_tag/<int:id>/', dashview.delete_tag, name='delete_tag'),
    path('dashboard/delete_category/<int:id>/', dashview.delete_category, name='delete_category'),
    path('dashboard/delete_carousel/<int:id>/', dashview.delete_carousel, name='delete_carousel'),


     
     


    

    path('contact/', views.contact, name='contact'),
    path('search/',views.search, name='search'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    
   

]