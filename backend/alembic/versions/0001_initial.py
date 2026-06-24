"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-06-24 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('email', sa.String(length=256), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # Create resumes table
    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('filename', sa.String(length=512), nullable=False),
        sa.Column('extracted_text', sa.Text(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True),
    )

    # Create interviews table
    op.create_table(
        'interviews',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('company', sa.String(length=256), nullable=False),
        sa.Column('role', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=64), nullable=True),
        sa.Column('meta', sa.JSON(), nullable=True),
    )

    # Create questions table
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('interview_id', sa.Integer(), sa.ForeignKey('interviews.id', ondelete='CASCADE'), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=128), nullable=True),
        sa.Column('meta', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # Create responses table
    op.create_table(
        'responses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('question_id', sa.Integer(), sa.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('interview_id', sa.Integer(), sa.ForeignKey('interviews.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('answer_text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('evaluation', sa.JSON(), nullable=True),
    )

    # Create analytics table
    op.create_table(
        'analytics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category', sa.String(length=128), nullable=False),
        sa.Column('average_score', sa.Float(), nullable=True),
        sa.Column('snapshot', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('analytics')
    op.drop_table('responses')
    op.drop_table('questions')
    op.drop_table('interviews')
    op.drop_table('resumes')
    op.drop_table('users')
