"""Initial migration.

Revision ID: b8b9be3a0bb4
Revises: 
Create Date: 2020-02-12 23:47:07.377038

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b8b9be3a0bb4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "set",
        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("bonuses", sa.PickleType(), nullable=True),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "user",
        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "custom_set",
        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("owner_id", postgresql.UUID(), nullable=True),
        sa.Column("creation_date", sa.DateTime(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["user.uuid"],),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "custom_set_exos",
        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("stat", sa.String(), nullable=True),
        sa.Column("value", sa.Integer(), nullable=True),
        sa.Column("custom_set_id", postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(["custom_set_id"], ["custom_set.uuid"],),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "custom_set_stats",
        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("scrolledVitality", sa.Integer(), nullable=True),
        sa.Column("scrolledWisdom", sa.Integer(), nullable=True),
        sa.Column("scrolledStrength", sa.Integer(), nullable=True),
        sa.Column("scrolledIntelligence", sa.Integer(), nullable=True),
        sa.Column("scrolledChance", sa.Integer(), nullable=True),
        sa.Column("scrolledAgility", sa.Integer(), nullable=True),
        sa.Column("baseVitality", sa.Integer(), nullable=True),
        sa.Column("baseWisdom", sa.Integer(), nullable=True),
        sa.Column("baseStrength", sa.Integer(), nullable=True),
        sa.Column("baseIntelligence", sa.Integer(), nullable=True),
        sa.Column("baseChance", sa.Integer(), nullable=True),
        sa.Column("baseAgility", sa.Integer(), nullable=True),
        sa.Column("custom_set_id", postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(["custom_set_id"], ["custom_set.uuid"],),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "item",
        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("itemType", sa.String(), nullable=False),
        sa.Column("set_id", postgresql.UUID(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("imageUrl", sa.String(), nullable=True),
        sa.Column("custom_set_id", postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(["custom_set_id"], ["custom_set.uuid"],),
        sa.ForeignKeyConstraint(["set_id"], ["set.uuid"],),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "item_conditions",
        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("item_id", postgresql.UUID(), nullable=True),
        sa.Column("stat_type", sa.String(), nullable=True),
        sa.Column("conditionType", sa.String(), nullable=True),
        sa.Column("limit", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["item_id"], ["item.uuid"],),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "item_stats",
        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("item_id", postgresql.UUID(), nullable=True),
        sa.Column("stat", sa.String(), nullable=True),
        sa.Column("minValue", sa.Integer(), nullable=True),
        sa.Column("maxValue", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["item_id"], ["item.uuid"],),
        sa.PrimaryKeyConstraint("uuid"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("item_stats")
    op.drop_table("item_conditions")
    op.drop_table("item")
    op.drop_table("custom_set_stats")
    op.drop_table("custom_set_exos")
    op.drop_table("custom_set")
    op.drop_table("user")
    op.drop_table("set")
    # ### end Alembic commands ###
