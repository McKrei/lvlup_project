from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship
import enum

from database.database import Base


class TransactionType(enum.Enum):
    Buy = "Buy"
    Sell = "Sell"
    Dividend = "Dividend"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    asset_types = relationship("AssetType", back_populates="user")
    portfolios = relationship("Portfolio", back_populates="user")

    def __str__(self):
        return f"User: {self.username} Email: {self.email} ID: {self.id}"


class AssetType(Base):
    __tablename__ = "asset_type"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="asset_types")
    assets = relationship("Asset", back_populates="asset_type")


class Portfolio(Base):
    __tablename__ = "portfolio"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="portfolios")
    assets = relationship("Asset", back_populates="portfolio")


class Asset(Base):
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Float)
    purchase_price = Column(Float)
    current_price = Column(Float)
    commission = Column(Float)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    asset_type_id = Column(Integer, ForeignKey("asset_type.id"))
    portfolio = relationship("Portfolio", back_populates="assets")
    asset_type = relationship("AssetType", back_populates="assets")
    transactions = relationship("Transaction", back_populates="asset")


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(TransactionType))
    created_at = Column(DateTime, default=datetime.now)
    quantity = Column(Float)
    price = Column(Float)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    asset = relationship("Asset", back_populates="transactions")
