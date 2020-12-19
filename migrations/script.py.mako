"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy_searchable import sync_trigger, vectorizer


def upgrade():
    vectorizer.clear()

    conn = op.get_bind()
    op.add_column('article', sa.Column('name_translations', HSTORE))

    metadata = sa.MetaData(bind=conn)
    articles = sa.Table('article', metadata, autoload=True)

    @vectorizer(articles.c.name_translations)
    def hstore_vectorizer(column):
        return sa.cast(sa.func.avals(column), sa.Text)

    op.add_column('article', sa.Column('content', sa.Text))
    sync_trigger(
        conn,
        'article',
        'search_vector',
        ['name_translations', 'content'],
        metadata=metadata
    )

${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
