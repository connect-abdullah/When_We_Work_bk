"""add pending to workstatus enum

Revision ID: add_pending_ws
Revises: fa04801ba017
Create Date: 2026-02-11 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_pending_ws'
down_revision = 'fa04801ba017'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add 'pending' value to the workstatus enum type
    # PostgreSQL requires ALTER TYPE to add new enum values
    op.execute("ALTER TYPE workstatus ADD VALUE IF NOT EXISTS 'pending' BEFORE 'assigned'")


def downgrade() -> None:
    # Note: PostgreSQL doesn't support removing enum values directly
    # You would need to recreate the enum type to remove a value
    # For now, we'll leave it as-is since removing enum values is complex
    # and 'pending' is a valid state that won't cause issues
    pass
