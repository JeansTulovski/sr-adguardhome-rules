import re
import urllib.request
import os

def convert_rule(source_url, output_filename):
    print(f"正在从远程拉取规则: {source_url}")
    try:
        req = urllib.request.urlopen(source_url)
        content = req.read().decode('utf-8')
        lines = content.splitlines()
    except Exception as e:
        print(f"拉取远程规则 {source_url} 失败: {e}")
        return

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
        
        for i, url in enumerate(urls):
            # 第一行链接默认输出为 jeans-adblock.list，后续如果有更多行会依次命名为 rule_2.list 等
            output_name = f"rule_{i+1}.list" if i > 0 else "jeans-adblock.list"
            convert_rule(url, output_name)
    else:
        print("未找到 sources.txt 配置文件！")
