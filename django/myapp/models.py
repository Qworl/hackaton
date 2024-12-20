from django.db import models
import enum

class Record(models.Model):
    id = int
    title = models.TextField()
    text = models.TextField()
    comment_id = int
    grade = int
    is_new = bool
    is_quailfied = bool
    feedback_type = models.TextField()
    is_finance = bool
    subcategory_type = models.TextField()


    def __str__(self):
        return self.name

@enum.unique
class Feedback(enum.Enum):
    Претензия = 0
    Предложение = 1
    Благодарность = 2

@enum.unique
class Subcategory(enum.Enum):
    Ошибка_сотрудника = 0
    Несогласие_с_тарифами = 1
    Технический_сбой = 2
    Скорость_обслуживания = 3
