import nonebot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.params import State
from nonebot.typing import T_State
from nonebot import on_command
from nonebot.log import logger
from ...database import DB
from ...utils import handle_q_date, is_date_valid

query_info = on_command("查询")
query_info.handle()(handle_q_date)


@query_info.got("q_date", prompt="请输入要查询的日期, 格式为yyyy-mm-dd，例:2022-01-25")
async def _(event: MessageEvent, state: T_State = State()):
    query_time = str(state['q_date'])
    data = []
    if is_date_valid(query_time):
        async with DB() as db:
            result = await db.get_students_by_date(m_date=query_time)
        if result is None:
            await query_info.finish("未查询到当天的结果哦~")
        else:
            for stu in result:
                if stu.status == '未登记':
                    data.append(f"{stu.name},{stu.status}\n")
                else:
                    data.append(f"{stu.name},{stu.status},{stu.check_time}\n")
            await query_info.finish("\n".join(data))
    else:
        await query_info.finish("请输入正确的日期格式")
