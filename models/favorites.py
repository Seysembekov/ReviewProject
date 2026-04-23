from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base
from sqlalchemy import UniqueConstraint


class Favorites(Base):
    __tablename__ = 'favorites'
    __table_args__ = (UniqueConstraint('user_id', 'place_id', name= 'uq_user_place_fav'))

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    place_id: Mapped[int] = mapped_column(ForeignKey('places.id'), nullable=False)

    user: Mapped['Users'] = relationship('Users', back_populates='favorites')
    place: Mapped['Places'] = relationship('Places', back_populates='favorites')