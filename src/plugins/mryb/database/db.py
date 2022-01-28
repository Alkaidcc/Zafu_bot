from typing import Dict, List, Optional
from nonebot import get_driver
from tortoise import Tortoise
from .models import Score, Student, Reg
from ..utils import Stu, get_orign_stu_info, get_path, is_date_valid, parse_datetime_from_db
from nonebot.log import logger
from typing import List
from tortoise.queryset import QuerySet


class DB:
    """数据库交互类"""

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @classmethod
    async def init(cls):
        from . import models
        await Tortoise.init(
            db_url=f"sqlite://{get_path('data.sqlite3')}",
            modules={'models': [locals()['models']]}
        )
        await Tortoise.generate_schemas()

    async def add_reg(self, stu_id, status, reg_time):
        # logger.info(reg_time)
        if reg_time == "未登记":
            await Reg.create(
                stu_id=stu_id,
                status=status,
                time=None
            )
        else:
            await Reg.create(
                stu_id=stu_id,
                status=status,
                time=reg_time
            )

    async def add_student(self, stu_id, q_id, name):
        await Student.create(
            stu_id=stu_id,
            q_id=q_id,
            name=name,
            total_score=0
        )

    async def add_score(self, stu_id, score, time):
        if time == "未登记":
            await Score.create(
                stu_id=stu_id,
                score=score,
                time=None
            )
        else:
            await Score.create(
                stu_id=stu_id,
                score=score,
                time=time
            )

    async def init_student(self):
        conn = Tortoise.get_connection("default")
        res = await conn.execute_query_dict("SELECT COUNT(*) FROM student")
        count = res[0]['COUNT(*)']
        # logger.info(count)
        if count == 0:
            logger.info("Student表为空，开始初始化表")
            stu_list = get_orign_stu_info()
            for stu in stu_list:
                await self.add_student(int(stu.id), int(stu.qid), stu.name)
        else:
            logger.info("Student表已初始化")

    async def get_students_by_date(self, m_date) -> Optional[List[Stu]]:
        if is_date_valid(m_date):
            logger.info("valid date")
            conn = Tortoise.get_connection("default")
            res = await conn.execute_query_dict(f"SELECT * FROM reg where date(time)='{m_date}'")
            stu_list = get_orign_stu_info()
            if res:
                for item in res:
                    for stu in stu_list:
                        if str(item['stu_id']) == stu.id:
                            logger.info("Im ininnnnn")
                            stu.status = item['status']
                            logger.info(stu.status)
                            stu.check_time = parse_datetime_from_db(item['time'])
                            logger.info(stu.check_time)
                            break
                return stu_list
            else:
                return None
        else:
            logger.warning("错误的日期格式")
            return None

    @classmethod
    async def get_student_by_stu_id(cls, stu_id: int) -> Optional[Student]:
        return await Student.filter(stu_id=stu_id).first()

    @classmethod
    async def get_student_by_name(cls, name: str) -> Optional[Student]:
        return await Student.filter(name=name).first()


async def init():
    async with DB() as db:
        await db.init()
        await db.init_student()


get_driver().on_startup(init)
get_driver().on_shutdown(Tortoise.close_connections)
