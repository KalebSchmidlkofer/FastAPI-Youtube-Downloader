"""4.0.1 migrations

Revision ID: bc1775d0fc21
Revises: bdbc4797881b
Create Date: 2024-11-16 23:17:19.566894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc1775d0fc21'
down_revision: Union[str, None] = 'bdbc4797881b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('requests', 'app')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requests', sa.Column('app', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
