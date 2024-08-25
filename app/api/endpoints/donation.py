from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationAdminDB, DonationCreate, DonationDB
from app.utils.investing import investment

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationAdminDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получает список всех пожертвований.

    Только для администраторов.
    """
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Создает новое пожертвование.

    Примечания: \n
        - Функция создает новое пожертвование. \n
        - Созданное пожертвование добавляется в сессию базы данных.\n
        - Получает списка объектов, которые не полностью инвестированы.\n
        - Вызывается функция `investment` для инвестирования.\n
        - Список инвестированных объектов фиксируется в базе данных.\n
        - Сессия базы данных обновляется.\n
        - Созданное пожертвование возвращается.
    """
    new_donation = await donation_crud.create(
        donation,
        user=user,
        session=session,
        commit=False
    )
    fill_models = await charity_project_crud.get_unfilled(session)
    invested_list = investment(new_donation, fill_models)
    await donation_crud.commit_objects(invested_list, session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDB],
    dependencies=[Depends(current_user)],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Возвращает список пожертвований, сделанных текущим пользователем.
    """
    return await donation_crud.get_by_user(session, user)
