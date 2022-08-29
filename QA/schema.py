import graphene
from graphql_auth.schema import MeQuery, UserQuery
from graphql_auth import mutations
from qaApp.schema import ModelQuery, ModelMutation


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class Query(MeQuery, UserQuery, ModelQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, ModelMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
