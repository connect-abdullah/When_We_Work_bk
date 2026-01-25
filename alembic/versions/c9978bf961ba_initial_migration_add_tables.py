"""Initial migration - add tables

Revision ID: c9978bf961ba
Revises: 
Create Date: 2026-01-26 00:52:50.591577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c9978bf961ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create admin table
    op.create_table(
        'admin',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('middle_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('photo', sa.String(), nullable=True),
        sa.Column('language', sa.String(), nullable=False, server_default='en'),
        sa.Column('gender', sa.Enum('male', 'female', 'other', name='gender'), nullable=False),
        sa.Column('role', sa.Enum('admin', 'worker', name='userroleenum'), nullable=True, server_default='admin'),
        sa.Column('business_id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_id'), 'admin', ['id'], unique=False)

    # Create workers table
    op.create_table(
        'workers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('middle_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('emergency_contact', sa.String(), nullable=True),
        sa.Column('photo', sa.String(), nullable=True),
        sa.Column('language', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('gender', sa.Enum('male', 'female', 'other', name='gender'), nullable=False),
        sa.Column('availability', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('employment_type', sa.Enum('full_time', 'part_time', 'contract', 'freelancer', name='employmenttype'), nullable=False),
        sa.Column('user_role', sa.Enum('admin', 'worker', name='userroleenum'), nullable=True, server_default='worker'),
        sa.Column('roles', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('remarks', sa.String(), nullable=True),
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workers_id'), 'workers', ['id'], unique=False)

    # Create jobs table
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive', 'completed', 'cancelled', name='jobstatus'), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('minimum_education', sa.String(), nullable=False),
        sa.Column('job_category', sa.Enum('full_time', 'part_time', 'contract', 'freelancer', name='jobcategory'), nullable=False),
        sa.Column('tone_requirement', sa.Enum('professional', 'casual', 'formal', 'friendly', 'empathetic', name='tonerequirement'), nullable=False),
        sa.Column('characteristics', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('workers_required', sa.Integer(), nullable=False),
        sa.Column('workers_hired', sa.Integer(), nullable=False),
        sa.Column('salary', sa.Integer(), nullable=False),
        sa.Column('salary_type', sa.Enum('hourly', 'fixed', name='salarytype'), nullable=False),
        sa.Column('language', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('join_date', sa.DateTime(), nullable=False),
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_id'), 'jobs', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_jobs_id'), table_name='jobs')
    op.drop_table('jobs')
    op.drop_index(op.f('ix_workers_id'), table_name='workers')
    op.drop_table('workers')
    op.drop_index(op.f('ix_admin_id'), table_name='admin')
    op.drop_table('admin')
    
    # Drop enums
    sa.Enum(name='gender').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='userroleenum').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='employmenttype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='jobstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='jobcategory').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='tonerequirement').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='salarytype').drop(op.get_bind(), checkfirst=True)

