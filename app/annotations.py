from sqlalchemy.orm     import Session
from typing     import Annotated
from fastapi    import Depends
from .database  import get_db
from .oauth2    import get_current_user

# Dependency Injection, type hint 간소화
# https://fastapi.tiangolo.com/tutorial/dependencies/#dependencies-first-steps

annotation_db = Annotated[Session, Depends(get_db)]
annotation_auth = Annotated[int, Depends(get_current_user)]
