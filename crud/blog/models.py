from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def to_slug(instance, word):
    count = 1
    slug = slugify(word)
    while instance.objects.filter(slug=slug).exists():
        slug += f"-{count}"
        count += 1
    return slug


class Friendship(models.Model):
    first = models.ForeignKey("User", related_name='first_user', on_delete=models.CASCADE)
    second = models.ForeignKey("User", related_name='second_user', on_delete=models.CASCADE)


class FriendRequest(models.Model):
    sending = models.ForeignKey("User", related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiving = models.ForeignKey("User", related_name='received_friend_requests', on_delete=models.CASCADE)


class User(AbstractUser):
    pfp = models.ImageField(upload_to="photos/%Y/%m/%d/")
    bio = models.TextField()
    nickname = models.SlugField(unique=True, max_length=255)
    friends = models.ManyToManyField("Friendship", related_name="users",null=True,blank=True)
    requests = models.ManyToManyField("FriendRequest", related_name="users",null=True,blank=True)
    favorite = models.ManyToManyField("Post", through="PostUserConnection")
    online = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)
    birthday = models.DateField(null=True, blank=True)
    preferable_cars = models.ManyToManyField("Category")
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='blogging_users',
        blank=True
    )


class PostUserConnection(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    cats = models.ManyToManyField("Category")
    tags = models.ManyToManyField("Tag")
    age_restricted = models.BooleanField(default=False)
    images = models.ManyToManyField('Image', related_name="PostImage", through="ImagePost")
    views = models.IntegerField(default = 0)
    author = models.ForeignKey("User",on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    def like_count(self):
        return Like.objects.filter(post=self).count()

    def dislike_count(self):
        return Dislike.objects.filter(post=self).count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = to_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_reverse_url(self):
        return reverse('post',kwargs={'slug': self.slug})

    def comments_count(self):
        return Comment.objects.filter(post=self).count()
class ImagePost(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image = models.ForeignKey("Image", on_delete=models.CASCADE)


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = to_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = to_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Ike(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Like(Ike):
    pass


class Dislike(Ike):
    pass


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE, blank=True, null=True)
    upcomment = models.ForeignKey("Comment", on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey("User", on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField(upload_to="media/photos/%Y/%m/%d/")


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
