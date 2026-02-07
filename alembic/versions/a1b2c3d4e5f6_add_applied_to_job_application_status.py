"""add applied to jobapplicationstatus enum

Revision ID: a1b2c3d4e5f6
Revises: dafe5fd5e2f1
Create Date: 2026-02-07

"""
from alembic import op


revision = 'a1b2c3d4e5f6'
down_revision = 'dafe5fd5e2f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add 'applied' to jobapplicationstatus so app can use applied/pending semantics
    op.execute("ALTER TYPE jobapplicationstatus ADD VALUE IF NOT EXISTS 'applied'")


def downgrade() -> None:
    # PostgreSQL does not support removing an enum value; leave 'applied' in place
    pass
