from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, Textarea

class User(AbstractUser):
    pass

class Follow(models.Model):
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "following")
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "followed")

    def __str__(self):
        return f'{self.following} follows {self.followed}'

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name ="posts")
    content = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", blank=True, related_name="liked")

    def __str__(self):
        return f'{self.user} posted "{self.content}"'

    def serialize(self):
        return {
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [user.username for user in self.likes.all()]
        }

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'cols': 20, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control new-post'