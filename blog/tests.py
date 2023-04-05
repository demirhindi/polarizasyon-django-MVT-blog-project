from django.test import TestCase, Client
from .models import BlogContext, Category, Tags, AuthorInfo
from django.urls import reverse

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title='Test Category', slug='This is a test category')

    def test_title_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_slug_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_title_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('title').max_length
        self.assertEquals(max_length, 150)

    def test_object_name_is_title(self):
        category = Category.objects.get(id=1)
        expected_object_name = f'{category.title}'
        self.assertEquals(expected_object_name, str(category))

    def test_category_slug(self):
        category = Category.objects.get(id=1)
        expected_slug = 'test-category'
        self.assertEquals(expected_slug, category.slug)



class TagModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Tags.objects.create(title='Test Tag', slug='test-tag')

    def test_title(self):
        tag = Tags.objects.get(id=1)
        expected_title = tag.title
        self.assertEquals(expected_title, 'Test Tag')

    def test_slug(self):
        tag = Tags.objects.get(id=1)
        expected_slug = tag.slug
        self.assertEquals(expected_slug, 'test-tag')



class BlogContextModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='test_category', slug='test_category')
        self.tag = Tags.objects.create(title='test_tag', slug='test-tag')
        

        self.blog = BlogContext.objects.create(title='Test Blog', slug='test-blog', context='This is a test blog context')
        self.blog.category.add(self.category)
        self.blog.tags.add(self.tag)
        

    def test_blog_title(self):
        blog = BlogContext.objects.get(id=1)
        expected_title = f'{blog.title}'
        self.assertEquals(expected_title, str(blog))

    def test_blog_url(self):
        blog = BlogContext.objects.get(id=1)
        expected_url = reverse('detail', kwargs={'blog_slug': blog.slug})
        self.assertEquals(expected_url, blog.get_url())

    def test_blog_category(self):
        blog = BlogContext.objects.get(id=1)
        expected_category = f'{self.category}'
        self.assertEquals(expected_category, str(blog.category.first()))

    def test_blog_tag(self):
        blog = BlogContext.objects.get(id=1)
        expected_tag = f'{self.tag}'
        self.assertEquals(expected_tag, str(blog.tags.first()))








class DetailViewTestCase(TestCase):

    def setUp(self):
        # Test için kullanılacak verileri burada oluşturun
        self.blog = BlogContext.objects.create(
            title='Test Blog',
           
            slug='test-blog'
        )

    def test_detail_view(self):
        # Test senaryosunu burada yazın
        client = Client()

        # Blog detay sayfasını test edeceğimiz için bu URL'yi kullanıyoruz
        url = reverse('detail', args=[self.blog.slug])
        
        # client.get() yöntemi ile URL'ye GET isteği gönderiyoruz
        response = client.get(url)

        # HTTP 200 OK yanıtı aldığımızı doğrulayın
        self.assertEqual(response.status_code, 200)

        # Blog başlığının sayfada göründüğünü doğrulayın
        self.assertContains(response, self.blog.title)

      