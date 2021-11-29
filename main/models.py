from django.db import models

from account.models import MyUser

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='problems')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CodeImage(models.Model):
    image = models.ImageField(upload_to='images')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='images')


class Reply(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    image = models.ImageField(upload_to='replies')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='replies')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.body[:20]}'


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=False)

    def __str__(self):
        return self.name


class Department(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='hotel')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='hotel')
    title = models.CharField(max_length=225)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DepartmentImage(models.Model):
    image = models.ImageField(upload_to='departments', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('-created', )


class Likes(models.Model):
    likes = models.BooleanField(default=False)
    post = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')



    def __str__(self):
        return str(self.likes)


class Rating(models.Model):
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return str(self.rating)

class Favorite(models.Model):
    post = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favourites')
    favorite = models.BooleanField(default=True)



