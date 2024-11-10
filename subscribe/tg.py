import yaml
import requests
from datetime import datetime
import pytz
from telegram import Bot
import asyncio
from collections import defaultdict

# 设置 Telegram Bot Token 和 Chat ID
TOKEN = '7105513269:AAGxdsjP9P6cp3wPdZeeLqmSA7wiBxn5ll8'
CHAT_ID = '-1002242550802'
bot = Bot(token=TOKEN)

# 获取北京时间
beijing = pytz.timezone('Asia/Shanghai')
update_time = datetime.now(beijing).strftime('%Y-%m-%d %H:%M:%S')

# 解析远程的 clash.yaml 并对节点进行分类
def classify_nodes_by_region(yaml_url):
    response = requests.get(yaml_url)
    response.raise_for_status()  # 如果请求失败则抛出异常
    data = yaml.safe_load(response.text)
    
    # 定义地区分类的字典，默认为空列表
    regions = defaultdict(list)

    # 遍历每个节点的名称并分类
    for proxy in data['proxies']:
        if 'name' in proxy:
            name = proxy['name']
            if name.startswith("🇺🇸"):
                regions["美国 🇺🇸"].append(name)
            elif name.startswith("🇬🇧"):
                regions["英国 🇬🇧"].append(name)
            elif name.startswith("🇨🇳"):
                regions["中国 🇨🇳"].append(name)
            elif name.startswith("🇯🇵"):
                regions["日本 🇯🇵"].append(name)
            else:
                regions["其他"].append(name)  # 未知地区或未标记的节点

    return regions

# 获取节点数量
def get_node_count(yaml_url):
    response = requests.get(yaml_url)
    response.raise_for_status()
    data = yaml.safe_load(response.text)
    return len(data['proxies'])

# 远程 YAML 文件 URL
yaml_url = 'https://gist.githubusercontent.com/eliangwww/059af67e3c197b8094441be1a16eec3f/raw/clash.yaml'
node_count = get_node_count(yaml_url)
node_regions = classify_nodes_by_region(yaml_url)

# 构建消息内容
message = f"#节点更新\n\npool 2h更新任务已完成\n\n节点链接：https://pool.cfip.nyc.mn\n\n更新时间: {update_time} (北京时间)\n\n节点数量: {node_count}\n\n节点地区：\n"
for region, names in node_regions.items():
    message += f"\n{region} ({len(names)}个节点):\n" + "\n".join(names) + "\n"

# 发送通知的异步函数
async def send_notification():
    await bot.send_message(chat_id=CHAT_ID, text=message)

# 运行异步函数
asyncio.run(send_notification())
