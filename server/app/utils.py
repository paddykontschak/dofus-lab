from app import db, session_scope, cache_region, limiter
from app.database.model_custom_set import ModelCustomSet
from app.database.model_custom_set_stat import ModelCustomSetStat
from datetime import datetime
from flask import session
from flask_babel import _
from graphql import GraphQLError
from flask_login import current_user
from sqlalchemy import update


@limiter.limit("3/second", error_message=_("Please wait a moment before trying again."))
def get_or_create_custom_set(custom_set_id, db_session):
    owned_custom_sets = session.get("owned_custom_sets") or []
    if custom_set_id:
        custom_set = db_session.query(ModelCustomSet).get(custom_set_id)
        if custom_set.owner_id and custom_set.owner_id != current_user.get_id():
            raise GraphQLError(_("You don't have permission to edit that build."))
        elif not custom_set.owner_id and custom_set.uuid not in owned_custom_sets:
            raise GraphQLError(_("You don't have permission to edit that build."))
        custom_set.last_modified = datetime.utcnow()
    else:
        custom_set = ModelCustomSet(owner_id=current_user.get_id())
        db_session.add(custom_set)
        db_session.flush()
        custom_set_stat = ModelCustomSetStat(custom_set_id=custom_set.uuid)
        if current_user.is_anonymous:
            owned_custom_sets.append(custom_set.uuid)
            session["owned_custom_sets"] = owned_custom_sets
        db_session.add(custom_set_stat)
    return custom_set


def save_custom_sets(db_session):
    owned_custom_sets = session.get("owned_custom_sets")
    if owned_custom_sets:
        db_session.query(ModelCustomSet).filter(
            ModelCustomSet.uuid.in_(owned_custom_sets)
        ).update(
            {ModelCustomSet.owner_id: current_user.get_id()},
            synchronize_session="fetch",
        )
        session["owned_custom_sets"] = []


def anonymous_or_verified(func):
    def wrapper(*args, **kwargs):
        if (
            current_user.is_authenticated
            and not current_user._get_current_object().verified
        ):
            raise GraphQLError(
                _("Please verify your account to continue using DofusLab.")
            )
        return func(*args, **kwargs)

    return wrapper


def check_owner(custom_set):
    if not custom_set:
        raise GraphQLError(_("That build does not exist."))
    owned_custom_sets = session.get("owned_custom_sets") or []
    if custom_set.owner_id and custom_set.owner_id != current_user.get_id():
        raise GraphQLError(_("You don't have permission to edit that build."))
    elif not custom_set.owner_id and custom_set.uuid not in owned_custom_sets:
        raise GraphQLError(_("You don't have permission to edit that build."))
