"""Inserir podcast inicial

Revision ID: 6cf8351ab844
Revises: 3a05db1c7b1e
Create Date: 2025-04-05 20:54:44.198391

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6cf8351ab844'
down_revision: Union[str, None] = '3a05db1c7b1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        INSERT INTO podcast (id, titulo, descricao, autor, poster_url, feed_url)
        VALUES (1,
                'NerdCast',
                'O mundo vira piada no Jovem Nerd',
                'Jovem Nerd',
                'https://jovemnerd.com.br/wp-content/themes/jovem-nerd-v9/assets/images/nc-feed.jpg',
                'https://jnfilter.gabrielgio.me/'
                )
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DELETE FROM podcast
        WHERE id = 1
        """
    )