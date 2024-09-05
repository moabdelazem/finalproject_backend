from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.services.dependencies import create_access_token, verify_password
from app.db.database import get_db
from app.models import User
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create a new APIRouter instance
router = APIRouter()

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

print(SECRET_KEY)



# Password hashing functions
def get_password_hash(password):
    """
    Generates a hash for the given password.

    Parameters:
    password (str): The password to be hashed.

    Returns:
    str: The hashed password.
    """
    return pwd_context.hash(password)


#  Verify the password
def verify_password(plain_password, hashed_password):
    """
    Verify if a plain password matches a hashed password.

    Parameters:
    - plain_password (str): The plain password to be verified.
    - hashed_password (str): The hashed password to compare against.

    Returns:
    - bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Create an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates an access token based on the provided data and expiration delta.

    Parameters:
        data (dict): The data to be encoded in the access token.
        expires_delta (timedelta, optional): The expiration delta for the access token. If not provided, a default expiration of 15 minutes will be used.

    Returns:
        str: The generated access token.

    """
    # Create a copy of the data to encode
    to_encode = data.copy()
    # Add an expiration time to the token
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        # Default expiration time is 15 minutes
        expire = datetime.now() + timedelta(minutes=15)
    # Update the data with the expiration time
    to_encode.update({"exp": expire})
    # Encode the data using the JWT library
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Authenticate the user
def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticates a user by checking if the provided username and password match a user in the database.

    Args:
        db (Session): The database session.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        Union[bool, User]: Returns the authenticated user if the username and password match, otherwise returns False.
    """
    # Query the database for a user with the provided username
    user = db.query(User).filter(User.username == username).first()
    # If the user does not exist or the password is incorrect, return False
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The newly registered user.

    Raises:
        HTTPException: If the email or username is already registered.
    """
    # Check if the email and username is already registered
    existing_email = db.query(User).filter(User.email == email).first()
    existing_username = db.query(User).filter(User.username == username).first()
    # If the email is already registered, raise an HTTPException
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # If the email is already registered, raise an HTTPException
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    # Hash the password
    hashed_password = get_password_hash(password)
    # Create a new user from the provided data
    user = User(username=username, email=email, hashed_password=hashed_password)
    # Add the user to the database
    db.add(user)
    # Commit the transaction
    db.commit()
    # Refresh the user object
    db.refresh(user)
    return user


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    try:
        # Query the database for the user
        user = db.query(User).filter(User.username == username).first()
        # Check if user exists and if the password is correct
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create an access token for the authenticated user
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "is_admin": user.is_admin},
            expires_delta=access_token_expires,
        )

        # Return the access token
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/")
def create_user(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    """
    Create a new user with the provided username, email, and password.
    Parameters:
        - username (str): The username of the user.
        - email (str): The email address of the user.
        - password (str): The password of the user.
        - db (Session, optional): The database session. Defaults to Depends(get_db).
    Returns:
        - user: The created user object.
    """
    password = get_password_hash(password)
    user = User(username=username, email=email, hashed_password=password, is_admin=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}")
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Reads a user from the database based on the provided user ID.

    Parameters:
    - user_id (int): The ID of the user to be retrieved from the database.
    - db (Session): The database session.
    - current_user (dict): The current user making the request.

    Returns:
    - User: The user object retrieved from the database.

    Raises:
    - HTTPException: If the user with the provided ID is not found in the database.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all users from the database.

    Parameters:
    - db (Session): The database session.

    Returns:
    - List[User]: A list of all users in the database.
    """
    users = db.query(User).all()
    return users


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user from the database based on the provided user ID.

    Parameters:
    - user_id (int): The ID of the user to be deleted.
    - db (Session): The database session.

    Returns:
    - str: A message indicating that the user has been deleted.

    Raises:
    - HTTPException: If the user with the provided ID is not found in the database.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
