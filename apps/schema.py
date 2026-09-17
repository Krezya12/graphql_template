from pyexpat.errors import messages

import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'


# Query -> Malumotlarni bazadan olish qismi QUERY deyiladi
class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info):
        return Category.objects.all()


# Mutation ->  Malumotlarni o'zgartirish saqlash o'chirish MUTATION deyiladi
class CreateCategory(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    def mutate(self, info, name, description):
        Category.objects.create(name=name, description=description)
        return CreateCategory(message="yaratildi")


class UpdateCategory(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    def mutate(self, info, id, name=None, description=None):
        category = Category.objects.get(pk=id)
        if name:
            category.name = name
        if description:
            category.description = description

        category.save()
        return UpdateCategory(message="Post o'zgartirildi")


class DeleteCategory(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        query = Category.objects.filter(pk=id)
        if query.exists():
            query.delete()
        return UpdateCategory(message="Post o'chirildi")


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()


# Asosiy schema
schema = graphene.Schema(query=Query, mutation=Mutation)
