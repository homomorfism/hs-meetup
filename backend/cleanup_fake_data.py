"""
Clean up all fake/seed data and keep only real Meetup.com data
"""
from app.database import SessionLocal
from app.models import User, Group, Event
from app.core.security import get_password_hash

def cleanup_fake_data():
    db = SessionLocal()

    try:
        print("=" * 60)
        print("Cleaning up fake/seed data")
        print("=" * 60)

        # Step 1: Create a system admin user for imported events
        print("\n[1] Creating system admin user...")
        admin_user = User(
            email="admin@meetup.local",
            name="Meetup System",
            password_hash=get_password_hash("admin123"),
            bio="System account for managing imported Meetup.com events",
            location="Global",
            avatar="https://api.dicebear.com/7.x/bottts/svg?seed=admin"
        )
        db.add(admin_user)
        db.flush()  # Get the ID
        print(f"✓ Created admin user (ID: {admin_user.id})")

        # Step 2: Reassign all groups and events to new admin
        print("\n[2] Reassigning groups and events to admin user...")
        groups_updated = db.query(Group).update({Group.organizer_id: admin_user.id})
        events_updated = db.query(Event).update({Event.organizer_id: admin_user.id})
        db.flush()
        print(f"✓ Updated {groups_updated} groups")
        print(f"✓ Updated {events_updated} events")

        # Step 3: Clear user relationships that would block deletion
        print("\n[3] Clearing user relationships...")
        from sqlalchemy import text

        # Clear event attendees
        db.execute(text("DELETE FROM event_attendees"))
        print("✓ Cleared event attendees")

        # Clear group members
        db.execute(text("DELETE FROM group_members"))
        print("✓ Cleared group members")

        # Clear user interests
        db.execute(text("DELETE FROM user_interests"))
        print("✓ Cleared user interests")

        # Clear friendships
        db.execute(text("DELETE FROM friendships"))
        print("✓ Cleared friendships")

        # Step 4: Delete all fake users (except new admin)
        print("\n[4] Deleting fake users...")
        fake_users = db.query(User).filter(User.id != admin_user.id).all()
        fake_user_names = [u.name for u in fake_users]
        for user in fake_users:
            db.delete(user)
        print(f"✓ Deleted {len(fake_users)} fake users:")
        for name in fake_user_names:
            print(f"  - {name}")

        # Step 5: Commit all changes
        db.commit()

        # Step 6: Verify results
        print("\n" + "=" * 60)
        print("Cleanup Complete!")
        print("=" * 60)

        users_count = db.query(User).count()
        groups_count = db.query(Group).count()
        events_count = db.query(Event).count()

        print(f"\n✅ Remaining data:")
        print(f"   Users: {users_count} (admin@meetup.local)")
        print(f"   Groups: {groups_count} (real Meetup groups)")
        print(f"   Events: {events_count} (real Meetup events)")

        print(f"\n🔑 Admin credentials:")
        print(f"   Email: admin@meetup.local")
        print(f"   Password: admin123")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_fake_data()
