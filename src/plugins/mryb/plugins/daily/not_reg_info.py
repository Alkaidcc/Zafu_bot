from nonebot import on_command
from nonebot.matcher import Matcher
from ...libs.zafureq import zr

nocheck = on_command("未填报")

@nocheck.handle()
async def wtb(matcher: Matcher):
    wtb_stu = []
    result = await zr.get_health_info()
    if result:
        for stu in result:
            if stu.status == "未登记":
                wtb_stu.append(f"{stu.name},{stu.status}\n")
        if wtb_stu:
            await matcher.send(message="\n".join(wtb_stu))
        else:
            await matcher.send(message="全部填报完成")
    else:
        await matcher.send(message="获取结果为空")