import json

with open('usernames.txt', 'w') as f:
    for i in range(180591004, 180591101):
        user = {"username": str(i), "email": f"{i}@example.com", "password": "12345678"}
        json.dump(user, f)
        f.write('\n')
