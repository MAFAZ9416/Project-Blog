#----> Import the necessary modules
from django.contrib.auth.models import Group, Permission


#----> Create a function to create groups and permissions and we will connect this function to the post_migrate signal in the apps.py file so when we run the migrate command this function will be executed and it will create the groups and permissions in the database
def create_group_permission(sender, **kwargs):

    # We use try and except block to handle the error if the groups and permissions already exist in the database
    try :

        # Create Groups
        readers_group, created = Group.objects.get_or_create(name = 'Readers')
        authors_group, created = Group.objects.get_or_create(name = 'Authors')
        editors_group, created = Group.objects.get_or_create(name = 'Editors')

        # Create Permission
        readers_permission = [
            Permission.objects.get(codename = "view_post")
        ] 
        authors_permission = [
            Permission.objects.get(codename = "view_post"),
            Permission.objects.get(codename = "add_post"),
            Permission.objects.get(codename = "change_post"),
            Permission.objects.get(codename = "delete_post")
        ]

        # We use get_or_create function so it will return two values so we declare two variables and just use the is_published to the editors permission.
        is_published, created = Permission.objects.get_or_create(codename = 'is_published', name = 'can publish post', content_type_id = 7) 

        editors_permission = [
            is_published,
            Permission.objects.get(codename = "view_post"),
            Permission.objects.get(codename = "add_post"),
            Permission.objects.get(codename = "change_post"),
            Permission.objects.get(codename = "delete_post")
        ]

        # Assign the groups to the permissions
        readers_group.permissions.set(readers_permission)
        authors_group.permissions.set(authors_permission)
        editors_group.permissions.set(editors_permission)

        # Print a message to the console if the groups and permissions are created successfully
        print("Permission Granted Successfully !")

    except Exception as e:
        # Print the error message to the console if any error occurs while creating the groups and permissions
        print(f"Error occurred {e}")