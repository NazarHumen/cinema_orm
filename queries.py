import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')
django.setup()

from movies.models import Genre, Director, Movie, Review
from django.db.models import Count, Avg, Min, Max, Q, F

# Завдання 1 - Базова вибірка
movies = Movie.objects.all()
titles = Movie.objects.values_list("title", flat=True)
print(list(titles))

# Завдання 2 — Фільтрація за рейтингом
top_movies = Movie.objects.filter(rating__gte=8.5).order_by("-rating")
for m in top_movies:
    print(m.title, m.rating)

# Завдання 3 — Пошук по тексту з Q-об'єктами
result = Movie.objects.filter(
    Q(title__icontains="Blade") | Q(title__icontains="Dark")
)
print(result)

# Завдання 4 — Фільтр через зв'язану таблицю
nolan_films = Movie.objects.filter(director__last_name="Nolan")
print(nolan_films)

# Завдання 5 — Комбінована фільтрація
combined_filtration = Movie.objects.filter(genre__name="Sci-Fi",
                                           year__gt=2015).order_by("year")
print(combined_filtration)

# Завдання 6 — exclude()
result = Movie.objects.exclude(
    Q(genre__name="Drama") | Q(genre__name="Comedy"))
for m in result:
    print(m.title, "-", m.genre.name if m.genre else "без жанру")

# Завдання 7 — Пагінація
by_rating = Movie.objects.order_by("-rating")
page1 = by_rating[:4]
page2 = by_rating[4:8]

# Завдання 8 — Кількість фільмів у кожному жанрі
genres = Genre.objects.annotate(
    movie_count=Count("movie")
).order_by("-movie_count")

for g in genres:
    print(g.name, ":", g.movie_count)

# Завдання 9 — Середній рейтинг
total_avg = Movie.objects.aggregate(avg=Avg("rating"))
print("Середнiй рейтинг:", total_avg["avg"])

directors = Director.objects.annotate(
    avg_rating=Avg("movie__rating")
).values("last_name", "avg_rating").order_by("-avg_rating")

for d in directors:
    print(d["last_name"], ":", d["avg_rating"])

# Завдання 10 — Фільми без відгуків
no_reviews = Movie.objects.filter(review__isnull=True)
print(no_reviews)

no_reviews = Movie.objects.annotate(
    review_count=Count("review")
).filter(review_count=0)
print(no_reviews)

# Завдання 11 — Масовий UPDATE
updated_count = Movie.objects.filter(rating__lt=7.8).update(is_public=False)
print(f"Оновлено: {updated_count} фiльмiв")

# Завдання 12 — Оновлення через F()
Movie.objects.filter(
    director__last_name="Tarantino"
).update(rating=F("rating") + 0.2)

# Завдання 13 — Відгуки конкретного фільму
inception = Movie.objects.get(title="Inception")
reviews = inception.review_set.all()
for r in reviews:
    print(r.score, ":", r.text)
avg_score = inception.review_set.aggregate(avg=Avg("score"))
print("Середня оцiнка:", avg_score["avg"])

# Завдання 14 — Найкращий режисер за середнім рейтингом
director = Director.objects.annotate(avg_rating=Avg("movie__rating")).order_by(
    "-avg_rating").first()
print(director.first_name, director.avg_rating)

# Завдання 15 — Власний запит: жанри, у яких більше 2 фільмів (annotate + filter)
# Цей запит знаходить усі жанри, в яких більше ніж 2 фільми.
# Спочатку використовується annotate(), щоб додати до кожного жанру поле movie_count —
# це кількість пов’язаних з ним фільмів (через Count("movie")).
# Потім через filter(movie_count__gt=2) відбираються тільки ті жанри,
# де кількість фільмів більша за 2.
# У результаті ми отримуємо список "популярних" жанрів за кількістю фільмів.
# Мені це цікаво, тому що тут поєднується агрегація (Count) і фільтрація,
# що допомагає краще зрозуміти, як працювати з базою даних у Django ORM.
# Наприклад, так можна визначати популярні категорії товарів.
popular_genres = Genre.objects.annotate(
    movie_count=Count("movie")
).filter(movie_count__gt=2)

for g in popular_genres:
    print(f"Популярний жанр: {g.name} (фільмів: {g.movie_count})")
