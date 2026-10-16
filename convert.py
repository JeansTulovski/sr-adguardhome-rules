import re
import urllib.request
import os
from urllib.parse import urlparse

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

    sr_rules = [
        f"# ======= Reusable AdBlock Rule-Set (Auto Generated) ======= #\n",
        f"# Source: {source_url}\n\n"
    ]

    for line in lines:
        line = line.strip()
        # 兼容 AdGuard 格式 (||domain.com^) 和纯域名格式
        m = re.match(r"^\|\|([^^]+)\^$", line)
        if m:
            sr_rules.append(f"DOMAIN-SUFFIX,{m.group(1)}\n")
        elif line and not line.startswith("!") and not line.startswith("#"):
            sr_rules.append(f"DOMAIN-SUFFIX,{line}\n")

    with open(output_filename, "w", encoding="utf-8") as f:
        f.writelines(sr_rules)
    print(f"转换成功！已保存至 {output_filename}，共生成 {len(sr_rules) - 2} 条规则。")

if __name__ == "__main__":
    if os.path.exists("sources.txt"):
        with open("sources.txt", "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        for url in urls:
            convert_rule(url)
    else:
        print("未找到 sources.txt 配置文件！")
