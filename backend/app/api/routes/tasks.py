import uuid
from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import func, select, Session
from app.api.deps import CurrentUser,get_current_active_superuser, SessionDep
from app.models import (
    ProjectMember,
    Task,
    TaskPublic,
    TasksPublic,
    TaskCreate,
    TaskUpdate,
    TaskComment,
)
from app.crud import (
    create_task,
    get_task_by_id,
    update_task_status,
    delete_task,
    add_task_comment,
    get_comments_for_task,
    get_project_by_id,
    list_tasks
)


router = APIRouter(prefix="/tasks", tags=["tasks"])

# ---- TASK ENDPOINTS ----
@router.get("/", response_model=TasksPublic)
def read_projects(session: SessionDep, current_user: CurrentUser) -> Any:
    """Retrieve all tasks."""
    
    count_statement = select(func.count()).select_from(Task)
    count = session.exec(count_statement).one()
    return TasksPublic(data=list_tasks(session=session), count=count)


@router.post("/{project_id}", response_model=TaskPublic)
def create_new_task(session: SessionDep, current_user: CurrentUser, project_id: uuid.UUID, task_in: TaskCreate) -> Any:
    """Create a task in a project. Only project owners or managers can create tasks."""
    project = get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return create_task(session=session, project_id=project_id, **task_in.dict())


@router.put("/{task_id}", response_model=TaskPublic)
def update_task(session: SessionDep, current_user: CurrentUser, task_id: uuid.UUID, task_in: TaskUpdate) -> Any:
    """Update task details. Only project managers or assigned users can update."""
    task = get_task_by_id(session=session, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.assigned_member_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    task.title = task_in.title or task.title
    task.description = task_in.description or task.description
    task.status = task_in.status or task.status
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def remove_task(session: SessionDep, current_user: CurrentUser, task_id: uuid.UUID) -> Any:
    """Delete a task. Only the project owner or managers can delete tasks."""
    task = get_task_by_id(session=session, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    delete_task(session=session, task_id=task_id)
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/assign", response_model=Task)
def assign_task(
    *,
    session: SessionDep,
    task_id: uuid.UUID,
    assigned_member_id: uuid.UUID
) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project_member = session.get(ProjectMember, assigned_member_id)
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    if project_member.project_id != task.project_id:
        raise HTTPException(status_code=400, detail="Project member does not belong to the same project as the task")

    task.assigned_member_id = assigned_member_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.patch("/{task_id}/unassign", response_model=Task)
def unassign_task(
    *,
    session: SessionDep,
    task_id: uuid.UUID
) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.assigned_member_id = None
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# ---- TASK COMMENTS ENDPOINTS ----
@router.post("/{task_id}/comments", response_model=TaskComment)
def add_comment(session: SessionDep, current_user: CurrentUser, task_id: uuid.UUID, content: str) -> Any:
    """Add a comment to a task. Any user in the project can comment."""
    task = get_task_by_id(session=session, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return add_task_comment(session=session, task_id=task_id, author_id=current_user.id, content=content)


@router.get("/{task_id}/comments", response_model=List[TaskComment])
def get_task_comments(session: SessionDep, current_user: CurrentUser, task_id: uuid.UUID) -> Any:
    """Retrieve all comments for a task."""
    task = get_task_by_id(session=session, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return get_comments_for_task(session=session, task_id=task_id)

@router.patch(
    "/{task_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=TaskPublic,
)
def update_task(
    *,
    session: SessionDep,
    task_id: uuid.UUID,
    task_in: TaskUpdate,
) -> Any:
    """db_task
    Update a project.
    """
    # Retrieve the existing project
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="The task with this ID does not exist in the system",
        )

    # Update the project's attributes
    task_data = task_in.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
