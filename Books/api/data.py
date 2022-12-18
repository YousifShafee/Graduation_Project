from django.db import connection
from Api.models import Books, Authors, Categories
from django_currentuser.middleware import get_current_user
from Recommend.views import cached_item


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def avg_rating(book_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT AVG(value) FROM Ratings where ratings.book = %s", [book_id])
        rate = cursor.fetchone()
    return rate


def review(book_id):
    with connection.cursor() as cursor:
        cursor.execute("select  users.id, username, users.img, reviews.created_at, comment, likes "
                       "from reviews, users where reviews.book = %s and users.id = reviews.user", [book_id])
        rev = dictfetchall(cursor)
    return rev


def review_count(book_id):
    with connection.cursor() as cursor:
        cursor.execute("select count(comment) from reviews where book = %s", [book_id])
        rev = cursor.fetchone()
    return rev


def user_rating(book_id):
    u = get_current_user().id
    with connection.cursor() as cursor:
        cursor.execute("select avg(value) from Ratings where ratings.book = %s and ratings.user = %s", [book_id, u])
        rate = cursor.fetchone()
    return rate


def user_id(book_id):
    u = get_current_user().id
    with connection.cursor() as cursor:
        cursor.execute("select user from Ratings where ratings.book = %s and ratings.user = %s "
                       "and value IS NOT NULL", [book_id, u])
        user_id = cursor.fetchone()
    return user_id


def user_status(book_id):
    u = get_current_user().id
    with connection.cursor() as cursor:
        cursor.execute("SELECT status FROM books_user where books_user.book = %s and books_user.user = %s",
                       [book_id, u])
        stat = cursor.fetchone()
    return stat


def same_author(book_id):
    with connection.cursor() as cursor:
        cursor.execute("select books.id, books.book_name, books.img, avg(value) as avg from books, ratings where "
                       "books.author = (select author from books where id = %s) and ratings.book = books.id group "
                       "by books.id order by books.id desc limit 12", [book_id])
        book = dictfetchall(cursor)
    return book


def main(book_id):
    book = Books.objects.get(id=book_id)
    result = {'id': book_id}
    result['book_name'] = book.book_name
    result['img'] = str(book.img)
    author = Authors.objects.get(id=str(book.author.id))
    result['author'] = {'id': author.id, 'author_name': author.author_name}
    category = Categories.objects.get(id=str(book.category.id))
    result['category'] = {'id': category.id, 'cate_name': category.cate_name}
    item = cached_item(book.id)
    result['recommend_item'] = item[:10]
    result['avg_rating'] = avg_rating(book.id)
    result['user_rating'] = user_rating(book.id)
    result['user_status'] = user_status(book.id)
    result['same_author'] = same_author(book.id)
    result['book_desc'] = book.book_desc
    result['review_count'] = review_count(book.id)
    result['review'] = review(book.id)
    return result
