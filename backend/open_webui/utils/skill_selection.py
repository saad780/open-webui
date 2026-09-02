from collections.abc import Iterable


def resolve_skill_ids(
    submitted_skill_ids: Iterable[str],
    model_skill_ids: Iterable[str],
    mentioned_skill_ids: Iterable[str],
) -> tuple[set[str], set[str]]:
    """Separate full-content skill selections from model defaults.

    The web client includes model-attached skills in ``skill_ids`` so they can
    remain selected in the UI. Those defaults must stay description-only; an
    explicitly mentioned model skill may still request its full instructions.
    """
    submitted = set(submitted_skill_ids)
    model = set(model_skill_ids)
    mentioned = set(mentioned_skill_ids)
    user = (submitted - model) | mentioned
    return user, user | model
