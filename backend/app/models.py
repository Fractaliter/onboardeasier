import uuid
from datetime import datetime
from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional


# ---- USER BASE ----
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = Field(default=None, max_length=255)


# ---- USER MODELS ----
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: Optional[str] = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[EmailStr] = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

    # Relationships
    items: List["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    project_memberships: List["ProjectMember"] = Relationship(back_populates="user")


# ---- USER PUBLIC RESPONSE ----
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: List[UserPublic]
    count: int


# ---- ITEMS ----
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)


class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User = Relationship(back_populates="items")


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: List[ItemPublic]
    count: int


# ---- MESSAGES & TOKENS ----
class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: Optional[str] = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# ---- ENUMS ----
class ProjectRoleEnum(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    VIEWER = "viewer"


class TaskStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# ---- PROJECT ----
class ProjectBase(SQLModel):
    name: str = Field(unique=True, index=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)


class Project(ProjectBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")  # 🔥 Fixed FK

    # Relationships
    owner: User = Relationship()
    members: List["ProjectMember"] = Relationship(back_populates="project")
    tasks: List["Task"] = Relationship(back_populates="project")


# ---- PROJECT MEMBERS ----
class ProjectMember(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    project_id: uuid.UUID = Field(foreign_key="project.id", nullable=False, ondelete="CASCADE")
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")  # 🔥 Fixed FK
    role: ProjectRoleEnum = Field(default=ProjectRoleEnum.EMPLOYEE)

    # Relationships
    project: Project = Relationship(back_populates="members")
    user: User = Relationship(back_populates="project_memberships")


# ---- TASKS ----
class TaskBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=500)
    status: TaskStatusEnum = Field(default=TaskStatusEnum.PENDING)


class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=500)
    status: TaskStatusEnum = Field(default=TaskStatusEnum.PENDING)

    project_id: uuid.UUID = Field(foreign_key="project.id", nullable=False, ondelete="CASCADE")
    assigned_member_id: Optional[uuid.UUID] = Field(foreign_key="projectmember.id", default=None, nullable=True, ondelete="SET NULL")

    project: Project = Relationship(back_populates="tasks")
    assigned_member: Optional[ProjectMember] = Relationship()

    comments: List["TaskComment"] = Relationship(back_populates="task")


# ---- TASK COMMENTS ----
class TaskComment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: uuid.UUID = Field(foreign_key="task.id", nullable=False, ondelete="CASCADE")
    author_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")  # 🔥 Fixed FK
    content: str = Field(max_length=1000)
    created_at: datetime = Field(default=datetime.utcnow)

    task: Task = Relationship(back_populates="comments")
    author: User = Relationship()


# ---- PUBLIC SCHEMAS ----
class ProjectPublic(SQLModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    owner_id: uuid.UUID


class TaskPublic(SQLModel):
    id: uuid.UUID
    title: str
    status: TaskStatusEnum
    project_id: uuid.UUID
    assigned_member_id: Optional[uuid.UUID]
