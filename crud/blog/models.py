from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


def to_slug(instance, word):
    count = 1
    slug = slugify(word)
    while instance.objects.filter(slug=slug).exists():
        slug += f"-{count}"
        count += 1
    return slug


class Friendship(models.Model):
    first = models.ForeignKey("User", on_delete=models.CASCADE)
    second = models.ForeignKey("User", on_delete=models.CASCADE)


class FriendRequest(models.Model):
    sending = models.ForeignKey("User", on_delete=models.CASCADE)
    receiving = models.ForeignKey("User", on_delete=models.CASCADE)


class User(AbstractUser):
    pfp = models.ImageField(upload_to="media/photos/%Y/%m/%d/")
    nickname = models.SlugField(unique=True, max_length=255)
    friends = models.ManyToManyField("Friendship")
    requests = models.ManyToManyField("FriendRequest")
    favorite = models.ManyToManyField("Post", through="PostUserConnection")
    online = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now_add=True)
    birthday = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = to_slug(self, self.username)
        super().save(*args, **kwargs)


class PostUserConnection(models.Model):
    user = models.ForeignKey('User')
    post = models.ForeignKey('Post')
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

    def __str__(self):
        return self.title

    def like_count(self):
        return Like.objects.count(post=self)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = to_slug(self, self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = to_slug(self, self.title)
        super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = to_slug(self, self.title)
        super().save(*args, **kwargs)


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
    post = models.ForeignKey("Post", on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField(upload_to="media/photos/%Y/%m/%d/")
    post = models.ForeignKey("Post")
