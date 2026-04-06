# Django Cinema Project

Цей проєкт є навчальним прикладом роботи з Django ORM на базі бази даних
фільмів. Він включає моделі для жанрів, режисерів, фільмів та відгуків, а також
приклади складних запитів.

## Використані технології

Проєкт базується на наступних основних бібліотеках:

- **Django 6.0.3** — основний фреймворк.
- **psycopg2-binary 2.9.11** — адаптер для роботи з PostgreSQL.
- **python-dotenv 1.2.2** — для керування змінними середовища.

## Як запустити проєкт

### 1. Клонування репозиторію та підготовка

Переконайтеся, що у вас встановлено Python (рекомендовано 3.10+).

### 2. Створення віртуального середовища

```bash
python -m venv venv
# Активуйте віртуальне середовище:
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

> **Примітка для користувачів macOS:** На комп'ютерах з чипами Apple Silicon (M1/M2/M3) для коректного встановлення `psycopg2-binary` може знадобитися встановлений PostgreSQL у системі. Ви можете встановити його за допомогою Homebrew: `brew install postgresql`.

### 4. Налаштування середовища

Проєкт використовує змінні середовища через файл `.env`.

1. Скопіюйте приклад файлу налаштувань:
   ```bash
   # macOS / Linux / Windows PowerShell:
   cp .env.example .env

   # Windows Command Prompt (CMD):
   copy .env.example .env
   ```
2. Відкрийте файл `.env` та заповніть його власними даними (наприклад,
   параметри підключення до бази даних).

Обов'язкові змінні:

- `SECRET_KEY`: Секретний ключ Django.
- `DEBUG`: Режим розробки (`true` або `false`).
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Налаштування бази
  даних PostgreSQL.

Приклад налаштувань (мій приклад "Supabase"):

```env
SECRET_KEY='django-dhjfsgjgfdgsdjfgsjfgsdjf37473fhdg'
DEBUG=true
ALLOWED_HOSTS=[]

DB_NAME=postgres
DB_USER=postgres.dsjfhdsjhfkjhsjfkd
DB_PASSWORD=password
DB_HOST=aws-1-eu-west-4.pooler.supabase.com
DB_PORT=6543
```

### 5. Застосування міграцій

```bash
python manage.py migrate
```

### 6. Запуск сервера розробки

```bash
python manage.py runserver
```

Тепер проєкт доступний за адресою `http://127.0.0.1:8000/`.

### 7. Запуск прикладів запитів (ORM)

Ви можете запустити скрипт `queries.py` для перегляду результатів виконання
різних ORM запитів:

```bash
python queries.py
```

---

## Опис моделей

Проєкт складається з наступних моделей у додатку `movies`:

### 1. Genre (Жанр)

Зберігає назви кіножанрів.

- `name` (CharField): Назва жанру (наприклад, Sci-Fi, Drama).

### 2. Director (Режисер)

Зберігає інформацію про режисерів.

- `first_name` (CharField): Ім'я.
- `last_name` (CharField): Прізвище.
- `birth_year` (IntegerField): Рік народження (може бути порожнім).
- `country` (CharField): Країна (може бути порожньою).

### 3. Movie (Фільм)

Основна модель фільму.

- `title` (CharField): Назва фільму.
- `year` (IntegerField): Рік випуску.
- `rating` (DecimalField): Рейтинг фільму (max 10.0).
- `duration` (IntegerField): Тривалість у хвилинах.
- `is_public` (BooleanField): Прапор публічності.
- `genre` (ForeignKey): Зв'язок з моделлю `Genre` (Many-to-One).
- `director` (ForeignKey): Зв'язок з моделлю `Director` (Many-to-One).

### 4. Review (Відгук)

Відгуки користувачів до фільмів.

- `movie` (ForeignKey): Зв'язок з моделлю `Movie` (Many-to-One).
- `text` (TextField): Текст відгуку.
- `score` (IntegerField): Оцінка користувача.
- `created_at` (DateTimeField): Дата створення відгуку.

---

## Приклади складних запитів (ORM)

### Завдання 15 — Власний запит: жанри, у яких більше 2 фільмів (annotate + filter)

Цей запит знаходить усі жанри, в яких більше ніж 2 фільми.

Спочатку використовується `annotate()`, щоб додати до кожного жанру поле
`movie_count` — це кількість пов’язаних з ним фільмів (через `Count("movie")`).
Потім через `filter(movie_count__gt=2)` відбираються тільки ті жанри, де
кількість фільмів більша за 2.

У результаті ми отримуємо список "популярних" жанрів за кількістю фільмів.

Мені це цікаво, тому що тут поєднується агрегація (Count) і фільтрація, що
допомагає краще зрозуміти, як працювати з базою даних у Django ORM. Наприклад,
так можна визначати популярні категорії товарів.

**Код запиту:**

```python
popular_genres = Genre.objects.annotate(
    movie_count=Count("movie")
).filter(movie_count__gt=2)

for g in popular_genres:
    print(f"Популярний жанр: {g.name} (фільмів: {g.movie_count})")
```
