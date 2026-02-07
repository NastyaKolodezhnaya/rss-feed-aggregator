from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100))  # todo: add email validation here
    password_hash: Mapped[bytes]

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.name!r}, email={self.email!r})'


# class Address(Base):
#     from typing import List
#     from typing import Optional
#     from sqlalchemy import ForeignKey__tablename__ = "address"
#     from sqlalchemy.orm import relationship
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")
#
#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
