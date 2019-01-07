from django_currentuser.middleware import get_current_user
from django.db import models, connection
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .enum import status_var, country_var, value_var, gender_var


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class UserManager(BaseUserManager):
    def create_user(self, username=None, password=None):
        if not username:
            raise ValueError('Users must have an Username address')

        user = self.model(username=self.normalize_username(username))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username=None, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.gender = 'Male'
        user.country = 'Afghanistan'
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.country = 'Afghanistan'
        user.gender = 'Male'
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class Users(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    img = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=230, blank=True)
    city_town = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, choices=country_var, default='')
    birthday = models.DateField(blank=True)
    gender = models.CharField(max_length=50, choices=gender_var, default='')
    ip = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'users'

    def avg_all(self):  # for all book to this author
        with connection.cursor() as cursor:
            cursor.execute("select AVG(value) as avg_all from ratings where ratings.user = %s", [self.id])
            name = cursor.fetchone()
        return name

    def book(self):
        with connection.cursor() as cursor:
            cursor.execute("select books.id, book_name, books.img, status from Books, books_user "
                           "where books_user.user = %s and books_user.book = Books.id", [self.id])
            name = dictfetchall(cursor)
        return name

    def read(self):
        with connection.cursor() as cursor:
            cursor.execute("select books.id, books.img, books.book_name, books.author, ratings.value, avg(value) as avg"
                           " from books_user, Books, ratings where books_user.user = %s and books.id = books_user.book "
                           "and books_user.status = 'read' and ratings.book = books_user.book "
                           "group by books_user.book", [self.id])
            name = dictfetchall(cursor)
        return name

    def current_read(self):
        with connection.cursor() as cursor:
            cursor.execute("select books.id, books.img, books.book_name, books.author, ratings.value, avg(value) as avg"
                           " from books_user, Books, ratings where books_user.user = %s and books.id = books_user.book "
                           "and books_user.status = 'current read' and ratings.book = books_user.book "
                           "group by books_user.book", [self.id])
            name = dictfetchall(cursor)
        return name

    def to_read(self):
        with connection.cursor() as cursor:
            cursor.execute("select books.id, books.img, books.book_name, books.author, ratings.value, avg(value) as avg"
                           " from books_user, Books, ratings where books_user.user = %s and books.id = books_user.book "
                           "and books_user.status = 'to read' and ratings.book = books_user.book "
                           "group by books_user.book", [self.id])
            name = dictfetchall(cursor)
        return name

    def get_username(self):
        if self.username:
            return self.username
        return self.username

    def get_password(self):
        if self.password:
            return self.password
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Authors(models.Model):
    author_name = models.CharField(max_length=100)
    author_bio = models.TextField(blank=True)
    birthday = models.DateField(blank=True)
    img = models.ImageField(upload_to="Authors\static\Authors", blank=True, null=True)
    header_img = models.ImageField(upload_to="Authors\static\Header", blank=True, null=True)
    face_icon = models.CharField(max_length=100, blank=True)
    twitter_icon = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'authors'

    def book_name(self):
        with connection.cursor() as cursor:
            cursor.execute("select books.id, books.book_name, books.img, left(books.book_desc,100),AVG(value) as avg, "
                           "books.created_at from Books, ratings where books.author = %s and ratings.book = books.id "
                           "group by books.id ", [self.id])
            name = dictfetchall(cursor)
        return name

    def avg_all(self):  # for all book to this author
        with connection.cursor() as cursor:
            cursor.execute("select AVG(value) as avg_all from ratings , books where books.author = %s "
                           "and ratings.book = books.id", [self.id])
            name = cursor.fetchone()
        return name

    def follower(self):
        with connection.cursor() as cursor:
            cursor.execute("select users.id, users.username, avg(VALUE) as avg, users.img from users, ratings, "
                           "followers where followers.following_id = %s and users.id = followers.follower_id and "
                           "ratings.user = followers.follower_id group by users.id", [self.id])
            name = dictfetchall(cursor)
            return name

    def s(self):
        d = {
            'author_name': self.author_name,
            'author_bio': self.author_bio,
            'birthday': self.birthday,
            'img': self.img,
            'header_img': self.header_img,
            'face_icon': self.face_icon,
            'twitter_icon': self.twitter_icon,
            'website': self.website,
            'created_at': self.created_at,
        }


class Categories(models.Model):
    id = models.IntegerField(primary_key=True)
    cate_name = models.CharField(max_length=100)
    cate_desc = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'categories'

    def most_recent(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT books.id, books.book_name, books.img, left(books.book_desc, 100) as description, "
                           "avg(ratings.value) as avg FROM books, ratings where ratings.book=books.id and "
                           "books.category = %s group by books.id order by books.created_at DESC limit 12", [self.id])
            name = dictfetchall(cursor)
        return name

    def most_read(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT books.id, books.book_name, books.img, left(books.book_desc, 100) as description, "
                           "avg(ratings.value) as avg FROM books_user, books, ratings where ratings.book = books.id "
                           "and books.category = %s and books_user.status = 'read' and books_user.book = books.id "
                           "group by books.id order by count(*) DESC limit 12", [self.id])
            name = dictfetchall(cursor)
        return name

    def most_rated(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT books.id, books.book_name, books.img, left(books.book_desc, 100) as description, "
                           "avg(ratings.value) as avg FROM books, ratings where ratings.book=books.id and "
                           "books.category = %s group by books.id order by avg DESC limit 12", [self.id])
            name = dictfetchall(cursor)
        return name


