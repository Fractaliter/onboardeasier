import uuid
from typing import Any, List, Optional
from datetime import datetime
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    Item, ItemCreate, User, UserCreate, UserUpdate,
    Project,
    ProjectMember,
    Task,
    TaskComment,
    TaskStatusEnum,
    ProjectRoleEnum
)

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# ---- PROJECT CRUD ----
def create_project(*, session: Session, name: str, description: Optional[str], owner_id: uuid.UUID) -> Project:
    # Ensure the owner exists in the User table
    owner = session.get(User, owner_id)
    if not owner:
        raise ValueError("Project owner does not exist.")

    db_project = Project(name=name, description=description, owner_id=owner_id)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project



def get_project_by_id(*, session: Session, project_id: uuid.UUID) -> Optional[Project]:
    return session.get(Project, project_id)


def list_projects(*, session: Session) -> List[Project]:
    statement = select(Project)
    return session.exec(statement).all()


def delete_project(*, session: Session, project_id: uuid.UUID) -> bool:
    project = get_project_by_id(session=session, project_id=project_id)
    if project:
        session.delete(project)
        session.commit()
        return True
    return False


# ---- PROJECT MEMBER CRUD ----
def add_member_to_project(*, session: Session, project_id: uuid.UUID, user_id: uuid.UUID, role: ProjectRoleEnum) -> Optional[ProjectMember]:
    # Ensure the user exists before adding them to the project
    user = session.get(User, user_id)
    if not user:
        raise ValueError("User does not exist.")

    db_member = ProjectMember(project_id=project_id, user_id=user_id, role=role)
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member

def get_project_members(*, session: Session, project_id: uuid.UUID) -> List[ProjectMember]:
    statement = select(ProjectMember).where(ProjectMember.project_id == project_id)
    return session.exec(statement).all()


def remove_member_from_project(*, session: Session, project_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    statement = select(ProjectMember).where(
        (ProjectMember.project_id == project_id) & (ProjectMember.user_id == user_id)
    )
    db_member = session.exec(statement).first()
    if db_member:
        session.delete(db_member)
        session.commit()
        return True
    return False


# ---- TASK CRUD ----
def create_task(
    session: Session,
    project_id: uuid.UUID,
    title: str,
    description: Optional[str],
    assigned_member_id: Optional[uuid.UUID],
    status: TaskStatusEnum = TaskStatusEnum.PENDING  # Default value provided
) -> Task:
    db_task = Task(
        project_id=project_id,
        title=title,
        description=description,
        assigned_member_id=assigned_member_id,
        status=status  # Use the provided status
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def list_tasks(*, session: Session) -> List[Task]:
    statement = select(Task)
    return session.exec(statement).all()

def get_task_by_id(*, session: Session, task_id: uuid.UUID) -> Optional[Task]:
    return session.get(Task, task_id)


def update_task_status(*, session: Session, task_id: uuid.UUID, new_status: TaskStatusEnum) -> Optional[Task]:
    task = get_task_by_id(session=session, task_id=task_id)
    if task:
        task.status = new_status
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    return None


def delete_task(*, session: Session, task_id: uuid.UUID) -> bool:
    task = get_task_by_id(session=session, task_id=task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False


# ---- TASK COMMENT CRUD ----
def add_task_comment(*, session: Session, task_id: uuid.UUID, author_id: uuid.UUID, content: str) -> TaskComment:
    # Ensure the author exists
    author = session.get(User, author_id)
    if not author:
        raise ValueError("Author does not exist.")

    db_comment = TaskComment(task_id=task_id, author_id=author_id, content=content, created_at=datetime.utcnow())
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


def get_comments_for_task(*, session: Session, task_id: uuid.UUID) -> List[TaskComment]:
    statement = select(TaskComment).where(TaskComment.task_id == task_id)
    return session.exec(statement).all()