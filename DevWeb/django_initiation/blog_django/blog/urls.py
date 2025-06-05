from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCategoryView, LegalPageView, CommentUpdateView, CommentDeleteView, register_view

app_name = 'blog'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('category/<path:slug>/', ArticleCategoryView.as_view(), name='article_category'),
    path('mentions-legales/', LegalPageView.as_view(page_type='mentions-legales'), name='mentions_legales'),
    path('politique-confidentialite/', LegalPageView.as_view(page_type='politique-confidentialite'), name='politique_confidentialite'),
    path('article/<slug:article_slug>/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('article/<slug:article_slug>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('register/', register_view, name='register'),
]