from django import forms

from blog.models import Contact,AuthorInfo,AuthorSocial, Category, Tags, BlogContext,BlogImage,Carousel




class AuthorInfoForm(forms.ModelForm):
    
    class Meta:
         
        model = AuthorInfo
        fields = ['birthyear', 'bio', 'photo']
        widgets = {
            'birthyear': forms.TextInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
        }


class AuthorSocialForm(forms.ModelForm):
    
    class Meta:
         
        model = AuthorSocial
        fields = ['title', 'url', 'alias']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
            'url': forms.TextInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
            'alias': forms.TextInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
        }
    


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
            
        }


class TagsForm(forms.ModelForm):
    
    class Meta:
        model = Tags
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
        }


class BlogContextForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), widget=forms.CheckboxSelectMultiple)
    author = forms.ModelMultipleChoiceField(queryset=AuthorInfo.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = BlogContext
        fields = ['title', 'category', 'tags', 'author', 'context', 'thumbnail', 'is_published']
        widgets = {
            'context': forms.Textarea(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
        }


class BlogImageForm(forms.ModelForm):
    blog_context = forms.ModelChoiceField(queryset=BlogContext.objects.all(), widget=forms.Select)

    class Meta:
        model = BlogImage
        fields = ['title', 'blog_context', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none','required': 'true'}),
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }




class CarouselForm(forms.ModelForm):
    
    class Meta:
         
        model = Carousel
        fields = ['title', 'url', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
            'url': forms.Textarea(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-100 mt-2 py-3 px-3 rounded-lg bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 dark:text-gray-50 font-semibold focus:border-blue-500 focus:outline-none',
                'required': 'true'
            }),
        }


