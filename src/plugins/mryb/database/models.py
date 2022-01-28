from tortoise.models import Model
from tortoise.fields.data import CharField, BigIntField, DatetimeField, IntField


class Student(Model):
    stu_id = BigIntField()
    q_id = BigIntField()
    name = CharField(max_length=5)
    total_score = IntField()


class Reg(Model):
    stu_id = BigIntField()
    status = CharField(max_length=5)
    time = DatetimeField(null=True)


class Score(Model):
    stu_id = BigIntField()
    score = IntField()
    time = DatetimeField(null=True)
