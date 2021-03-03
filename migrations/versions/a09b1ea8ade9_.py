"""empty message

Revision ID: a09b1ea8ade9
Revises: 
Create Date: 2021-02-26 13:50:50.418919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a09b1ea8ade9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mod_group',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name=op.f('fk_mod_group_group_id_group')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_mod_group_user_id_user'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mod_group')
    # ### end Alembic commands ###