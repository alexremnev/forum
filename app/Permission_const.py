from app.models.role_permission import Role

# permissions
anonymous_permissions = ['follow', 'register', 'login']
user_permissions = anonymous_permissions + ['add_post', 'edit_post', 'profile', 'logout']
moderator_permissions = user_permissions + ['edit_any_post', 'delete_post']
admin_permissions = moderator_permissions + ['admin']

# role names
anonymous_role_name = 'anonymous'
user_role_name = 'user'
moderator_role_name = 'moderator'
admin_role_name = 'admin'

# roles
anonymous_role = Role(name=anonymous_role_name)
user_role = Role(name=user_role_name)
moderator_role = Role(name=moderator_role_name)
admin_role = Role(name=admin_role_name)

role_permission = {
    anonymous_role: anonymous_permissions,
    user_role: user_permissions,
    moderator_role: moderator_permissions,
}
