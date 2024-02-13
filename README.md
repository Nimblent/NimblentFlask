# Permissions
Each user has a permissions that is an integer where each bit code a unique permission
Here are the unique identifier of permissions

0.  Create User
1.  Create Group
2.  Create Subject
3.  Create Course
4.  Edit Subject
5.  Edit Group
6.  Edit Course
7.  Edit User
8.  Delete Course
9.  Delete Subject
10. Delete User
11. Delete Group
12. Edit permission

```PY
user_perm = 3840 # Possible user permissions

# We want to check if this user can delete a subject (Perm n°9)
(user_perm >> 9) & 1 # Will return 1 if the user has the permission
```