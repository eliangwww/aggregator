import yaml
import requests
from datetime import datetime
import pytz
from telegram import Bot

# 设置 Telegram Bot Token 和 Chat ID
TOKEN = ''
CHAT_ID = ''
bot = Bot(token=TOKEN)

# 获取北京时间
beijing = pytz.timezone('Asia/Shanghai')
update_time = datetime.now(beijing).strftime('%Y-%m-%d %H:%M:%S')

# 解析 clash.yaml 获取节点地区
def get_node_regions(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        regions = set()  # 用于存储唯一的地区标识符（Emoji旗帜）
        for proxy in data['proxies']:
            if 'name' in proxy:
                name = proxy['name']
                # 假设旗帜emoji在节点名称的前面
                if name and name[0] in ["🇺🇸", "🇬🇧", "🇨🇳", "🇯🇵"]:  # 可根据需要扩展
                    regions.add(name[0])  # 获取第一个 emoji，表示地区
        return regions

# 获取节点数量
def get_node_count(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return len(data['proxies'])

# 获取节点地区
node_regions = get_node_regions('path_to_clash.yaml')
node_count = get_node_count('path_to_clash.yaml')

# 创建消息内容
message = f"""
更新时间: {update_time} (北京时间)
节点数量: {node_count}
节点地区: {', '.join(node_regions)}
"""

# 发送通知
bot.send_message(chat_id=CHAT_ID, text=message)

