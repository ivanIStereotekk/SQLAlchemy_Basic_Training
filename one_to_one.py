from datetime import datetime
from sqlalchemy import ForeignKey, String,select
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped,joinedload
from  sqlalchemy.orm import mapped_column
from typing import  List, Optional
from sqlalchemy import create_engine

current_time = datetime.now().time()



engine = create_engine("sqlite:///ewan_data.db",echo=True)

connection = engine.connect()



class Base(DeclarativeBase):
    pass


class User(Base):
    """" User ORM model"""
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(20))
    releases: Mapped[List["Release"]] = relationship(back_populates="author",lazy="joined",uselist=True,secondary="proxy")
    def __repr__(self) -> str:
        return f"USER-ID={self.id}  |  USER-NAME={self.name} |   USER-EMAIL={self.email} "




class Release(Base):
    """Release ORM model"""
    __tablename__ = 'release'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    release_date: Mapped[str] = mapped_column(String(100))
    author_fk: Mapped[List[int]] = mapped_column(ForeignKey('user.id')) # Here we define column trough - __tablename__ = 'user'
    author: Mapped["User"] = relationship(back_populates="releases",uselist=True,lazy="joined",secondary="proxy")
    def __repr__(self) -> str:
        return f"RELEASE-NAME={self.name} | RELEASE-ID={self.id}"






#https://youtu.be/Uym2DHnUEno?list=PLLAleBnw-fxzlVNyIylLbRdsj3zLHogoL tutorial

Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker
import random
import string
import secrets


Session = sessionmaker(engine)
#
with Session() as sess:
    user = User(name="OneUser", email="oneuser@jjj.com")
    user_two = User(name="TwoUser", email="twouser@xxx.com")
    release_one = Release(name="ThirdAlbum", release_date=str(current_time))
    release_two = Release(name="FourthAlbum", release_date=str(current_time))
    user.releases.append(release_one)
    user_two.releases.append(release_two)
    sess.add_all([user_two,user])
    sess.commit()


# Пример джоина
# stmt = select(User).options(joinedload(User.addresses)).filter_by(name="spongebob")
# >>> spongebob = session.scalars(stmt).unique().all()

# with Session() as sess:
#     rels = sess.scalars(select(ProxyRelation))
#     res = rels.unique()
#     for one in res:
#         print("## PROXY's:",one)
#
#
# with Session() as sess:
#     users = sess.scalars(select(User))
#     res = users.unique()
#     for one in res:
#         print("***USER is:",one, "|  HE HAS RELEASES:",one.releases )
# #
# with Session() as sess:
#     releases = sess.scalars(select(Release))
#     res = releases.unique()
#     for one in res:
#         print("***RELEASE author_FK is:",one)







# not so good - https://youtu.be/kFp9fdv9i_I?list=PLN0sMOjX-lm5Pz5EeX1rb3yilzMNT6qLM


#   this !!! Ruslan dev ---- https://www.youtube.com/watch?v=jTnlne2iw00&list=PLWQhUNXl0Lng1gQsizF2fBT8aF5qy3kWS




if __name__ == '__main__':
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    print("Creating successful")


