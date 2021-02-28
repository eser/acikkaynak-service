from app.profiles.models import Profile


def get_profiles_by_user(username):
    profiles = Profile.objects.filter(users__username=username).all()

    return profiles
