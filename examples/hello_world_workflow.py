from typing import TypedDict


class User(TypedDict):
    id: int
    name: str
    email: str
    active: bool


user_record = User(id=1, name="Mr.A", email="mra@gmail.com", active=True);
user_record["name"] = 1;
print(user_record["name"]);