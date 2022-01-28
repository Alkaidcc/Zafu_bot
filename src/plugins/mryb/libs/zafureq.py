from ..utils import get_orign_stu_info
from nonebot.log import logger
from ..utils.browser import get_new_token
import requests
from typing import List
from ..utils import Stu, load_token


class DailyCheck():
    def __init__(self):
        # 使用refresh_token重新获取token
        self.token = load_token()
        self.request_url = 'https://appui.zafu.edu.cn/vapp/yqdj/djlist.jhtm?token=' + self.token
        self.path = "/vapp/yqdj/djlist.jhtm?token=" + self.token
        self.stu: List[Stu] = get_orign_stu_info()

    def refresh_other_params(self):
        self.request_url = 'https://appui.zafu.edu.cn/vapp/yqdj/djlist.jhtm?token=' + self.token
        self.path = "/vapp/yqdj/djlist.jhtm?token=" + self.token

    async def get_health_info(self):
        # 获取状态码和相应结果
        code, response = await self.get_data_from_url(self.request_url)
        if response is not None:
            for item in response:
                name = item['xm']
                time = item['djsj']
                for i in range(len(self.stu)):
                    if name == self.stu[i].name:
                        if "未登记" not in time:
                            self.stu[i].status = "已登记"
                            self.stu[i].check_time = time
                        else:
                            self.stu[i].status = "未登记"
                            self.stu[i].check_time = None
                        break
            return self.stu
        else:
            logger.warning("获取健康信息结果失败")
            return None

    async def get_data_from_url(self, url):
        headers = {
            "authority": "appui.zafu.edu.cn",
            "method": "POST",
            "path": self.path,
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-length": "0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://appui.zafu.edu.cn",
            "referer": "https://appui.zafu.edu.cn/vapp/index.html",
            "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        }
        req = requests.post(url, headers=headers)
        if "error" in req.text:
            logger.warning("token过期，正在更新token...")
            self.token = await get_new_token()
            logger.info("token更新成功")
            self.refresh_other_params()
            status_code, result = await self.get_data_from_url(self.request_url)
            return status_code, result
        else:
            return req.status_code, req.json()
            
zr = DailyCheck()


