import os
import dotenv
from pathlib import Path
from typing import List, Optional
from .. import config
from . import patch
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.exception import FinishedException
from nonebot.params import CommandArg, State
from nonebot.typing import T_State
import time
import arrow
from nonebot.log import logger
from datetime import datetime
from openpyxl import load_workbook
from nonebot import require


class Stu:
    def __init__(self, stu_id, name, qid, status='未登记'):
        self.id = stu_id
        self.name = name
        self.qid = qid
        self.status = status
        self.check_time: Optional[str] = None


class xlsxParser:
    def __init__(self, path) -> None:
        self.data = load_workbook(path)
        self.sheet = self.data.worksheets[0]
        self.col1 = []
        self.col2 = []
        self.col3 = []

    def parse(self):
        for col in self.sheet['A']:
            if col.value == '' or col.value is None:
                break
            self.col1.append(col.value)
        for col in self.sheet['B']:
            if col.value == '' or col.value is None:
                break
            self.col2.append(col.value)
        for col in self.sheet['C']:
            if col.value == '' or col.value is None:
                break
            self.col3.append(col.value)
        return self.col1, self.col2, self.col3

    def get_stu_len(self):
        return len(self.col1)


def get_orign_stu_info() -> List[Stu]:
    file_path = './src/plugins/mryb/test.xlsx'
    res: List[Stu] = []
    parser = xlsxParser(file_path)
    stu_id, stu_name, stu_qid = parser.parse()
    for index, (s_id, name, qid) in enumerate(zip(stu_id, stu_name, stu_qid)):
        if index != 0:
            res.append(Stu(s_id, name, qid))
    return res


def save_token(s_token: str):
    dotenv_file = dotenv.find_dotenv()
    # print(dotenv_file)
    dotenv.load_dotenv(dotenv_file)
    os.environ["token"] = s_token
    dotenv.set_key(dotenv_file, "token", os.environ["token"])


def load_token() -> str:
    dotenv_file = dotenv.find_dotenv()
    # print(dotenv_file)
    dotenv.load_dotenv(dotenv_file)
    return os.environ["token"]


def get_path(*other):
    """获取数据文件绝对路径"""
    if config.abot_dir:
        dir_path = Path(config.abot_dir).resolve()
    else:
        dir_path = Path.cwd().joinpath("data")
    return str(dir_path.joinpath(*other))


def get_score_by_time(s_time) -> int:
    if not s_time:
        return -1
    struct_time = str_to_datetime(s_time)
    if struct_time.tm_hour < 12:
        return 1
    elif struct_time.tm_hour < 14:
        return 0
    else:
        return -1


def str_to_datetime(s_time):
    return time.strptime(s_time, "%Y-%m-%d %H:%M")


def is_date_valid(s_date) -> bool:
    try:
        datetime.strptime(s_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def parse_datetime_from_db(s_time) -> str:
    t_time = str(arrow.get(s_time))
    return datetime.strptime(t_time, "%Y-%m-%dT%H:%M:%S%z").strftime('%Y-%m-%d %H:%M')


async def handle_q_date(bot: Bot, event: MessageEvent, state: T_State = State(), command_arg: Message = CommandArg()):
    q_date = command_arg.extract_plain_text().strip()
    if not q_date:
        return
    if is_date_valid(str(q_date)):
        state["q_date"] = q_date
    else:
        await bot.send(event, "请输入正确的日期格式")
        raise FinishedException


scheduler = require("nonebot_plugin_apscheduler")
assert scheduler is not None
scheduler = scheduler.scheduler

if not Path(get_path()).is_dir():
    Path(get_path()).mkdir(parents=True)
