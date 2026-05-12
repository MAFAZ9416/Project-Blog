#----> Import the necessary modules 
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

#----> Create your models here.

#----> Create a Category module
class Categorys(models.Model):

    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


#----> Create a Post module
class Post(models.Model):

    title = models.CharField(max_length = 100)
    content = models.TextField()
    img_url = models.ImageField(null = True, upload_to = "posts/images")
    created_at = models.DateTimeField(auto_now_add = True)
    slug = models.SlugField(unique = True)
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    is_published = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # We use this property to get the full url of the image and we check if the url is start with http or https then we return the url otherwise we return the url of the image field and mentioned the decorators @property
    @property
    def formatted_img_url(self) :
        url = self.img_url if self.img_url.__str__().startswith(('http://', 'https://')) else self.img_url.url
        return url

    def __str__(self):

        return self.title
    

#----> Create an About module
class About(models.Model):

    content = models.TextField()

    