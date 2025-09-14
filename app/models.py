from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin
from hashlib import md5

followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True) ## so.Mapped -> thuoc tinh nay duoc anh xa toi 1 cot trong database. so.mapped_column -> khai bao mot cot
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author') # dinh nghia relationship, khong co cot nao, the hien moi lien ket giua 2 thuc the, trong do post
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_time: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers') #
    # primaryjoin là điều kiện kết nối từ entity sang associated table
    # secondaryjoin là điều kiện kết nối từ associated table sang phần còn lại của liên kết (ở đây là user-table-user)
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
    
    def is_following(self, user):
        self.following.select().where(User.id == user.id)
        return db.session.scalar()
    
    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)
    
    def following_count(self):
        query = sa.select(sa.func.count()).select_from( 
            self.following.select().subquery())
        return db.session.scalar(query)
    
    def following_posts(self):
        query = self.posts.select()
        return db.session.scalar(query)
    
    def __repr__(self):
        return 'User {}'.format(self.username) # in ra thong tin cua user
    
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id) ,index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body) # kiem soat format in ra cua oject post
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))