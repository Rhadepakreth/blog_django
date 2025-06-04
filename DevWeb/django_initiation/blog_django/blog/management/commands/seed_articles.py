import os
import random
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from faker import Faker
from blog_django.blog.models import Article

class Command(BaseCommand):
    help = 'Seeds the database with 20 surreal and humorous articles.'

    def handle(self, *args, **options):
        fake = Faker('fr_FR')
        users = User.objects.all()

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please create some users first.'))
            return

        self.stdout.write(self.style.SUCCESS('Seeding 20 articles...'))

        for _ in range(20):
            title = fake.sentence(nb_words=random.randint(5, 10), ext_word_list=[
                "licorne volante", "chaussette parlante", "nuage en fromage",
                "arbre à spaghettis", "robot poète", "canard philosophe",
                "téléportation de chaises", "pluie de bonbons", "orchestre de légumes",
                "voyage en machine à café", "le temps qui danse", "le silence qui crie"
            ]).replace('.', '')
            slug = fake.slug()
            author = random.choice(users)
            content = fake.paragraph(nb_sentences=random.randint(5, 15), ext_word_list=[
                "Dans un monde où les parapluies chantent l'opéra et les chaussettes se rebellent,",
                "Un jour, un concombre décida de devenir astronaute, défiant toutes les lois de la gravité et du bon sens.",
                "Le chat, expert en mécanique quantique, expliqua à la théière comment voyager dans le temps.",
                "Les nuages, fatigués de leur routine pluvieuse, organisèrent une grève et commencèrent à pleuvoir des confettis.",
                "Au fond de l'océan, les poissons découvrirent une bibliothèque où les livres étaient faits de bulles de savon.",
                "Le réveil sonna, mais au lieu de l'heure, il annonça la recette d'une tarte aux rêves.",
                "Les arbres, lassés de rester immobiles, inventèrent la danse du vent et se mirent à valser avec les feuilles.",
                "Un détective privé, spécialisé dans les affaires de chaussettes orphelines, suivait une piste qui le menait à la lune.",
                "La lune, en fait, était un énorme gâteau au fromage, et les étoiles, des miettes de pain d'épices.",
                "Les fourchettes et les couteaux, en pleine discussion philosophique, se demandaient si l'existence était une question de goût."
            ])
            category = random.choice([
                "Absurde", "Fantastique", "Humour", "Surréalisme", "Onirique", "Comédie"
            ])

            # Download a random image
            image_url = f"https://picsum.photos/seed/{random.randint(1, 1000)}/800/600"
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            # Save the image to a temporary file
            image_name = f"article_{slug}.jpg"
            image_path = os.path.join('media', 'articles', image_name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Create the Article object
            article = Article(
                titre=title,
                slug=slug,
                auteur=author,
                contenu=content,
                categorie=category,
                is_published=True
            )
            article.photo.name = os.path.join('articles', image_name)
            article.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully seeded article: "{title}"'))

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))