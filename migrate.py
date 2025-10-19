#!/usr/bin/env python3
"""
Database Migration Script for Production CI/CD

This script runs Alembic migrations in production environments.
It should be called as part of your CI/CD pipeline before starting the application.

Usage:
    python migrate.py                    # Run all pending migrations
    python migrate.py --check            # Check if migrations are needed
    python migrate.py --downgrade -1     # Rollback one migration
    python migrate.py --revision <rev>   # Migrate to specific revision

Environment Variables:
    DATABASE_URL: PostgreSQL connection string (required)

Exit Codes:
    0: Success
    1: Migration failed
    2: Configuration error
"""
import sys
import os
import argparse
from pathlib import Path

try:
    from alembic.config import Config
    from alembic import command
    from alembic.script import ScriptDirectory
    from alembic.runtime.migration import MigrationContext
    from sqlalchemy import create_engine
except ImportError as e:
    print(f"ERROR: Missing required package: {e}")
    print("Install with: pip install alembic sqlalchemy")
    sys.exit(2)


def get_database_url():
    """Get DATABASE_URL from environment"""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        print("Set it with: export DATABASE_URL='postgresql://user:pass@host/dbname'")
        sys.exit(2)
    return db_url


def get_alembic_config():
    """Get Alembic configuration"""
    script_dir = Path(__file__).parent
    alembic_ini = script_dir / "alembic.ini"
    
    if not alembic_ini.exists():
        print(f"ERROR: alembic.ini not found at {alembic_ini}")
        sys.exit(2)
    
    config = Config(str(alembic_ini))
    return config


def check_pending_migrations():
    """Check if there are pending migrations"""
    db_url = get_database_url()
    config = get_alembic_config()
    
    engine = create_engine(db_url)
    script = ScriptDirectory.from_config(config)
    
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        current_rev = context.get_current_revision()
        head_rev = script.get_current_head()
        
        if current_rev is None:
            print("⚠️  Database has no migration history")
            return True
        elif current_rev != head_rev:
            print(f"📋 Current revision: {current_rev}")
            print(f"📋 Head revision: {head_rev}")
            print("⚠️  Pending migrations detected")
            return True
        else:
            print(f"✅ Database is up to date (revision: {current_rev})")
            return False


def run_upgrade(revision="head"):
    """Run database migrations"""
    print(f"🚀 Running database migrations to: {revision}")
    
    try:
        config = get_alembic_config()
        command.upgrade(config, revision)
        print("✅ Migrations completed successfully")
        return 0
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_downgrade(revision):
    """Rollback database migrations"""
    print(f"⚠️  Rolling back database to: {revision}")
    
    try:
        config = get_alembic_config()
        command.downgrade(config, revision)
        print("✅ Rollback completed successfully")
        return 0
    except Exception as e:
        print(f"❌ Rollback failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


def show_current_revision():
    """Show current database revision"""
    try:
        config = get_alembic_config()
        command.current(config)
        return 0
    except Exception as e:
        print(f"❌ Failed to get current revision: {e}")
        return 1


def show_history():
    """Show migration history"""
    try:
        config = get_alembic_config()
        command.history(config)
        return 0
    except Exception as e:
        print(f"❌ Failed to get history: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Database migration script for NexusPlanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if migrations are needed (exit 0 if up to date, 1 if pending)"
    )
    parser.add_argument(
        "--current",
        action="store_true",
        help="Show current database revision"
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Show migration history"
    )
    parser.add_argument(
        "--downgrade",
        metavar="REVISION",
        help="Downgrade to specific revision (e.g., -1 for previous, base for initial)"
    )
    parser.add_argument(
        "--revision",
        metavar="REVISION",
        help="Upgrade to specific revision (default: head)"
    )
    
    args = parser.parse_args()
    
    db_url = get_database_url()
    print(f"📊 Database: {db_url.split('@')[1] if '@' in db_url else 'configured'}")
    print()
    
    if args.check:
        has_pending = check_pending_migrations()
        return 1 if has_pending else 0
    
    elif args.current:
        return show_current_revision()
    
    elif args.history:
        return show_history()
    
    elif args.downgrade:
        confirm = input(f"⚠️  Are you sure you want to downgrade to {args.downgrade}? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancelled")
            return 0
        return run_downgrade(args.downgrade)
    
    elif args.revision:
        return run_upgrade(args.revision)
    
    else:
        return run_upgrade("head")


if __name__ == "__main__":
    sys.exit(main())
