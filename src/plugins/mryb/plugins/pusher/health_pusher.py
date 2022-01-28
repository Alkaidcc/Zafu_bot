import nonebot
from ...libs.zafureq import zr
from ...utils import scheduler
from ... import config
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import MessageSegment


# 12点和14点定时推送
@scheduler.scheduled_job("cron", second="0", minute="0", hour="12,14", day="*")
async def dsrw():
    bot = nonebot.get_bot()
    data = MessageSegment('')
    result = await zr.get_health_info()
    if result:
        for stu in result:
            if stu.status == "未登记":
                logger.info(f"{stu.name},{stu.status}")
                tmp = MessageSegment.text(
                    f"{stu.name},{stu.status}")+MessageSegment.at(stu.qid)
                data = data + tmp
        if data and data != '':
            logger.info(data)
            await bot.send_group_msg(group_id=config.group_id, message=data)
        else:
            await bot.send_group_msg(group_id=config.group_id, message="全部填报完成")
    else:
        await bot.send_group_msg(group_id=config.group_id, message="获取结果为空")
