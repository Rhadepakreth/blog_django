from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', null=True, blank=True)
    contenu = models.TextField(null=True)
    photo = models.ImageField(upload_to='articles/')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de parution")
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True,
                                verbose_name="Date de modification")
    categorie = models.CharField(max_length=200, null=True, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Commentaire par {self.auteur} sur {self.article}'
