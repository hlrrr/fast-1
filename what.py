from fastapi.testclient     import TestClient
from app.main   import app
from app    import schemas, annotations
from app.database   import get_db, get_db_test
import pytest

from app.routers    import user

def test_create():
    original = user.create_user
    print(user.create_user.__annotations__['db'])
    original.__annotations__['db'] = annotations.database_test
    print(original.__annotations__['db'])

test_create()