# Zafu_Bot——健康信息填报统计机器人

## 简介
用于 ZAFU 每日一报信息填报的统计机器人。
## 基本功能
- 每日一报信息填报统计。（包括姓名，登记状态，登记时间）
- 未填报人员统计。
- 定时检测未填报人员，并at群员
- 查询某一天的填报情况
- 定时抓取数据到数据库

## 安装
### 环境
python 版本为3.8.10

NoneBot2 版本为beta1

安装依赖包
```shell
pip install -r requirements.txt
```

关于Nonebot2和go-cqhttp的常规配置请参考 [这个视频](https://www.bilibili.com/video/BV1aZ4y1f7e2?from=search&seid=16779114370085531019&spm_id_from=333.337.0.0) 链接可能会失效

### 其他配置
在`.env.prod`中填写好学号和密码以及需要推送的群号

在`/src/plugins/mryb/`下创建一个名为`test.xlsx`的文件，里面存放学生信息配置文件

test.xlsx格式

| ID  | NAME | QQ  |
|-----|------|-----|
| 学号1 | 姓名1  | QQ1 |
| 学号2 | 姓名2  | QQ2 |
| ... | ...  | ... |

**学号和姓名最好都为文本格式**，不清楚数字格式是否会导致错误

## 特别感谢
[HarukaBot](https://github.com/SK-415/HarukaBot) 提供了很好的插件编写模板（bushi

[NoneBot2](https://github.com/nonebot/nonebot2) 提供了稳定的异步机器人框架

[go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 提供了稳定的cqhttp实现
