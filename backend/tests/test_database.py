import pytest
from datetime import date
from app.models import User, Group, Event, Category
from app.models.user import user_interests, event_attendees, group_members


class TestUserModel:
    """Test User model and relationships."""

    def test_create_user(self, db):
        """Test creating a user."""
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User",
            location="San Francisco"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.member_since is not None

    def test_user_unique_email_constraint(self, db, test_user):
        """Test that email must be unique."""
        duplicate_user = User(
            email=test_user.email,
            password_hash="another_hash",
            name="Duplicate User"
        )
        db.add(duplicate_user)
        with pytest.raises(Exception):
            db.commit()


class TestGroupModel:
    """Test Group model and relationships."""

    def test_create_group(self, db, test_user):
        """Test creating a group."""
        group = Group(
            name="Test Group",
            description="A test group",
            category="Technology",
            location="San Francisco",
            organizer_id=test_user.id
        )
        db.add(group)
        db.commit()
        db.refresh(group)

        assert group.id is not None
        assert group.name == "Test Group"
        assert group.organizer_id == test_user.id
        assert group.founded is not None

    def test_group_organizer_relationship(self, db, test_user, test_group):
        """Test group-organizer relationship."""
        assert test_group.organizer.id == test_user.id
        assert test_group in test_user.organized_groups


