import yaml
import requests
from datetime import datetime
import pytz
from telegram import Bot
import asyncio

# 设置 Telegram Bot Token 和 Chat ID
TOKEN = '7105513269:AAGxdsjP9P6cp3wPdZeeLqmSA7wiBxn5ll8'
CHAT_ID = '-1002242550802'
bot = Bot(token=TOKEN)

# 获取北京时间
beijing = pytz.timezone('Asia/Shanghai')
update_time = datetime.now(beijing).strftime('%Y-%m-%d %H:%M:%S')

# 解析远程的 clash.yaml 获取节点地区
def get_node_regions(yaml_url):
    response = requests.get(yaml_url)
    response.raise_for_status()  # 如果请求失败则抛出异常
    data = yaml.safe_load(response.text)
    regions = set()  # 用于存储唯一的地区标识符（Emoji旗帜）
    for proxy in data['proxies']:
        if 'name' in proxy:
            name = proxy['name']
            # 假设旗帜emoji在节点名称的前面
            if name and name[0] in ["🇺🇸", "🇬🇧", "🇨🇳", "🇯🇵"]:  # 可根据需要扩展
                regions.add(name[0])  # 获取第一个 emoji，表示地区
    return regions

# 获取节点数量
def get_node_count(yaml_url):
    response = requests.get(yaml_url)
    response.raise_for_status()
    data = yaml.safe_load(response.text)
    return len(data['proxies'])

# 远程 YAML 文件 URL
yaml_url = 'https://gist.githubusercontent.com/eliangwww/059af67e3c197b8094441be1a16eec3f/raw/clash.yaml'
node_regions = get_node_regions(yaml_url)
node_count = get_node_count(yaml_url)

# 创建消息内容
message = f"""
更新时间: {update_time} (北京时间)
节点数量: {node_count}
节点地区: {', '.join(node_regions)}
"""

# 发送通知的异步函数
async def send_notification():
    await bot.send_message(chat_id=CHAT_ID, text=message)

# 运行异步函数
asyncio.run(send_notification())
