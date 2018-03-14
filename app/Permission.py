from app.models import Role

# permissions
anonymous_permissions = ['follow', 'register', 'login']
user_permissions = anonymous_permissions + ['add_post', 'edit_post', 'profile', 'logout']
moderator_permissions = user_permissions + ['edit_any_post', 'delete_post']
admin_permissions = moderator_permissions + ['admin']

# roles
anonymous_role = Role(name='anonymous')
user_role = Role(name='user')
moderator_role = Role(name='moderator')
admin_role = Role(name='admin')

role_permission = {
    anonymous_role: anonymous_permissions,
    user_role: user_permissions,
    moderator_role: moderator_permissions,
}
