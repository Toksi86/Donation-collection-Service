from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        return (await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )).scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        query = (
            select(CharityProject)
            .where(
                CharityProject.fully_invested.is_(True),
                CharityProject.close_date.isnot(None)
            )
            .order_by(
                func.julianday(CharityProject.close_date) -
                func.julianday(CharityProject.create_date)
            )
        )

        result_proxy = await session.execute(query)
        charityprojects = result_proxy.scalars().all()
        return charityprojects


charity_project_crud = CRUDCharityProject(CharityProject)
