from nonebot import on_command
from nonebot.matcher import Matcher
from ...libs.zafureq import zr
command = on_command("每日一报")

@command.handle()
async def mryb(matcher: Matcher):
    data = []
    result = await zr.get_health_info()
    if result:
        for stu in result:
            if stu.check_time:
                data.append(f"{stu.name},{stu.status},{stu.check_time}\n")
            else:
                data.append(f"{stu.name},{stu.status}\n")
        await matcher.send(message="\n".join(data))
    else:
        await matcher.send(message="获取结果为空")