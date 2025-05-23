"""7a34b6b5be43_01_init_url_and_urlclick_models

Revision ID: 7a34b6b5be43
Revises:
Create Date: 2023-09-30 12:06:11.911994

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7a34b6b5be43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'url',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('full_url', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_url_full_url'), 'url', ['full_url'], unique=True)
    op.create_table(
        'url_clicks',
        sa.Column('url_id', sa.UUID(), nullable=False),
        sa.Column('client', sa.String(length=100), nullable=False),
        sa.Column('datetime', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['url_id'], ['url.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('url_id', 'client', 'datetime'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url_clicks')
    op.drop_index(op.f('ix_url_full_url'), table_name='url')
    op.drop_table('url')
    # ### end Alembic commands ###
