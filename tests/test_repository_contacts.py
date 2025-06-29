import pytest
from unittest.mock import MagicMock
from datetime import date, timedelta

from src.repository import contacts as contact_repo
from src.database.models import Contact, User
from src.schemas.contacts import ContactCreate, ContactUpdate


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_user():
    return User(id=1, email="test@example.com")


def test_get_contacts(mock_db, mock_user):
    expected = [Contact(id=1), Contact(id=2)]
    mock_db.query().filter().all.return_value = expected

    result = contact_repo.get_contacts(mock_db, user_id=mock_user.id)

    assert result == expected


def test_create_contact(mock_db, mock_user):
    data = ContactCreate(
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        phone_number="123456789",
        birthday=date(1990, 5, 20),
        additional_info="Friend"
    )

    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    result = contact_repo.create_contact(mock_db, data, user_id=mock_user.id)

    assert result.user_id == mock_user.id
    assert result.first_name == "Alice"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_get_contact(mock_db, mock_user):
    contact = Contact(id=1, user_id=mock_user.id)
    mock_db.query().filter().first.return_value = contact

    result = contact_repo.get_contact(mock_db, 1, mock_user.id)

    assert result == contact


def test_update_contact(mock_db, mock_user):
    contact = Contact(id=1, user_id=mock_user.id, first_name="OldName")
    mock_db.query().filter().first.return_value = contact

    update_data = ContactUpdate(first_name="NewName")

    result = contact_repo.update_contact(mock_db, 1, update_data, mock_user.id)

    assert result.first_name == "NewName"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_delete_contact(mock_db, mock_user):
    contact = Contact(id=1, user_id=mock_user.id)
    mock_db.query().filter().first.return_value = contact

    result = contact_repo.delete_contact(mock_db, 1, mock_user.id)

    assert result == contact
    mock_db.delete.assert_called_once_with(contact)
    mock_db.commit.assert_called_once()


def test_search_contacts(mock_db, mock_user):
    results = [Contact(id=1, email="test@example.com")]
    mock_db.query().filter().all.return_value = results

    result = contact_repo.search_contacts(mock_db, "test", mock_user.id)

    assert result == results


def test_get_upcoming_birthdays(mock_db, mock_user):
    today = date.today()
    next_week = today + timedelta(days=5)
    contact = Contact(id=1, user_id=mock_user.id, birthday=next_week)

    mock_db.query().filter().all.return_value = [contact]

    result = contact_repo.get_upcoming_birthdays(mock_db, mock_user.id)

    assert contact in result
