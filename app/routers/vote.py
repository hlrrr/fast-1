from email.policy import HTTP
from fastapi    import Response, status, HTTPException, APIRouter
from ..     import schemas, database, models, oauth2, annotations


router = APIRouter(
    prefix='/vote/',
    tags=['Vote']
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,
         db: annotations.database,
         whois:annotations.authentication):
    
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post={vote.post_id} does not exist')
     
    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==whois.id)
    vote_found = vote_query.first()

    if (vote.direction==1):
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user={whois.id} already liked post={vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=whois.id)
        db.add(new_vote)
        db.commit()
        return {'message':'likey, added'}
       
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="no vote")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message':'likey, deleted'}
