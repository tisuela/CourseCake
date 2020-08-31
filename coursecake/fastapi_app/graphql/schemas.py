# graphql.schemas
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from ...database import models, sql


class Course(SQLAlchemyObjectType):
    class Meta:
        model = models.Course
        interfaces = (relay.Node, )


class Class(SQLAlchemyObjectType):
    class Meta:
        model = models.Class
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_courses = SQLAlchemyConnectionField(Course.connection)
    all_classes = SQLAlchemyConnectionField(Class.connection)
