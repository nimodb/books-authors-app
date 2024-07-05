import graphene
from books.schema import Query as BooksQuery, Mutation as BooksMutation


class Query(BooksQuery, graphene.ObjectType):
    pass


class Mutation(BooksMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
