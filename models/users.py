from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    hashpass: Mapped[str] = mapped_column(String(256), nullable=False)


    reviews: Mapped[list['Reviews']] = relationship('Reviews', back_populates='user')
    favorites: Mapped[list['Favorites']] = relationship('Favorites', back_populates='user')

