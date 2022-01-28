import nonebot
from nonebot.log import logger
from ... import config
from ...utils import get_score_by_time
from ...libs.zafureq import zr
from ...database import DB
from ...utils import scheduler


# 23点抓取一次数据 存入数据库
@scheduler.scheduled_job("cron", second="0", minute="00", hour="23", day="*")
async def save_to_db():
    bot = nonebot.get_bot()
    result = await zr.get_health_info()
    if result:
        async with DB() as db:
            for stu in result:
                await db.add_reg(int(stu.id), str(stu.status), stu.check_time)
                await db.add_score(
                    int(stu.id),
                    get_score_by_time(stu.check_time),
                    stu.check_time
                )
        await bot.send_group_msg(group_id=config.group_id, message="已成功写入数据库")
    else:
        logger.warning("获取结果失败")
        await bot.send_group_msg(group_id=config.group_id, message="获取结果为空，写入数据库失败")