class TestEventModel:
    """Test Event model and relationships."""

    def test_create_event(self, db, test_user, test_group):
        """Test creating an event."""
        event = Event(
            title="Test Event",
            description="A test event",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        assert event.id is not None
        assert event.title == "Test Event"
        assert event.group_id == test_group.id
        assert event.organizer_id == test_user.id

    def test_event_group_relationship(self, db, test_event, test_group):
        """Test event-group relationship."""
        assert test_event.group.id == test_group.id
        assert test_event in test_group.events

    def test_event_organizer_relationship(self, db, test_event, test_user):
        """Test event-organizer relationship."""
        assert test_event.organizer.id == test_user.id
        assert test_event in test_user.organized_events


class TestCategoryModel:
    """Test Category model."""

    def test_create_category(self, db):
        """Test creating a category."""
        category = Category(
            name="Technology",
            icon="💻",
            color="#3B82F6",
            slug="technology"
        )
        db.add(category)
        db.commit()
        db.refresh(category)

        assert category.id is not None
        assert category.name == "Technology"
        assert category.icon == "💻"


class TestUserInterestsAssociation:
    """Test user-interests many-to-many relationship."""

    def test_add_user_interest(self, db, test_user, test_category):
        """Test adding interest to user."""
        test_user.interests.append(test_category)
        db.commit()

        assert test_category in test_user.interests
        assert test_user in test_category.interested_users

    def test_remove_user_interest(self, db, test_user, test_category):
        """Test removing interest from user."""
        test_user.interests.append(test_category)
        db.commit()

        test_user.interests.remove(test_category)
        db.commit()

        assert test_category not in test_user.interests

    def test_multiple_user_interests(self, db, test_user):
        """Test user with multiple interests."""
        cat1 = Category(name="Technology", icon="💻", color="#3B82F6", slug="technology")
        cat2 = Category(name="Sports", icon="⚽", color="#10B981", slug="sports")
        db.add_all([cat1, cat2])
        db.commit()

        test_user.interests.extend([cat1, cat2])
        db.commit()

        assert len(test_user.interests) == 2


class TestGroupMembersAssociation:
    """Test group-members many-to-many relationship."""

    def test_add_group_member(self, db, test_group, test_user2):
        """Test adding member to group."""
        test_group.members.append(test_user2)
        db.commit()

        assert test_user2 in test_group.members
        assert test_group in test_user2.joined_groups

    def test_remove_group_member(self, db, test_group, test_user2):
        """Test removing member from group."""
        test_group.members.append(test_user2)
        db.commit()

        test_group.members.remove(test_user2)
        db.commit()

        assert test_user2 not in test_group.members

    def test_multiple_group_members(self, db, test_group, multiple_users):
        """Test group with multiple members."""
        test_group.members.extend(multiple_users[:3])
        db.commit()

        assert len(test_group.members) == 3

    def test_user_multiple_groups(self, db, test_user2, multiple_groups):
        """Test user joining multiple groups."""
        for group in multiple_groups[:2]:
            group.members.append(test_user2)
        db.commit()

        assert len(test_user2.joined_groups) == 2


class TestEventAttendeesAssociation:
    """Test event-attendees many-to-many relationship."""

    def test_add_event_attendee(self, db, test_event, test_user2):
        """Test adding attendee to event."""
        test_event.attendees.append(test_user2)
        db.commit()

        assert test_user2 in test_event.attendees
        assert test_event in test_user2.attended_events

    def test_remove_event_attendee(self, db, test_event, test_user2):
        """Test removing attendee from event."""
        test_event.attendees.append(test_user2)
        db.commit()

        test_event.attendees.remove(test_user2)
        db.commit()

        assert test_user2 not in test_event.attendees

    def test_multiple_event_attendees(self, db, test_event, multiple_users):
        """Test event with multiple attendees."""
        test_event.attendees.extend(multiple_users[:4])
        db.commit()

        assert len(test_event.attendees) == 4

    def test_user_multiple_events(self, db, test_user2, multiple_events):
        """Test user attending multiple events."""
        for event in multiple_events[:3]:
            event.attendees.append(test_user2)
        db.commit()

        assert len(test_user2.attended_events) == 3


class TestCascadeDeletes:
    """Test cascade delete behaviors."""

    def test_delete_user_cascades_to_groups(self, db, test_user):
        """Test deleting user deletes their organized groups."""
        group = Group(
            name="Test Group",
            category="Technology",
            organizer_id=test_user.id
        )
        db.add(group)
        db.commit()
        group_id = group.id

        db.delete(test_user)
        db.commit()

        # Verify group is deleted
        deleted_group = db.query(Group).filter(Group.id == group_id).first()
        assert deleted_group is None

    def test_delete_user_cascades_to_events(self, db, test_user, test_group):
        """Test deleting user deletes their organized events."""
        event = Event(
            title="Test Event",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        db.add(event)
        db.commit()
        event_id = event.id

        db.delete(test_user)
        db.commit()

        # Verify event is deleted
        deleted_event = db.query(Event).filter(Event.id == event_id).first()
        assert deleted_event is None

    def test_delete_group_cascades_to_events(self, db, test_group):
        """Test deleting group deletes its events."""
        event = Event(
            title="Test Event",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_group.organizer_id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        db.add(event)
        db.commit()
        event_id = event.id

        db.delete(test_group)
        db.commit()

        # Verify event is deleted
        deleted_event = db.query(Event).filter(Event.id == event_id).first()
        assert deleted_event is None

    def test_delete_user_removes_from_group_members(self, db, test_group, test_user2):
        """Test deleting user removes them from group members."""
        test_group.members.append(test_user2)
        db.commit()

        db.delete(test_user2)
        db.commit()

        # Verify user removed from members
        db.refresh(test_group)
        assert test_user2 not in test_group.members

    def test_delete_user_removes_from_event_attendees(self, db, test_event, test_user2):
        """Test deleting user removes them from event attendees."""
        test_event.attendees.append(test_user2)
        db.commit()

        db.delete(test_user2)
        db.commit()

        # Verify user removed from attendees
        db.refresh(test_event)
        assert test_user2 not in test_event.attendees

    def test_delete_category_removes_user_interests(self, db, test_user, test_category):
        """Test deleting category removes user interests."""
        test_user.interests.append(test_category)
        db.commit()

        db.delete(test_category)
        db.commit()

        # Verify interest removed
        db.refresh(test_user)
        assert test_category not in test_user.interests


class TestDataIntegrity:
    """Test data integrity constraints."""

    def test_event_requires_group(self, db, test_user):
        """Test that event must have a valid group."""
        event = Event(
            title="Orphan Event",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=9999,  # Non-existent group
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        db.add(event)
        with pytest.raises(Exception):
            db.commit()

    def test_event_requires_organizer(self, db, test_group):
        """Test that event must have a valid organizer."""
        event = Event(
            title="Orphan Event",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=9999,  # Non-existent user
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        db.add(event)
        with pytest.raises(Exception):
            db.commit()

    def test_group_requires_organizer(self, db):
        """Test that group must have a valid organizer."""
        group = Group(
            name="Orphan Group",
            category="Technology",
            organizer_id=9999  # Non-existent user
        )
        db.add(group)
        with pytest.raises(Exception):
            db.commit()


class TestRelationshipQueries:
    """Test relationship-based queries."""

    def test_query_user_organized_groups(self, db, test_user):
        """Test querying user's organized groups."""
        groups = [
            Group(name=f"Group {i}", category="Technology", organizer_id=test_user.id)
            for i in range(3)
        ]
        db.add_all(groups)
        db.commit()

        assert len(test_user.organized_groups) == 3

    def test_query_user_attended_events(self, db, test_user, test_group, test_user2):
        """Test querying user's attended events."""
        events = [
            Event(
                title=f"Event {i}",
                date=date(2025, 12, 15 + i),
                time="18:00",
                group_id=test_group.id,
                organizer_id=test_user.id,
                location_city="San Francisco",
                category="Technology",
                price="Free",
                is_online=False
            )
            for i in range(3)
        ]
        db.add_all(events)
        db.commit()

        # User2 attends all events
        for event in events:
            event.attendees.append(test_user2)
        db.commit()

        db.refresh(test_user2)
        assert len(test_user2.attended_events) == 3

    def test_query_group_events(self, db, test_user, test_group):
        """Test querying group's events."""
        events = [
            Event(
                title=f"Event {i}",
                date=date(2025, 12, 15 + i),
                time="18:00",
                group_id=test_group.id,
                organizer_id=test_user.id,
                location_city="San Francisco",
                category="Technology",
                price="Free",
                is_online=False
            )
            for i in range(4)
        ]
        db.add_all(events)
        db.commit()

        db.refresh(test_group)
        assert len(test_group.events) == 4