class Books(models.Model):
    book_name = models.CharField(max_length=100)
    img = models.ImageField(upload_to="Books\static\Books", blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING, db_column='category')
    author = models.ForeignKey(Authors, models.DO_NOTHING, db_column='author')
    book_desc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'books'

    def avg_rating(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT AVG(value) FROM Ratings where ratings.book = %s", [self.id])
            rate = cursor.fetchone()
        return rate

    def review(self):
        with connection.cursor() as cursor:
            cursor.execute("select  users.id, username, users.img, reviews.created_at, comment, likes "
                           "from reviews, users where reviews.book = %s and users.id = reviews.user", [self.id])
            rev = dictfetchall(cursor)
        return rev

    def review_count(self):
        with connection.cursor() as cursor:
            cursor.execute("select count(comment) from reviews where book = %s", [self.id])
            rev = cursor.fetchone()
        return rev

    def user_rating(self):
        u = get_current_user().id
        with connection.cursor() as cursor:
            cursor.execute("select avg(value) from Ratings where ratings.book = %s and ratings.user = %s", [self.id, u])
            rate = cursor.fetchone()
        return rate

    def user_id(self):
        u = get_current_user().id
        with connection.cursor() as cursor:
            cursor.execute("select user from Ratings where ratings.book = %s and ratings.user = %s "
                           "and value IS NOT NULL", [self.id, u])
            user_id = cursor.fetchone()
        return user_id

    def user_status(self):
        u = get_current_user().id
        with connection.cursor() as cursor:
            cursor.execute("SELECT status FROM books_user where books_user.book = %s and books_user.user = %s",
                           [self.id, u])
            stat = cursor.fetchone()
        return stat

    def same_author(self):
        with connection.cursor() as cursor:
            cursor.execute("select books.id, books.book_name, books.img, avg(value) as avg from books, ratings where "
                           "books.author = (select author from books where id = %s) and ratings.book = books.id group "
                           "by books.id order by books.id desc limit 12", [self.id])
            book = dictfetchall(cursor)
        return book

    def most_recent_l(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT books.id, books.book_name, books.img, left(books.book_desc, 100) as description, "
                           "avg(ratings.value) as avg FROM books, ratings where ratings.book=books.id "
                           "group by books.id order by books.created_at DESC limit 12")
            name = dictfetchall(cursor)
        return name

    def most_rated_l(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT books.id, books.book_name, books.img, left(books.book_desc, 100) as description, "
                           "avg(ratings.value) as avg FROM books, ratings where ratings.book=books.id "
                           "group by books.id order by avg DESC limit 12")
            name = dictfetchall(cursor)
        return name

    def most_recent(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT books.id, books.book_name, books.img, left(books.book_desc, 100) as description, "
                           "avg(ratings.value) as avg FROM books, ratings where ratings.book=books.id "
                           "group by books.id order by books.created_at ASC")
            name = dictfetchall(cursor)
        return name

    def most_rated(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT books.id, books.book_name, books.img, left(books.book_desc, 100) as description, "
                           "avg(ratings.value) as avg FROM books, ratings where ratings.book=books.id "
                           "group by books.id order by avg DESC")
            name = dictfetchall(cursor)
        return name

    def data(u):
        with connection.cursor() as cursor:
            cursor.execute("SELECT user as user_id, book as book_id,  value as rating from ratings")
            avg = dictfetchall(cursor)
        return avg

    def item(u):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id as book_id, book_name, img from books")
            avg = dictfetchall(cursor)
        return avg


class BooksUser(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, db_column='book')
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user')
    status = models.CharField(max_length=12, choices=status_var, default='')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = True
        unique_together = (('book', 'user'),)
        db_table = 'books_user'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Followers(models.Model):
    follower_id = models.ForeignKey('Users', models.DO_NOTHING, related_name='user_follower', db_column='follower_id')
    following_id = models.ForeignKey('Users', models.DO_NOTHING, related_name='user_following', db_column='following_id')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (('follower_id', 'following_id'),)
        db_table = 'followers'

    def user(self):
        with connection.cursor() as cursor:
            cursor.execute("select id, username from users where users.id = %s ", [get_current_user().id])
            rev = dictfetchall(cursor)
        return rev

    def followers(self):
        with connection.cursor() as cursor:
            cursor.execute("select users.username, followers.created_at, avg(value) as avg from users, followers, "
                           "ratings where followers.follower_id = %s and users.id = followers.following_id and "
                           "ratings.user = users.id group by users.id", [get_current_user().id])
            rev = dictfetchall(cursor)
        return rev


class Messages(models.Model):
    message_content = models.TextField()
    mess_from = models.IntegerField()
    mess_to = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'messages'

    def __unicode__(self):
        return self.message_content


class Ratings(models.Model):
    book = models.ForeignKey(Books, models.DO_NOTHING, db_column='book')
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user')
    value = models.CharField(max_length=3, choices=value_var, default='')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = True
        unique_together = (('book', 'user'),)
        db_table = 'ratings'

    def avrg(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT AVG(value) FROM Ratings")
            avg = cursor.fetchone()
        return avg


class Reviews(models.Model):
    book = models.ForeignKey(Books, models.DO_NOTHING, db_column='book')
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user')
    comment = models.TextField(blank=True)
    likes = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'reviews'
