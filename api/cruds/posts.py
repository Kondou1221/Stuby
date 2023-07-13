from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy import func, desc

import api.models.users as user_model
import api.models.follows as follow_model
import api.models.posts as post_model
import api.models.comments as comment_model

import api.schemas.posts as post_schema

#投稿作成
def create_post(db: Session, post_create: post_schema.create_post_request):

    try:
        new_post = post_model.Post(**post_create.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except SQLAlchemyError as e:
        return False
    return new_post

#ユーザープロフィール用の全ての投稿(20件)
def get_userprof_all(db: Session, myuser_id: int, other_user_id: int, post_id: int = None):
        
    try:

        post_comment_count_table = db.query(
                                        func.count()
                                    ).filter(
                                        comment_model.Comment.post_id == post_model.Post.post_id
                                    ).group_by(comment_model.Comment.post_id).label('post_comment_count')

        post_good_count_table = db.query(
                                func.count()
                            ).filter(
                                post_model.Postgood.post_id == post_model.Post.post_id
                            ).group_by(post_model.Postgood.post_id).label('post_good_count')
        
        post_good_status_table = db.query(
                                    func.count()
                                ).filter(
                                    post_model.Postgood.post_id == post_model.Post.post_id,
                                    post_model.Postgood.user_id == myuser_id
                                ).group_by(post_model.Postgood.post_id).label('post_good_status')
        
        if post_id:

            post = db.query(
                    post_model.Post,
                    post_model.Post.post_id,
                    post_model.Post.post_sentence,
                    post_model.Post.post_img,
                    post_model.Post.post_create,
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.icon_img,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    post_comment_count_table,
                    post_good_count_table,
                    post_good_status_table
                ).join(
                    user_model.User,
                    post_model.Post.user_id == user_model.User.user_id
                ).filter(post_model.Post.post_id < post_id, post_model.Post.user_id == other_user_id).order_by(desc(post_model.Post.post_id)).limit(20).all()

        
        else:

            post = db.query(
                    post_model.Post,
                    post_model.Post.post_id,
                    post_model.Post.post_sentence,
                    post_model.Post.post_img,
                    post_model.Post.post_create,
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.icon_img,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    post_comment_count_table,
                    post_good_count_table,
                    post_good_status_table
                ).join(
                    user_model.User,
                    post_model.Post.user_id == user_model.User.user_id
                ).filter(post_model.Post.user_id == other_user_id).order_by(desc(post_model.Post.post_id)).limit(20).all()

    except SQLAlchemyError as e:
        return False
        
    return post

#ユーザープロフィール用の写真と動画付きの投稿(20件) 写真のみと並び順がまだ
def get_userprof_img(db: Session, myuser_id: int, other_user_id: int, post_id: int = None):

    try:

        post_comment_count_table = db.query(
                                        func.count()
                                    ).filter(
                                        comment_model.Comment.post_id == post_model.Post.post_id
                                    ).group_by(comment_model.Comment.post_id).label('post_comment_count')

        post_good_count_table = db.query(
                                func.count()
                            ).filter(
                                post_model.Postgood.post_id == post_model.Post.post_id
                            ).group_by(post_model.Postgood.post_id).label('post_good_count')
        
        post_good_status_table = db.query(
                                    func.count()
                                ).filter(
                                    post_model.Postgood.post_id == post_model.Post.post_id,
                                    post_model.Postgood.user_id == myuser_id
                                ).group_by(post_model.Postgood.post_id).label('post_good_status')
        
        if post_id:

            post = db.query(
                    post_model.Post,
                    post_model.Post.post_id,
                    post_model.Post.post_sentence,
                    post_model.Post.post_img,
                    post_model.Post.post_create,
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.icon_img,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    post_comment_count_table,
                    post_good_count_table,
                    post_good_status_table
                ).join(
                    user_model.User,
                    post_model.Post.user_id == user_model.User.user_id
                ).filter(
                    post_model.Post.post_id < post_id,
                    post_model.Post.user_id == other_user_id,
                    post_model.Post.post_img.is_not(None)
                ).order_by(desc(post_model.Post.post_id)).limit(20).all()

        
        else:

            post = db.query(
                    post_model.Post,
                    post_model.Post.post_id,
                    post_model.Post.post_sentence,
                    post_model.Post.post_img,
                    post_model.Post.post_create,
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.icon_img,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    post_comment_count_table,
                    post_good_count_table,
                    post_good_status_table
                ).join(
                    user_model.User,
                    post_model.Post.user_id == user_model.User.user_id
                ).filter(
                    post_model.Post.post_img.is_not(None),
                    post_model.Post.user_id == other_user_id
                ).order_by(desc(post_model.Post.post_id)).limit(20).all()

    except SQLAlchemyError as e:
        return False
        
    return post

#投稿20件取得
def get_post(db: Session, user_id: int, post_id: int = None):

    try:

        post_comment_count_table = db.query(
                                        func.count()
                                    ).filter(
                                        comment_model.Comment.post_id == post_model.Post.post_id
                                    ).group_by(comment_model.Comment.post_id).label('post_comment_count')

        post_good_count_table = db.query(
                                func.count()
                            ).filter(
                                post_model.Postgood.post_id == post_model.Post.post_id
                            ).group_by(post_model.Postgood.post_id).label('post_good_count')
        
        post_good_status_table = db.query(
                                    func.count()
                                ).filter(
                                    post_model.Postgood.post_id == post_model.Post.post_id,
                                    post_model.Postgood.user_id == user_id
                                ).group_by(post_model.Postgood.post_id).label('post_good_status')
        
        print(post_good_status_table)
        
        if post_id:

            post = db.query(
                    post_model.Post,
                    post_model.Post.post_id,
                    post_model.Post.post_sentence,
                    post_model.Post.post_img,
                    post_model.Post.post_create,
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.icon_img,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    post_comment_count_table,
                    post_good_count_table,
                    post_good_status_table
                ).join(
                    user_model.User,
                    post_model.Post.user_id == user_model.User.user_id
                ).filter(post_model.Post.post_id > post_id).order_by(desc(post_model.Post.post_id)).limit(20).all()

        
        else:

            post = db.query(
                    post_model.Post,
                    post_model.Post.post_id,
                    post_model.Post.post_sentence,
                    post_model.Post.post_img,
                    post_model.Post.post_create,
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.icon_img,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    post_comment_count_table,
                    post_good_count_table,
                    post_good_status_table
                ).join(
                    user_model.User,
                    post_model.Post.user_id == user_model.User.user_id
                ).order_by(desc(post_model.Post.post_id)).limit(20).all()

    except SQLAlchemyError as e:
        return False

    return post

#フォローしている人の投稿(20件)
def get_post_user_id(db: Session, user_id: int, post_id: int = None):

    try:

        follower_post_table = db.query(
                                    follow_model.Follow.follower_id
                                ).filter(
                                    follow_model.Follow.follow_id == user_id,
                                ).subquery('fp')
        
        fp = aliased(follow_model.Follow, follower_post_table)

        post_comment_count_table = db.query(
                                        func.count()
                                    ).filter(
                                        comment_model.Comment.post_id == post_model.Post.post_id
                                    ).group_by(comment_model.Comment.post_id).label('post_comment_count')

        post_good_count_table = db.query(
                                func.count()
                            ).filter(
                                post_model.Postgood.post_id == post_model.Post.post_id
                            ).group_by(post_model.Postgood.post_id).label('post_good_count')
        
        post_good_status_table = db.query(
                                    func.count()
                                ).filter(
                                    post_model.Postgood.post_id == post_model.Post.post_id,
                                    post_model.Postgood.user_id == user_id
                                ).group_by(post_model.Postgood.post_id).label('post_good_status')
        
        if post_id:

            post = db.query(
                    post_model.Post,
                    post_model.Post.post_id,
                    post_model.Post.post_sentence,
                    post_model.Post.post_img,
                    post_model.Post.post_create,
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.icon_img,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    post_comment_count_table,
                    post_good_count_table,
                    post_good_status_table
                ).join(
                    user_model.User,
                    post_model.Post.user_id == user_model.User.user_id
                ).join(
                    fp,
                    fp.follower_id == post_model.Post.user_id
                ).filter(post_model.Post.post_id > post_id).order_by(desc(post_model.Post.post_id)).limit(20).all()

        else:

            post = db.query(
                    post_model.Post,
                    post_model.Post.post_id,
                    post_model.Post.post_sentence,
                    post_model.Post.post_img,
                    post_model.Post.post_create,
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.icon_img,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    post_comment_count_table,
                    post_good_count_table,
                    post_good_status_table
                ).join(
                    user_model.User,
                    post_model.Post.user_id == user_model.User.user_id
                ).join(
                    fp,
                    fp.follower_id == post_model.Post.user_id
                ).order_by(desc(post_model.Post.post_id)).limit(20).all()
            
    except SQLAlchemyError as e:
        return False
        
    return post

#投稿のいいね追加
def insert_postgood(db: Session, new_postgood: post_schema.change_postgood):
    new_postgood_data = post_model.Postgood(**new_postgood.dict())

    try:
        db.add(new_postgood_data)
        db.commit()
        db.refresh(new_postgood_data)
    except SQLAlchemyError as e:
        return False
    return new_postgood_data

#投稿のいいね削除
def delete_postgood_id(db: Session, delet_postgood: post_schema.change_postgood):
    delet_postgood = db.query(
            post_model.Postgood
        ).filter(
            post_model.Postgood.post_id == delet_postgood.post_id,
            post_model.Postgood.user_id == delet_postgood.user_id
        ).first()
    
    try:
        db.delete(delet_postgood)
        db.commit()
    except SQLAlchemyError as e:
        return False
    return delet_postgood