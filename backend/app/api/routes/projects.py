import uuid
from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import func, select, Session
from app.api.deps import CurrentUser, SessionDep
from app.models import (
    ProjectPublic,
    ProjectMember,
    TaskPublic,
    TaskComment,
    TaskStatusEnum,
    ProjectRoleEnum,
)
from app.crud import (
    create_project,
    get_project_by_id,
    list_projects,
    delete_project,
    add_member_to_project,
    get_project_members,
    remove_member_from_project,
    create_task,
    get_task_by_id,
    update_task_status,
    delete_task,
    add_task_comment,
    get_comments_for_task,
)


router = APIRouter(prefix="/projects", tags=["projects"])


# ---- PROJECT ENDPOINTS ----
@router.post("/", response_model=ProjectPublic)
def create_new_project(
    session: SessionDep, current_user: CurrentUser, name: str, description: Optional[str] = None
) -> Any:
    """
    Create a new project. Only Managers and above can create projects.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Only managers can create projects")

    project = create_project(session=session, name=name, description=description, owner_id=current_user.id)
    return project


@router.get("/", response_model=List[ProjectPublic])
def read_projects(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Retrieve all projects (Only for Superusers).
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    projects = list_projects(session=session)
    return projects


@router.delete("/{project_id}", response_model=ProjectPublic)
def remove_project(session: SessionDep, current_user: CurrentUser, project_id: uuid.UUID) -> Any:
    """
    Delete a project. Only the project owner or superuser can delete.
    """
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    delete_project(session=session, project_id=project_id)
    return project


# ---- PROJECT MEMBERS ENDPOINTS ----
@router.post("/{project_id}/members", response_model=ProjectMember)
def add_member(
    session: SessionDep,
    current_user: CurrentUser,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
    role: ProjectRoleEnum,
) -> Any:
    """
    Add a member to a project. Only Managers and Owners can add members.
    """
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return add_member_to_project(session=session, project_id=project_id, user_id=user_id, role=role)


@router.delete("/{project_id}/members/{user_id}")
def remove_member(
    session: SessionDep, current_user: CurrentUser, project_id: uuid.UUID, user_id: uuid.UUID
) -> Any:
    """
    Remove a member from a project. Only project owners can remove members.
    """
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    removed = remove_member_from_project(session=session, project_id=project_id, user_id=user_id)
    if not removed:
        raise HTTPException(status_code=404, detail="User not found in project")

    return {"message": "User removed successfully"}


# ---- TASK ENDPOINTS ----
@router.post("/{project_id}/tasks", response_model=TaskPublic)
def create_new_task(
    session: SessionDep,
    current_user: CurrentUser,
    project_id: uuid.UUID,
    title: str,
    description: Optional[str] = None,
    assigned_member_id: Optional[uuid.UUID] = None,
) -> Any:
    """
    Create a task in a project. Only project owners or managers can create tasks.
    """
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return create_task(session=session, project_id=project_id, title=title, description=description, assigned_member_id=assigned_member_id)


@router.put("/tasks/{task_id}/status", response_model=TaskPublic)
def update_task(
    session: SessionDep,
    current_user: CurrentUser,
    task_id: uuid.UUID,
    new_status: TaskStatusEnum,
) -> Any:
    """
    Update task status. Only the assigned user or project managers can update status.
    """
    task = get_task_by_id(session=session, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.assigned_member_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return update_task_status(session=session, task_id=task_id, new_status=new_status)


@router.delete("/tasks/{task_id}")
def remove_task(session: SessionDep, current_user: CurrentUser, task_id: uuid.UUID) -> Any:
    """
    Delete a task. Only the project owner or managers can delete tasks.
    """
    task = get_task_by_id(session=session, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    delete_task(session=session, task_id=task_id)
    return {"message": "Task deleted successfully"}


# ---- TASK COMMENTS ENDPOINTS ----
@router.post("/tasks/{task_id}/comments", response_model=TaskComment)
def add_comment(
    session: SessionDep,
    current_user: CurrentUser,
    task_id: uuid.UUID,
    content: str,
) -> Any:
    """
    Add a comment to a task. Any user in the project can comment.
    """
    task = get_task_by_id(session=session, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return add_task_comment(session=session, task_id=task_id, author_id=current_user.id, content=content)


@router.get("/tasks/{task_id}/comments", response_model=List[TaskComment])
def get_task_comments(session: SessionDep, current_user: CurrentUser, task_id: uuid.UUID) -> Any:
    """
    Retrieve all comments for a task.
    """
    task = get_task_by_id(session=session, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return get_comments_for_task(session=session, task_id=task_id)
