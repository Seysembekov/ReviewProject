from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime
from database import Base


class Reviews(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    images: Mapped[str | None] = mapped_column(nullable=True)
    evaluation: Mapped[int] = mapped_column(nullable=False)
    review_on_place: Mapped[int] = mapped_column(ForeignKey('places.id'), nullable=False)
    desc: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped['Users'] = relationship('Users', back_populates='reviews')  
    place: Mapped['Places'] = relationship('Places', back_populates='reviews')