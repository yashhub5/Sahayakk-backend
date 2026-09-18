from pydantic import BaseModel
from fastapi import FastAPI
from database import SessionLocal
from models import User, Service , Skill , Workers , Cooperative , Booking , Customer , Payment
from datetime import datetime

def get_db():
    db = SessionLocal()
    return db

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str
class CustomerCreate(BaseModel):
    user_id: int
    address: str
    city: str
    pincode: str
    longitude: float
    latitude: float


class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(user: LoginRequest):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user is None:
       return {"message": "User not found"}
    if db_user.password_hash != user.password:
        return {"message": "Incorrect password"}
    return {
    "message": "Login successful",
    "user_id": db_user.id,
    "role": db_user.role
}


@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()

    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password_hash=user.password,
        role=user.role,
        created_at=datetime.now()
    )

    db.add(db_user)
    db.commit()

    return {"message": "Database session created"}

class ServiceCreate(BaseModel):
    skill_id: int
    name: str
    description: str
    base_price: float

@app.post("/customers")
def create_customer(customer: CustomerCreate):
    db = SessionLocal()

    db_customer = Customer(
        user_id=customer.user_id,
        address=customer.address,
        city=customer.city,
        pincode=customer.pincode,
        longitude=customer.longitude,
        latitude=customer.latitude,
        created_at=datetime.now()
    )

    db.add(db_customer)
    db.commit()

    return {"message": "Customer created successfully"}

@app.post("/services")
def create_service(service: ServiceCreate):
    db = SessionLocal()

    db_service = Service(
    skill_id=service.skill_id,
    name=service.name,
    description=service.description,
    base_price=service.base_price,
    created_at=datetime.now()
)

    db.add(db_service)
    db.commit()
    return {"message": "Service created successfully"}


class SkillCreate(BaseModel):
    name: str
    description: str

@app.post("/skills")
def create_skill(skill: SkillCreate):
    db = SessionLocal()
    db_skill = Skill(
    name=skill.name,
    description=skill.description,
    created_at=datetime.now()
)
    db.add(db_skill)
    db.commit()
    return {"message": "Skill created successfully"}


class WorkerCreate(BaseModel):
    user_id: int
    cooperative_id: int
    address: str
    city: str
    pincode: str
    latitude: float
    longitude: float
    experience_years: int

@app.post("/workers")
def create_worker(worker: WorkerCreate):
    db = SessionLocal()
    db_worker = Workers(
    user_id=worker.user_id,
    cooperative_id=worker.cooperative_id,
    address=worker.address,
    city=worker.city,
    pincode=worker.pincode,
    latitude=worker.latitude,
    longitude=worker.longitude,
    experience_years=worker.experience_years,
    verification_status="pending",
    created_at=datetime.now()
)
    db.add(db_worker)
    db.commit()
    return {"message": "Worker created successfully"}

class BookingCreate(BaseModel):
    customer_id: int
    worker_id: int
    service_id: int
    booking_date: datetime
    address: str

class CooperativeCreate(BaseModel):
    name: str
    registration_number: str
    address: str
    city: str
    pincode: str
    contact_phone: str

@app.post("/cooperatives")
def create_cooperative(cooperative: CooperativeCreate):
    db = SessionLocal()
    db_cooperative = Cooperative(
    name=cooperative.name,
    registration_number=cooperative.registration_number,
    address=cooperative.address,
    city=cooperative.city,
    pincode=cooperative.pincode,
    contact_phone=cooperative.contact_phone,
    created_at=datetime.now()
)
    db.add(db_cooperative)
    db.commit()
    return {"message": "Cooperative created successfully"}

@app.get("/skills")
def get_skills():
    db = SessionLocal()

    skills = db.query(Skill).all()

    return skills

@app.get("/services")
def get_services():
    db = SessionLocal()

    services = db.query(Service).all()

    return services

@app.get("/workers")
def get_workers():
    db = SessionLocal()

    workers = db.query(Workers).all()

    return workers

@app.get("/skills/{skill_id}")
def get_skill(skill_id: int):
    db = SessionLocal()

    skill = db.query(Skill).filter(Skill.id == skill_id).first()

    return skill

@app.get("/services/{service_id}")
def get_service(service_id: int):
    db = SessionLocal()

    service = db.query(Service).filter(Service.id == service_id).first()

    return service


@app.get("/workers/{worker_id}")
def get_worker(worker_id: int):
    db = SessionLocal()

    worker = db.query(Workers).filter(Workers.id == worker_id).first()

    return worker

@app.post("/bookings")
def create_booking(booking: BookingCreate):
    db = SessionLocal()

    db_booking = Booking(
        customer_id=booking.customer_id,
        worker_id=booking.worker_id,
        service_id=booking.service_id,
        booking_date=booking.booking_date,
        address=booking.address,
        status="pending",
        total_amount=500,
        created_at=datetime.now()
    )

    db.add(db_booking)
    db.commit()

    return {"message": "Booking created successfully"}

class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    payment_method: str

@app.post("/payments")
def create_payment(payment: PaymentCreate):
    db = SessionLocal()

    db_payment = Payment(
        booking_id=payment.booking_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        payment_status="success",
        transaction_id=None,
        welfare_amount=0,
        paid_at=datetime.now(),
        created_at=datetime.now()
    )

    db.add(db_payment)
    db.commit()

    return {"message": "Payment successful"}


class RatingCreate(BaseModel):
    rating: float
    review: str

@app.put("/bookings/{booking_id}/rating")
def add_rating(booking_id: int, rating_data: RatingCreate):
    db = SessionLocal()

    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    booking.rating = rating_data.rating
    booking.review = rating_data.review

    db.commit()

    return {"message": "Rating and review added successfully"}


@app.get("/customers/{customer_id}/bookings")
def get_customer_bookings(customer_id: int):
    db = SessionLocal()

    bookings = db.query(Booking).filter(
        Booking.customer_id == customer_id
    ).all()

    return bookings

@app.get("/workers/{worker_id}/bookings")
def get_worker_bookings(worker_id: int):
    db = SessionLocal()

    bookings = db.query(Booking).filter(
        Booking.worker_id == worker_id
    ).all()

    return bookings

@app.put("/bookings/{booking_id}/accept")
def accept_booking(booking_id: int):
    db = SessionLocal()

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    booking.status = "accepted"

    db.commit()

    return {"message": "Booking accepted successfully"}

@app.put("/bookings/{booking_id}/complete")
def complete_booking(booking_id: int):
    db = SessionLocal()

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    booking.status = "completed"

    db.commit()

    return {"message": "Booking completed successfully"}