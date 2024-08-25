from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_project_exists,
                                check_project_name_duplicate,
                                check_the_project_has_investment,
                                checks_the_new_amount_is_less_than_investments,
                                project_pre_modification_check)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.utils.investing import investment

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получает список всех благотворительных проектов.
    """
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создаёт новый благотворительный проект.

    Только для администраторов.
    """
    project = await charity_project_crud.get_project_by_name(
        charity_project.name, session
    )
    check_project_name_duplicate(charity_project.name, project)
    new_project = await charity_project_crud.create(
        charity_project,
        session=session,
        commit=False
    )
    fill_models = await donation_crud.get_unfilled(session)
    invested_list = investment(new_project, fill_models)
    await charity_project_crud.commit_objects(invested_list, session)
    await session.refresh(new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет пустой благотворительный проект по его ID.

    Только для администраторов.
    """
    project = await charity_project_crud.get(project_id, session)
    check_the_project_has_investment(project)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    charity_project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Обновляет открытый благотворительный проект по его ID.

    Только для администраторов.
    """
    project_by_id = await charity_project_crud.get(project_id, session)
    check_project_exists(project_by_id)
    project_pre_modification_check(project_by_id)
    checks_the_new_amount_is_less_than_investments(
        charity_project.full_amount, project_by_id.invested_amount
    )
    check_project_name_duplicate(charity_project.name, project_by_id)
    project_by_name = await charity_project_crud.get_project_by_name(
        charity_project.name, session
    )
    check_project_name_duplicate(charity_project.name, project_by_name)
    project = await charity_project_crud.update(
        project_by_id, charity_project, session
    )
    return project
