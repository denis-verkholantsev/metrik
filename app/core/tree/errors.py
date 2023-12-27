from app.common.errors import AppError


class SkillTreeNotFoundError(AppError):
    error_message = "skill tree not found"


class SkillNotFoundError(AppError):
    error_message = "skill not found"


class KnowledgeNotFoundError(AppError):
    error_message = "knowledge not found"
