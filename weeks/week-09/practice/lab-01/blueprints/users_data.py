def get_user(uid):
    users = {
        1: {"first_name": "Văn", "last_name": "Nguyễn", "email": "van.nguyen@example.com"}
    }
    return users.get(uid)
