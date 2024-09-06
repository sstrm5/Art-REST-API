from ninja import Schema

class QuestionFilters(Schema):
    search: str | None = None