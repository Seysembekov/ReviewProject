from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database import Base


class Places(Base):
    __tablename__ = 'places'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    media: Mapped[str | None] = mapped_column(nullable=True)

    reviews: Mapped[list['Reviews']] = relationship('Reviews', back_populates='place')
    favorites: Mapped[list['Favorites']] = relationship('Favorites', back_populates='place')
