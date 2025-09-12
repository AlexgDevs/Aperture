from datetime import datetime, timezone

from .. import Base

from . import Mapped, mapped_column

from sqlalchemy import String, Boolean

class ClickStatistics(Base):
    __tablename__ = 'click_statistics'
    
    short_code: Mapped[str] = mapped_column(String(10))
    endpoint_type: Mapped[str] = mapped_column(String(20))  
    hidden_ip: Mapped[str] = mapped_column(String(50))  
    hashed_user: Mapped[str] = mapped_column(String(64))
    browser: Mapped[str] = mapped_column(String(100), nullable=True)
    browser_version: Mapped[str] = mapped_column(String(50), nullable=True)
    os: Mapped[str] = mapped_column(String(100), nullable=True)
    os_version: Mapped[str] = mapped_column(String(50), nullable=True)
    device: Mapped[str] = mapped_column(String(100), nullable=True)
    is_mobile: Mapped[bool] = mapped_column(Boolean, default=False)
    is_tablet: Mapped[bool] = mapped_column(Boolean, default=False)
    is_pc: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False)
    accept_language: Mapped[str] = mapped_column(String(100), nullable=True)