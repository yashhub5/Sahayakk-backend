from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey, DateTime ,func
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    address: Mapped[str] = mapped_column(String(250))
    city: Mapped[str] = mapped_column(String(250))
    pincode: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    longitude: Mapped[float] = mapped_column()
    latitude: Mapped[float] = mapped_column()


class Cooperative(Base):
    __tablename__ = "cooperatives"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(150))
    registration_number: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    address: Mapped[str] = mapped_column(String(250))
    city: Mapped[str] = mapped_column(String(100))
    pincode: Mapped[str] = mapped_column(String(10))

    contact_phone: Mapped[str] = mapped_column(String(15))
    created_at: Mapped[datetime] = mapped_column(DateTime)

class Workers(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True
    )
    cooperative_id: Mapped[int] = mapped_column(
        ForeignKey("cooperatives.id")
    )
    address: Mapped[str] = mapped_column(String(250))
    city: Mapped[str] = mapped_column(String(250))
    pincode: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    longitude: Mapped[float] = mapped_column()
    latitude: Mapped[float] = mapped_column()
    experience_years: Mapped[int] = mapped_column()
    verification_status: Mapped[str] = mapped_column(String(20))
    is_available: Mapped[bool] = mapped_column(default=True)



class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    description: Mapped[str] = mapped_column(
        String(250)
    )

    created_at: Mapped[datetime] = mapped_column(DateTime)


class WorkerSkill(Base):
    __tablename__ = "worker_skills"

    id: Mapped[int] = mapped_column(primary_key=True)

    worker_id: Mapped[int] = mapped_column(
        ForeignKey("workers.id")
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id")
    )

    experience_years: Mapped[int] = mapped_column()

    certification: Mapped[str] = mapped_column(
        String(150)
    )

    created_at: Mapped[datetime] = mapped_column(DateTime)


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id")
    )

    name: Mapped[str] = mapped_column(
        String(150)
    )

    description: Mapped[str] = mapped_column(
        String(300)
    )

    base_price: Mapped[float] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(DateTime)


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id")
    )

    worker_id: Mapped[int] = mapped_column(
        ForeignKey("workers.id")
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id")
    )

    booking_date: Mapped[datetime] = mapped_column(DateTime)

    address: Mapped[str] = mapped_column(
        String(250)
    )

    status: Mapped[str] = mapped_column(
        String(30)
    )

    total_amount: Mapped[float] = mapped_column()

    rating: Mapped[float | None] = mapped_column(
        nullable=True
    )

    review: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime)


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)

    booking_id: Mapped[int] = mapped_column(
        ForeignKey("bookings.id"),
        unique=True
    )

    amount: Mapped[float] = mapped_column()

    payment_method: Mapped[str] = mapped_column(
        String(30)
    )

    payment_status: Mapped[str] = mapped_column(
        String(30)
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(150),
        unique=True,
        nullable=True
    )

    welfare_amount: Mapped[float] = mapped_column(
        default=0
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime)

