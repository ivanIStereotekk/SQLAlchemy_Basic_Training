from datetime import datetime
from sqlalchemy import ForeignKey, String,select
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped,joinedload
from  sqlalchemy.orm import mapped_column
from typing import  List, Optional
from sqlalchemy import create_engine

current_time = datetime.now().time()



engine = create_engine("sqlite:///oneToMany_data.db",echo=True)

connection = engine.connect()



class Base(DeclarativeBase):
    pass


class User(Base):
    """" User ORM model"""
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20),unique=True)
    email: Mapped[str] = mapped_column(String(20),unique=True)
    releases: Mapped[List["Release"]] = relationship(back_populates="author",lazy="joined",uselist=True)
    def __repr__(self) -> str:
        return f"USER-ID={self.id}  |  USER-NAME={self.name} |   USER-EMAIL={self.email} "




class Release(Base):
    """Release ORM model"""
    __tablename__ = 'release'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    release_date: Mapped[str] = mapped_column(String(100))
    genre: Mapped[str] = mapped_column(String(100))
    author_fk: Mapped[List[int]] = mapped_column(ForeignKey('user.id')) # Here we define column trough - __tablename__ = 'user'
    author: Mapped["User"] = relationship(back_populates="releases",uselist=True,lazy="joined")
    def __repr__(self) -> str:
        return f"RELEASE-NAME={self.name} | RELEASE-ID={self.id}  | GENRE={self.genre}"





#https://youtu.be/Uym2DHnUEno?list=PLLAleBnw-fxzlVNyIylLbRdsj3zLHogoL tutorial

Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker
import random
import string
import secrets



#





# user_collection = [
#     {'name': "Bob marley", 'email':"bob@example.com"},
#     {'name': "Sting Claustraphobic", 'email':"sting@example.com"},
#     {'name': "Michael Jackson", 'email':"mj@jackson.com"},
#     {'name': "Eric Morillo", 'email':"subliminal@eric.com"},
#     {'name': "Seb Fontain", 'email':"seb@fontain.com"},
#     {'name': "Britney Spears", 'email':"britany@from_london.com"},
#     {'name': "Enio Mariconne", 'email':"great_enio@mariconne.com"},
#     {'name': "Boby MacFarren", 'email':"boby_farren@example.com"},
#     {'name': "Gorge Michael", 'email':"gorgemichael@example.com"},
#     {'name': "Jichael Mackson", 'email':"jichaelMackson@junk.com"},
#     {'name': "Nick Warren", 'email':"nickwarren@warren.com"},
#     {'name': "Nick Fancully", 'email':"fancully@nick.com"},
#     {'name': "Black Madonna", 'email':"bm@london.com"},
#     {'name': "Sven Vat", 'email':"coccoon@sven.com"}
# ]
# from random import randint
# genres = ['rock','new-age','electronic','folk','techno','jazz']



#
# with Session() as sess:
#     for user in user_collection:
#         album_name = f"{user['name']}" + "".join([random.choice(string.printable) for i in range(8)])
#         one_user = User(**user) # Its interesting !!!
#         release = Release(name=album_name,release_date=str(current_time),genre=str(genres[randint(1,5)]))
#         one_user.releases.append(release)
#         sess.add(one_user)
#         sess.commit()
#
#
# #
# with Session() as sess:
#     users = sess.scalars(select(User))
#     res = users.unique()
#     for one in res:
#         print("***USER is:",one, "|  HE HAS RELEASES:",one.releases )
# # #
# with Session() as sess:
#     releases = sess.scalars(select(Release))
#     res = releases.unique()
#     for one in res:
#         print("***RELEASE author_FK is:",one)


################################################################
Session = sessionmaker(engine)
session = Session(bind=connection)
################################################################ QUERIES

#SIMPLE QUERIES
user_by_id = session.get(User,4)
# NEW SYNTAX instead of - session.query(User).get(4)
print("Here we retrieve User by ID ", user_by_id)

# QUERY - FILTER_BY - used with str expressions
user_filter_by = session.query(User).filter_by(name='Enio Mariconne').all()
print("Here we retrieve User via FILTER_BY ", user_filter_by)


# QUERY - FILTER - used with PYTHONIC expressions
username = ['Michael Jackson','Bob marley','Britney Spears']
user_filter = session.query(User).filter(User.name == username[2]).first()
print("Here we retrieve User by name with some PYTHONIC EXP", user_filter)


# JOIN QUERY with simple filtering option
joined_query = session.query(User).join(Release).filter(Release.genre == 'techno').all()
print("@_@_@Here we retrieve User and Releases JOIN", joined_query)
# HERE we're extracting releases from collection of joined query
for one in joined_query:
    print("RELEASE:", one.releases)

joined_releases = session.query(Release).join(User).filter(Release.genre == 'techno').all()
authors = [one.author for one in joined_releases]
print("*** RELEASES AND AUTHORS",joined_releases,authors)
# for one in joined_releases:
#     print("AUTHORS:", one.author)


if __name__ == '__main__':
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    print("Creating successful")


