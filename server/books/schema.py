import graphene
from graphene_django.types import DjangoObjectType
from .models import Book, Author


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class BooksType(DjangoObjectType):
    class Meta:
        model = Book


class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType)
    book = graphene.Field(BooksType, id=graphene.Int())
    all_authors = graphene.List(AuthorType)
    author = graphene.Field(AuthorType, id=graphene.Int())

    def resolve_all_books(self, info, **kwargs):
        return Book.objects.all()

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

    def resolve_all_authors(self, info, **kwargs):
        return Author.objects.all()

    def resolve_author(self, info, id):
        return Author.objects.get(pk=id)


class CreateAuthor(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        if Author.objects.filter(name=name).exists():
            return CreateAuthor(
                success=False, message="Author with this name already exists."
            )
        author = Author(name=name)
        author.save()
        return CreateAuthor(
            id=author.pk,
            name=author.name,
            success=True,
            message="Author created successfully.",
        )


class CreateBook(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    genre = graphene.String()
    author_id = graphene.Int()
    date_released = graphene.types.datetime.Date()
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        name = graphene.String()
        genre = graphene.String()
        author_id = graphene.Int()
        date_released = graphene.types.datetime.Date()

    def mutate(self, info, name, genre, author_id, date_released):
        author = Author.objects.get(pk=author_id)
        book = Book(name=name, genre=genre, author=author, date_released=date_released)
        book.save()
        return CreateBook(
            id=book.id,
            name=book.name,
            genre=book.genre,
            author_id=author.id,
            date_released=book.date_released,
            success=True,
            message="Book created successfully.",
        )


class UpdateAuthor(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, id, name):
        try:
            author = Author.objects.get(pk=id)
            if Author.objects.filter(name=name).exclude(pk=id).exists():
                return UpdateAuthor(
                    success=False,
                    message="Another with this name already exists.",
                )
            author.name = name
            author.save()
            return UpdateAuthor(
                id=author.pk,
                name=author.name,
                success=True,
                message="Author updated successfully.",
            )
        except Author.DoesNotExist:
            return UpdateAuthor(success=False, message="Author not found.")


class UpdateBook(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    genre = graphene.String()
    author_id = graphene.Int()
    date_released = graphene.types.datetime.Date()
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        genre = graphene.String()
        author_id = graphene.Int()
        date_released = graphene.types.datetime.Date()

    def mutate(
        self, info, id, name=None, genre=None, author_id=None, date_released=None
    ):
        try:
            book = Book.objects.get(pk=id)
            if name:
                book.name = name
            if genre:
                book.genre = genre
            if author_id:
                book.author = Author.objects.get(pk=author_id)
            if date_released:
                book.date_released = date_released
            book.save()
            return UpdateBook(
                id=book.pk,
                name=book.name,
                genre=book.genre,
                author_id=book.author.pk,
                date_released=book.date_released,
                success=True,
                message="Book updated successfully.",
            )
        except Book.DoesNotExist:
            return UpdateBook(success=False, message="Book not found.")
        except Author.DoesNotExist:
            return UpdateBook(success=False, message="Author not found.")


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_book = CreateBook.Field()
    update_author = UpdateAuthor.Field()
    update_book = UpdateBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
