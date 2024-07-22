import pytest
from sqlalchemy.orm import Session

from application.core.users.exceptions import UserEmailNotFound, UserIdNotFound
from application.core.users.serializers import UserCreate
from application.database.models.users import UserOrm
from application.database.repositories.users import UserRepository


def test_insert_user_data_adds_row_to_db(session: Session) -> None:
    user_to_insert = UserCreate(
        email="test@test.com",
        password="R@nd0mP@ssw0rd",
        first_name="first_name",
        last_name="last_name",
    )

    user_repository = UserRepository(session=session)
    user = user_repository.insert_user(user_to_insert=user_to_insert)
    user_orms = session.query(UserOrm).all()
    assert len(user_orms) == 1
    user_orm = user_orms[0]
    assert user_orm.id == user.id
    assert user_orm.email == user.email == user_to_insert.email
    assert user_orm.password == user_to_insert.password


def test_get_user_by_email_returns_user_when_user_email_exists(
    session: Session,
) -> None:
    user_email = "test@test.com"
    user_to_insert = UserCreate(
        email=user_email,
        first_name="first_name",
        last_name="last_name",
        password="R@nd0mP@ssw0rd",
    )
    session.add(UserOrm(**user_to_insert.dict()))
    session.commit()

    user_repository = UserRepository(session=session)

    user = user_repository.get_user_by_email(user_email=user_email)

    assert user.email == user_email


def test_get_user_by_email_raises_error_when_user_email_doesnt_exist(
    session: Session,
) -> None:
    user_repository = UserRepository(session=session)

    with pytest.raises(UserEmailNotFound):
        user_repository.get_user_by_email(user_email="test@test.com")


def test_get_user_by_id_returns_user_when_user_id_exists(session: Session) -> None:
    user_email = "test@test.com"
    user_to_insert = UserCreate(
        email=user_email,
        first_name="first_name",
        last_name="last_name",
        password="R@nd0mP@ssw0rd",
    )
    user_orm = UserOrm(**user_to_insert.dict())
    session.add(user_orm)
    session.commit()
    session.refresh(user_orm)

    user_repository = UserRepository(session=session)

    user = user_repository.get_user_by_id(user_id=user_orm.id)

    assert user.id == user_orm.id
    assert user.email == user_to_insert.email


def test_get_user_by_id_raises_error_when_user_id_doesnt_exist(
    session: Session,
) -> None:
    user_repository = UserRepository(session=session)

    with pytest.raises(UserIdNotFound):
        user_repository.get_user_by_id(user_id=1)


def test_password_is_changed_after_update_password_is_called(session: Session) -> None:
    user_email = "test@test.com"
    user_to_insert = UserCreate(
        email=user_email,
        first_name="first_name",
        last_name="last_name",
        password="R@nd0mP@ssw0rd",
    )
    user_orm = UserOrm(**user_to_insert.dict())
    session.add(user_orm)
    session.commit()
    session.refresh(user_orm)

    user_repository = UserRepository(session=session)

    new_password = "TEST"
    user_repository.update_password(user_id=user_orm.id, new_password=new_password)
    assert (
        session.query(UserOrm.password).filter_by(id=user_orm.id).one()[0]
        == new_password
    )
