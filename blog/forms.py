from django import forms
from blog.models import Comment
from .models import Contact,AuthorInfo,AuthorSocial, Category, Tags, BlogContext,BlogImage

class CommentForm(forms.ModelForm):
	body = forms.CharField(label='',
			widget=forms.Textarea(attrs={
            'class': 'px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 focus:outline-none dark:text-white dark:placeholder-gray-400 dark:bg-gray-800',
            'placeholder': 'Write your comment...'
        }), 
	        required=True)
	
    

	class Meta:
		model = Comment
		fields = ('body',)




class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'subject', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500','required': 'true'}),
            'subject': forms.TextInput(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500','required': 'true'}),
            'message': forms.Textarea(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500','required': 'true'}),
        }
		















