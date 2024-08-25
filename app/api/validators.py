from http import HTTPStatus

from fastapi import HTTPException

from app.models import CharityProject


def check_project_name_duplicate(
    charity_project_name: str,
    charity_project: CharityProject,
):
    """
    Проверяет, существует ли благотворительный проект с указанным именем.
    """
    if (
        charity_project is not None and
        charity_project.name == charity_project_name
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Благотворительный проект с указанным именем уже существует'
        )


def check_project_exists(charity_project: CharityProject):
    """
    Проверяет, существует ли благотворительный проект с заданным ID.
    """
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Благотворительного проекта с таким ID не существует.',
        )


def check_the_project_has_investment(charity_project: CharityProject):
    """
    Проверяет, были ли внесены средства в благотворительный проект.
    """
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалить благотворительный проект,'
                   'в который были инвестированы средства.',
        )


def project_pre_modification_check(charity_project: CharityProject):
    """
    Проверяет, полностью ли инвестирован благотворительный проект.
    """
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Редактирование закрытого проекта невозможно!',
        )


def checks_the_new_amount_is_less_than_investments(
    new_full_amount: int,
    invested_amount: int
):
    """
    Проверяет, что новая полная сумма не меньше суммы,
    уже внесенной в качестве инвестиций.
    """
    if (
        new_full_amount is not None and
        new_full_amount < invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Новая полная сумма не может быть меньше суммы,'
                   'уже внесенной в качестве инвестиций.',
        )
