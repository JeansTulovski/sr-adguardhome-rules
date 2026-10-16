import re
import urllib.request
import os
import glob
from urllib.parse import urlparse
from datetime import datetime, timezone, timedelta

def clean_old_lists():
    # 查找仓库里所有以 jeans- 开头的 .list 文件并删除
    old_files = glob.glob("jeans-*.list")
    for f in old_files:
        try:
            os.remove(f)
            print(f"已清理旧文件: {f}")
        except Exception as e:
            print(f"清理文件 {f} 失败: {e}")

def convert_rule(source_url):
    print(f"正在从远程拉取规则: {source_url}")
    try:
        req = urllib.request.urlopen(source_url)
        content = req.read().decode('utf-8')
        lines = content.splitlines()
    except Exception as e:
        print(f"拉取远程规则 {source_url} 失败: {e}")
        return

    # 1. 自动从 URL 中提取原始文件名（例如 adguard-dns.txt）
    parsed_url = urlparse(source_url)
    basename = os.path.basename(parsed_url.path)
    
    # 2. 去掉原后缀（如 .txt），并加上 jeans- 前缀和 .list 后缀
    if basename:
        name_without_ext = os.path.splitext(basename)[0]
        output_filename = f"jeans-{name_without_ext}.list"
    else:
        output_filename = "jeans-rules.list"

    # 3. 计算北京时间 (UTC+8) 时间戳
    bj_time = datetime.now(timezone.utc) + timedelta(hours=8)
    time_str = bj_time.strftime("%Y-%m-%d %H:%M:%S")

    sr_rules = [
        f"# ======= Jeans App AdBlock Rule-Set (Auto Generated) ======= #\n",
        f"# Source: {source_url}\n",
        f"# Updated: {time_str} (UTC+8)\n\n"
    ]

    for line in lines:
        line = line.strip()
        m = re.match(r"^\|\|([^^]+)\^$", line)
        if m:
            sr_rules.append(f"DOMAIN-SUFFIX,{m.group(1)}\n")
        elif line and not line.startswith("!") and not line.startswith("#"):
            sr_rules.append(f"DOMAIN-SUFFIX,{line}\n")

    with open(output_filename, "w", encoding="utf-8") as f:
        f.writelines(sr_rules)
    print(f"转换成功！已保存至 {output_filename}，共生成 {len(sr_rules) - 3} 条规则。")

if __name__ == "__main__":
    # 运行前清理旧的 jeans-*.list 文件
    clean_old_lists()

    if os.path.exists("sources.txt"):
        with open("sources.txt", "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        for url in urls:
            convert_rule(url)
    else:
        print("未找到 sources.txt 配置文件！")
