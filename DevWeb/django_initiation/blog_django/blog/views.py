from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login
from django.shortcuts import render
from .models import Article, Comment, Profile # Ajout de l'importation de Profile
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect



class LegalPageView(TemplateView):
    template_name = 'blog/legal.html'
    page_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_type = self.page_type
        if page_type == 'mentions-legales':
            context['title'] = 'Mentions Légales'
            context['content'] = """
            <h2>Éditeur du site</h2>
            <p>Nom de l'entreprise : [Votre Nom/Nom de l'entreprise]</p>
            <p>Forme juridique : [SARL, SAS, Auto-entreprise, etc.]</p>
            <p>Adresse : [Votre adresse complète]</p>
            <p>Téléphone : [Votre numéro de téléphone]</p>
            <p>Email : [Votre adresse email]</p>
            <p>Numéro d'immatriculation (SIRET/RCS) : [Votre numéro SIRET/RCS]</p>

            <h2>Hébergeur</h2>
            <p>Nom de l'hébergeur : [Nom de l'hébergeur]</p>
            <p>Adresse : [Adresse de l'hébergeur]</p>
            <p>Téléphone : [Numéro de téléphone de l'hébergeur]</p>

            <h2>Propriété intellectuelle</h2>
            <p>L'ensemble de ce site relève de la législation française et internationale sur le droit d'auteur et la propriété intellectuelle. Tous les droits de reproduction sont réservés, y compris pour les documents téléchargeables et les représentations iconographiques et photographiques.</p>

            <h2>Données personnelles</h2>
            <p>Conformément à la loi Informatique et Libertés du 6 janvier 1978 modifiée, vous disposez d'un droit d'accès, de rectification et de suppression des données vous concernant. Pour l'exercer, adressez-vous à [Votre adresse email].</p>

            <h2>Limitation de responsabilité</h2>
            <p>L'éditeur du site ne saurait être tenu pour responsable des erreurs rencontrées sur le site, problèmes techniques, interprétation des informations publiées et conséquences de leur utilisation.</p>
            """
        elif page_type == 'politique-confidentialite':
            context['title'] = 'Politique de Confidentialité'
            context['content'] = """
            <h2>Collecte des données personnelles</h2>
            <p>Nous collectons les informations que vous nous fournissez directement, par exemple lorsque vous créez un compte, vous inscrivez à notre newsletter, participez à un sondage ou nous contactez. Ces informations peuvent inclure votre nom, adresse email, numéro de téléphone, etc.</p>

            <h2>Utilisation des données</h2>
            <p>Les données collectées sont utilisées pour :</p>
            <ul>
                <li>Fournir, exploiter et maintenir notre site web</li>
                <li>Améliorer, personnaliser et développer notre site web</li>
                <li>Comprendre et analyser la façon dont vous utilisez notre site web</li>
                <li>Développer de nouveaux produits, services, fonctionnalités et fonctions</li>
                <li>Communiquer avec vous, directement ou par l'intermédiaire de l'un de nos partenaires, y compris pour le service client, pour vous fournir des mises à jour et d'autres informations relatives au site web, et à des fins de marketing et de promotion</li>
                <li>Vous envoyer des emails</li>
                <li>Détecter et prévenir la fraude</li>
            </ul>

            <h2>Partage des données</h2>
            <p>Nous ne partageons pas vos informations personnelles avec des tiers, sauf dans les cas suivants :</p>
            <ul>
                <li>Avec votre consentement</li>
                <li>Pour se conformer à une obligation légale</li>
                <li>Pour protéger et défendre nos droits ou notre propriété</li>
            </ul>

            <h2>Sécurité des données</h2>
            <p>Nous mettons en œuvre des mesures de sécurité techniques et organisationnelles appropriées pour protéger la sécurité de vos données personnelles.</p>

            <h2>Vos droits</h2>
            <p>Conformément au Règlement Général sur la Protection des Données (RGPD), vous disposez des droits suivants :</p>
            <ul>
                <li>Droit d'accès : obtenir la confirmation que vos données sont traitées et, le cas échéant, y accéder.</li>
                <li>Droit de rectification : demander la correction des données inexactes.</li>
                <li>Droit à l'effacement : demander la suppression de vos données.</li>
                <li>Droit à la limitation du traitement : demander la suspension du traitement de vos données.</li>
                <li>Droit à la portabilité : recevoir vos données dans un format structuré et couramment utilisé.</li>
                <li>Droit d'opposition : vous opposer au traitement de vos données.</li>
            </ul>
            <p>Pour exercer ces droits, veuillez nous contacter à [Votre adresse email].</p>

            <h2>Modifications de cette politique</h2>
            <p>Nous pouvons mettre à jour notre Politique de Confidentialité de temps à autre. Nous vous informerons de tout changement en publiant la nouvelle Politique de Confidentialité sur cette page.</p>
            """
        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Article.objects.values_list('categorie', flat=True).distinct()
        return context


class ArticleCategoryView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category = self.kwargs['slug']
        return Article.objects.filter(categorie=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Article.objects.values_list('categorie', flat=True).distinct()
        context['current_category'] = self.category
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        comments = article.comments.all()
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['categories'] = Article.objects.values_list('categorie', flat=True).distinct()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = self.object
            new_comment.auteur = request.user
            new_comment.save()
            return redirect(reverse('blog:article_detail', kwargs={'slug': self.object.slug}))
        else:
            # If the form is not valid, re-render the page with errors
            context = self.get_context_data(**kwargs)
            context['comment_form'] = comment_form
            return self.render_to_response(context)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['contenu']
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'slug': self.object.article.slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.auteur


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'slug': self.object.article.slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.auteur

from django.contrib.auth.views import LoginView
from django.contrib import messages
from .profile_forms import UserUpdateForm, ProfileUpdateForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        # Authentifier l'utilisateur mais ne pas encore le connecter
        user = form.get_user()
        
        # Vérifier si l'utilisateur a un profil, sinon en créer un
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
        
        # Rafraîchir l'objet utilisateur pour s'assurer que le profil est chargé
        user.refresh_from_db()

        # La méthode parente gérera la connexion de l'utilisateur et la redirection
        return super().form_valid(form)

def register_view(request):
    """
    Gère l'inscription des nouveaux utilisateurs.
    Si la requête est POST et que le formulaire est valide, un nouvel utilisateur est créé et connecté.
    Sinon, un formulaire vide est affiché.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username} !')
            login(request, user)
            return redirect('blog:article_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('blog:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'blog/profile.html', context)

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('blog:article_list') # Rediriger vers la page d'accueil après suppression
    return render(request, 'blog/delete_account_confirm.html')
