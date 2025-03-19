import uuid
from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import func, select, Session
from app.api.deps import CurrentUser,get_current_active_superuser, SessionDep
from app.models import (
    ProjectPublic,
    ProjectCreate,
    ProjectMember,
    Task,
    TaskPublic,
    ProjectRoleEnum,
    User,
    ProjectsPublic,
    Project,
    ProjectUpdate
)
from app.crud import (
    create_project,
    get_project_by_id,
    list_projects,
    delete_project,
    add_member_to_project,
    remove_member_from_project,
)


router = APIRouter(prefix="/projects", tags=["projects"])


# ---- PROJECT ENDPOINTS ----
@router.post("/", response_model=ProjectPublic)
def create_new_project(
    *,
    session: SessionDep,
    current_user: User = Depends(get_current_active_superuser),
    project_in: ProjectCreate
) -> Any:
    """
    Create a new project. Only superusers can create projects.
    """
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    project = create_project(session=session, name=project_in.name, description=project_in.description, owner_id=current_user.id)
    return project

@router.get("/", response_model=ProjectsPublic)
def read_projects(session: SessionDep, current_user: CurrentUser) -> Any:
    """Retrieve all projects (Only for Superusers)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    count_statement = select(func.count()).select_from(Project)
    count = session.exec(count_statement).one()
    return ProjectsPublic(data=list_projects(session=session), count=count)


@router.get("/{project_id}", response_model=ProjectPublic)
def read_project(session: SessionDep, current_user: CurrentUser, project_id: uuid.UUID) -> Any:
    """Retrieve a single project by ID."""
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
def remove_project(session: SessionDep, current_user: CurrentUser, project_id: uuid.UUID) -> Any:
    """Delete a project. Only the project owner or superuser can delete."""
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    delete_project(session=session, project_id=project_id)
    return {"message": "Project deleted successfully"}


# ---- PROJECT MEMBERS ENDPOINTS ----
@router.post("/{project_id}/members", response_model=ProjectMember)
def add_member(
    session: SessionDep, current_user: CurrentUser, project_id: uuid.UUID, user_id: uuid.UUID, role: ProjectRoleEnum
) -> Any:
    """Add a member to a project. Only Managers and Owners can add members."""
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return add_member_to_project(session=session, project_id=project_id, user_id=user_id, role=role)


@router.delete("/{project_id}/members/{user_id}")
def remove_member(session: SessionDep, current_user: CurrentUser, project_id: uuid.UUID, user_id: uuid.UUID) -> Any:
    """Remove a member from a project. Only project owners can remove members."""
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    removed = remove_member_from_project(session=session, project_id=project_id, user_id=user_id)
    if not removed:
        raise HTTPException(status_code=404, detail="User not found in project")

    return {"message": "User removed successfully"}

@router.patch(
    "/{project_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProjectPublic,
)
def update_project(
    *,
    session: SessionDep,
    project_id: uuid.UUID,
    project_in: ProjectUpdate,
) -> Any:
    """
    Update a project.
    """
    # Retrieve the existing project
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="The project with this ID does not exist in the system",
        )

    # Update the project's attributes
    project_data = project_in.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)

    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


# Endpoint to retrieve tasks by project ID
@router.get("/{project_id}/tasks/", response_model=List[TaskPublic])
def get_tasks_by_project_id(
    *, session: SessionDep, project_id: uuid.UUID
) -> List[TaskPublic]:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    return tasks