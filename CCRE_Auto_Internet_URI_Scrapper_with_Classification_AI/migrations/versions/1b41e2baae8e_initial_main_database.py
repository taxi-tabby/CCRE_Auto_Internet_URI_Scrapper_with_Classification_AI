"""Initial main database

Revision ID: 1b41e2baae8e
Revises: 
Create Date: 2025-04-15 06:28:54.259170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b41e2baae8e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = ('maindb',)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classes',
    sa.Column('id', sa.BigInteger().with_variant(sa.INTEGER(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('class_code', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_classes_class_code', 'classes', ['class_code'], unique=False)
    op.create_table('robots',
    sa.Column('id', sa.BigInteger().with_variant(sa.INTEGER(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('base_domain', sa.String(length=255), nullable=False),
    sa.Column('ruleset_text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('default_robots_index', 'robots', ['base_domain'], unique=False)
    op.create_table('roots',
    sa.Column('id', sa.BigInteger().with_variant(sa.INTEGER(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('root_key', sa.String(length=255), nullable=False),
    sa.Column('root_uri', sa.Text(), nullable=False),
    sa.Column('rules', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_roots_key_uri', 'roots', ['root_key', 'root_uri'], unique=False)
    op.create_table('branches',
    sa.Column('id', sa.BigInteger().with_variant(sa.INTEGER(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('parent_id', sa.BigInteger(), nullable=True),
    sa.Column('root_id', sa.BigInteger(), nullable=False),
    sa.Column('branch_uri', sa.Text(), nullable=False),
    sa.Column('_duplicate_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['branches.id'], ),
    sa.ForeignKeyConstraint(['root_id'], ['roots.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_branches_default', 'branches', ['root_id', 'id'], unique=False)
    op.create_index('idx_branches_parent_id', 'branches', ['root_id', 'parent_id'], unique=False)
    op.create_index('idx_branches_root_id', 'branches', ['root_id'], unique=False)
    op.create_index('idx_branches_uri', 'branches', ['branch_uri'], unique=False)
    op.create_table('leaves',
    sa.Column('id', sa.BigInteger().with_variant(sa.INTEGER(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('root_id', sa.BigInteger(), nullable=False),
    sa.Column('branch_id', sa.BigInteger(), nullable=False),
    sa.Column('val_html_meta_title', sa.Text(), nullable=True),
    sa.Column('val_html_meta_og_title', sa.Text(), nullable=True),
    sa.Column('val_html_meta_robots', sa.Text(), nullable=True),
    sa.Column('val_html_meta_description', sa.Text(), nullable=True),
    sa.Column('val_html_meta_keywords', sa.Text(), nullable=True),
    sa.Column('val_html_meta_author', sa.Text(), nullable=True),
    sa.Column('val_mime_type', sa.Text(), nullable=True),
    sa.Column('val_main_language', sa.Text(), nullable=True),
    sa.Column('val_content_size', sa.Integer(), nullable=True),
    sa.Column('link_cnt', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['branch_id'], ['branches.id'], ),
    sa.ForeignKeyConstraint(['root_id'], ['roots.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_leaves_root_branch_id', 'leaves', ['root_id', 'branch_id', 'id'], unique=False)
    op.create_table('leaves_classes',
    sa.Column('id', sa.BigInteger().with_variant(sa.INTEGER(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('root_id', sa.BigInteger(), nullable=False),
    sa.Column('branch_id', sa.BigInteger(), nullable=False),
    sa.Column('leaf_id', sa.BigInteger(), nullable=False),
    sa.Column('class_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['branch_id'], ['branches.id'], ),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['leaf_id'], ['leaves.id'], ),
    sa.ForeignKeyConstraint(['root_id'], ['roots.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_leaves_classes_branch', 'leaves_classes', ['branch_id'], unique=False)
    op.create_index('idx_leaves_classes_branch_leaf', 'leaves_classes', ['branch_id', 'leaf_id'], unique=False)
    op.create_index('idx_leaves_classes_class', 'leaves_classes', ['class_id'], unique=False)
    op.create_index('idx_leaves_classes_created_at', 'leaves_classes', ['created_at'], unique=False)
    op.create_index('idx_leaves_classes_default', 'leaves_classes', ['root_id', 'branch_id', 'id'], unique=False)
    op.create_index('idx_leaves_classes_leaf', 'leaves_classes', ['leaf_id'], unique=False)
    op.create_index('idx_leaves_classes_leaf_class', 'leaves_classes', ['leaf_id', 'class_id'], unique=False)
    op.create_index('idx_leaves_classes_root', 'leaves_classes', ['root_id'], unique=False)
    op.create_index('idx_leaves_classes_root_branch_leaf', 'leaves_classes', ['root_id', 'branch_id', 'leaf_id'], unique=False)
    op.create_index('idx_leaves_classes_root_class', 'leaves_classes', ['root_id', 'class_id'], unique=False)
    op.create_index('idx_leaves_classes_root_leaf', 'leaves_classes', ['root_id', 'leaf_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_leaves_classes_root_leaf', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_root_class', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_root_branch_leaf', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_root', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_leaf_class', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_leaf', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_default', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_created_at', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_class', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_branch_leaf', table_name='leaves_classes')
    op.drop_index('idx_leaves_classes_branch', table_name='leaves_classes')
    op.drop_table('leaves_classes')
    op.drop_index('idx_leaves_root_branch_id', table_name='leaves')
    op.drop_table('leaves')
    op.drop_index('idx_branches_uri', table_name='branches')
    op.drop_index('idx_branches_root_id', table_name='branches')
    op.drop_index('idx_branches_parent_id', table_name='branches')
    op.drop_index('idx_branches_default', table_name='branches')
    op.drop_table('branches')
    op.drop_index('idx_roots_key_uri', table_name='roots')
    op.drop_table('roots')
    op.drop_index('default_robots_index', table_name='robots')
    op.drop_table('robots')
    op.drop_index('idx_classes_class_code', table_name='classes')
    op.drop_table('classes')
    # ### end Alembic commands ###
