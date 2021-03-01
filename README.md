# acikkaynak-service

## Table of Contents

1. [GraphQL Endpoints](#graphql-endpoints)
    * [Auth](#auth)
        - [CheckUser query](#checkuser-query)
        - [Login mutation](#login-mutation)
        - [Signup mutation](#signup-mutation)
        - [SignupConfirm mutation](#signupconfirm-mutation)
    * [Profiles](#profiles)
        - [Getting All Profiles](#getting-all-profiles)
        - [Getting a Specific Profile by ID](#getting-a-specific-profile-by-id)
        - [Getting a Specific Profile by Slug](#getting-a-specific-profile-by-slug)
        - [Updating a Specific Profile](#updating-a-specific-profile)
        - [Updating a Specific Profile Partially](#updating-a-specific-profile-partially)
2. [Development Manual](#development-manual)
    * [Development Environment](#development-environment)
        - [Setting up the codebase](#setting-up-the-codebase)
        - [Creating the database](#creating-the-database)
    * [Development Operations](#development-operations)
        - [Compressing migration files](#compressing-migration-files)
    * [AWS ECS/Fargate deployment](#aws-ecsfargate-deployment)


## GraphQL Endpoints

### Auth

#### CheckUser query

checking user by phone number:

```
query {
  checkUser(login: "+905115001122") {
    username
    userExists
    status
  }
}
```

checking user by e-mail address:

```
query {
  checkUser(login: "eser@ozvataf.com") {
    username
    userExists
    status
  }
}
```


#### Login mutation

use previously obtained username to login here:

```
mutation {
  login(username: "34de0e45-e43b-48e7-bfc2-f2d5a4ce5b70", password: "test123") {
    isSuccessful
    error
    details {
      tokenType
      idToken
      accessToken
      refreshToken
      expiresIn
    }
    profiles {
      id
      slug
      firstName
      lastName
      profilePictureUri
    }
  }
}
```


#### Signup mutation

check the e-mail afterwards to continue with the signup confirmation:

```
mutation {
  signup(
    login: "eser@ozvataf.com",
    password: "test123",
    firstName: "Eser",
    lastName: "Ozvataf",
    gender: "MALE",
    birthdate: "1984-04-16",
    phone: "+905115001122",
    profilePictureUri: "https://avatars.githubusercontent.com/u/866558?s=460&u=b22a39f91f830670029edf4a75a4917d167e3477&v=4",
    locale: "en-us"
  ) {
    isSuccessful
    error
    confirmationCode {
      attributeName
      deliveryMedium
      destination
    }
    username
  }
}
```


#### SignupConfirm mutation

use received confirmation code here:

```
mutation {
  signupConfirm(username: "34de0e45-e43b-48e7-bfc2-f2d5a4ce5b70", confirmationCode: "572954") {
    isSuccessful
    error
  }
}
```


#### ResetPassword mutation

```
mutation {
  resetPassword(username: "34de0e45-e43b-48e7-bfc2-f2d5a4ce5b70") {
    isSuccessful
    error
  }
}
```


#### ResetPasswordConfirm mutation

```
mutation {
  resetPasswordConfirm(username: "34de0e45-e43b-48e7-bfc2-f2d5a4ce5b70", confirmationCode: "572954", newPassword: "test456") {
    isSuccessful
    error
  }
}
```


#### ResendConfirmation mutation

```
mutation {
  resendConfirmation(username: "34de0e45-e43b-48e7-bfc2-f2d5a4ce5b70") {
    isSuccessful
    error
  }
}
```


#### ChangePassword mutation

```
mutation {
  changePassword(accessToken: "...", previousPassword: "test456", newPassword: "test789") {
    isSuccessful
    error
  }
}
```


### Profiles

#### Getting All Profiles

```
query {
  allProfiles {
    edges {
      node {
        id
        slug
        role
        firstName
        lastName
        email
        phone
        profilePictureUri
        bio
        locationCity
        locationCountry
        languages {
          edges {
            node {
              isoCode
              name
            }
          }
        }
        tags {
          edges {
            node {
              slug
              name
            }
          }
        }
        achievements {
          edges {
            node {
              type
              earnedAt
            }
          }
        }
      }
    }
  }
}
```


#### Getting a Specific Profile by ID

```
query {
  profile(id: "UHJvZmlsZU5vZGU6YTA3MjE1NWUtNWUwYi00OWNmLThkNWItYzQ2YjBlN2E4MDAx") {
    id
    slug
    role
    firstName
    lastName
    email
    phone
    profilePictureUri
    bio
    locationCity
    locationCountry
    languages {
      edges {
        node {
          isoCode
          name
        }
      }
    }
    tags {
      edges {
        node {
            slug
            name
        }
      }
    }
    achievements {
      edges {
        node {
            type
            earnedAt
        }
      }
    }
  }
}
```


#### Getting a Specific Profile by Slug

```
query {
  profileBySlug(slug: "eser-ozvataf") {
    id
    slug
    role
    firstName
    lastName
    email
    phone
    profilePictureUri
    bio
    locationCity
    locationCountry
    languages {
      edges {
        node {
          isoCode
          name
        }
      }
    }
    tags {
      edges {
        node {
          slug
          name
        }
      }
    }
    achievements {
      edges {
        node {
          type
          earnedAt
        }
      }
    }
  }
}
```


#### Updating a Specific Profile

```
mutation {
  updateProfile(
      id: "UHJvZmlsZU5vZGU6YTA3MjE1NWUtNWUwYi00OWNmLThkNWItYzQ2YjBlN2E4MDAx",
      firstName: "Eser",
      lastName: "Ozvataf",
      profilePictureUri: "https://avatars.githubusercontent.com/u/866558?s=460&u=b22a39f91f830670029edf4a75a4917d167e3477&v=4",
      bio: "Morbi in hendrerit augue. Proin tincidunt ligula libero, efficitur imperdiet eros lacinia ac. Vivamus metus nunc, fermentumas."
  ) {
    id
    firstName
    lastName
    profilePictureUri
    bio
  }
}
```


#### Updating a Specific Profile Partially

```
mutation {
  updateProfile(
      id: "UHJvZmlsZU5vZGU6YTA3MjE1NWUtNWUwYi00OWNmLThkNWItYzQ2YjBlN2E4MDAx",
      bio: "Morbi in hendrerit augue. Proin tincidunt ligula libero, efficitur imperdiet eros lacinia ac. Vivamus metus nunc, fermentumas."
  ) {
    id
    bio
  }
}
```


## Development Manual

### Development Environment

#### Setting up the codebase

```sh
echo "\033[1;33mInstalling dependencies... \033[0m"
pipenv install --dev --pre
```


#### Creating the database

```sh
echo "\033[1;33mApplying migrations... \033[0m"
python manage.py migrate


echo "\033[1;33mSeeding initial data... \033[0m"
python manage.py loaddata ./app/common/fixtures/initial_data.yaml
python manage.py loaddata ./app/profiles/fixtures/initial_data.yaml
python manage.py loaddata ./app/certificates/fixtures/initial_data.yaml
```


### Development Operations

you may need these instructions during development, but don't execute them unless you know what these mean


#### Compressing migration files

IMPORTANT: recreation of database is needed afterwards

```sh
echo "\033[1;33mDumping existing initial data... \033[0m"
APP_NAMES=`python manage.py app_list`
for app in ${APP_NAMES[*]}
do
    echo "...executing $app"
    python manage.py dumpdata --format yaml --indent 2 "$app" > "app/$app/fixtures/initial_data.yaml"
done

echo "\033[1;33mRecreating migrations... \033[0m"
for app in ${APP_NAMES[*]}
do
    echo "...deleting migrations of $app"
    rm "app/$app/migrations/0*.py"
done
echo "...creating"
python manage.py makemigrations
```


### AWS ECS/Fargate deployment

```sh
docker build . -t acikkaynak-service:0001 -t __id__.dkr.ecr.eu-west-1.amazonaws.com/acikkaynak-service:0001

aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin __id__.dkr.ecr.eu-west-1.amazonaws.com
docker push __id__.dkr.ecr.eu-west-1.amazonaws.com/acikkaynak-service

aws ecs update-service --cluster acikkaynak-service --service custom-service --force-new-deployment
```
