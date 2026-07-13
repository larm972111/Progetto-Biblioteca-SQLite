from enum import Enum
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
from extension import db

class ItemStatus(Enum):
    LOANED = 1
    AVAILABLE = 2
    UNAVAILABLE = 3

class VideoResolution(Enum):
    FOUR_K = "4K"
    FHD = "FHD"
    HD = "HD"

class LibraryItem(db.Model):
    __tablename__ = "libraryitem"
    item_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str]  
    title: Mapped[str]
    author: Mapped[str]
    status: Mapped[ItemStatus]= mapped_column(SQLEnum(ItemStatus), default=ItemStatus.AVAILABLE)
    user_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey('users.id'))

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "libraryitem",
    }


    def __str__(self):
        return f"Title: {self.title} Author: {self.author} Id: {self.item_id} Status: {self.status}"
        
    def __repr__(self):
        return f"{self.type.capitalize()}(id='{self.item_id}', title='{self.title}')"
        
    def borrow_item(self) -> str:
        if self.status == ItemStatus.AVAILABLE:
            self.status = ItemStatus.LOANED
            return f"The {self.type.capitalize()} {self.title} has been checked out"
        return f"Error: {self.title} has currently {self.status}"
        
    def return_item(self) -> str:
        if self.status == ItemStatus.LOANED:
            self.status = ItemStatus.AVAILABLE
            return f"The {self.type.capitalize()} {self.title} now is again available"
        return f"Error: {self.title} has currently {self.status}"


class Book(LibraryItem):
    __tablename__ = "book"
    item_id: Mapped[int] = mapped_column(db.ForeignKey("libraryitem.item_id"), primary_key=True)
    isbn: Mapped[str]
    pagnum: Mapped[int]

    __mapper_args__ = {
        "polymorphic_identity": "book",
    }
    
        
        
class Dvd(LibraryItem):
    __tablename__ = "dvd"
    item_id: Mapped[int] = mapped_column(db.ForeignKey("libraryitem.item_id"), primary_key=True)
    duration: Mapped[int]
    resolution: Mapped[VideoResolution] = mapped_column(SQLEnum(VideoResolution))

    __mapper_args__ = {
        "polymorphic_identity": "dvd",
    }
    
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"
             
    