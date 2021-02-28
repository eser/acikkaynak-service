import graphene
from app.common.library import graphql
from app.common.models import City
from ..models import Profile
from .queries import ProfileNode


# queries


class Query(graphene.ObjectType):
    pass


# mutations


class ProfileUpdateMutation(graphene.Mutation):
    Output = ProfileNode

    class Arguments:
        profile = graphene.ID(required=True)
        slug = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        gender = graphene.String()
        birthdate = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        profile_picture_uri = graphene.String()
        locale = graphene.String()
        bio = graphene.String()
        location_city = graphene.ID()
        languages = graphene.List(graphene.ID)
        timezone = graphene.String()

    @classmethod
    # pylint:disable=unused-argument
    def mutate(cls, root, info, **kwargs):
        # TODO ensure that that profile belongs to this user
        profile_id = graphql.global_id_to_model_id(kwargs["profile"])
        if profile_id is None:
            raise ValueError("Profile id is invalid")

        profile = Profile.objects.get(pk=profile_id)

        cognito_needs_update = False
        user = None

        if profile.users.count() == 1:
            user = profile.users.first()

        # if profile.users.filter(uuid=info.context.user.uuid).count() == 0:
        #     raise ValueError("you don't own this profile")

        # for standard fields
        # (keyword, update_profile, update_user, update_cognito)
        fields = [
            ("slug", True, False, False),
            ("first_name", True, True, True),
            ("last_name", True, True, True),
            ("gender", True, True, True),
            ("birthdate", True, True, True),
            ("email", True, True, True),
            ("phone", True, True, True),
            ("profile_picture_uri", True, True, True),
            ("bio", True, False, False),
            ("timezone", True, False, False),
            ("locale", False, True, True),
        ]

        for keyword, update_profile, update_user, update_cognito in fields:
            if kwargs.get(keyword):
                if update_profile:
                    setattr(profile, keyword, kwargs[keyword])
                if update_user and user is not None:
                    setattr(user, keyword, kwargs[keyword])
                if update_cognito:
                    cognito_needs_update = True

        # for *-to-many fields
        if (kwargs.get("languages")):
            profile.languages.clear()

            for language_global_id in kwargs["languages"]:
                language_id = graphql.global_id_to_model_id(language_global_id)

                if language_id is not None:
                    profile.languages.add(language_id)

        if (kwargs.get("location_city")):
            location_city_id = graphql.global_id_to_model_id(kwargs["location_city"])
            if location_city_id is None:
                raise ValueError("City id is invalid")

            location_city = City.objects.get(pk=location_city_id)
            location_country = location_city.country

            profile.location_city = location_city
            profile.location_country = location_country

        if cognito_needs_update:
            pass  # TODO: update cognito

        profile.full_clean()
        profile.save()

        return profile


class Mutation(graphene.ObjectType):
    profile_update = ProfileUpdateMutation.Field()
