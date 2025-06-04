from django.contrib import admin
from blog_django.blog.models import Article, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'article', 'created_at')
    list_filter = ('auteur', 'created_at')
    search_fields = ('auteur__username', 'article__titre', 'contenu')

@admin.register(Article)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'created_at', 'updated_at', 'longueur_contenu')
    list_filter = ('auteur', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at', )
    search_fields = ('contenu', 'titre', 'auteur' )
    fieldsets = (
        ("informations", {
            'fields': ('titre', 'slug', 'auteur', 'contenu', 'photo', 'categorie', 'is_published')
        }),
    )
    

    def nom_auteur(self, obj):
        if obj.auteur:
            return obj.auteur.username
        return 'Inconnu'
    
    def longueur_contenu(self, obj):
        return str(len(obj.contenu)) + ' caractères'

    
    nom_auteur.short_description = 'Auteur'
    longueur_contenu.short_description = 'Longueur'