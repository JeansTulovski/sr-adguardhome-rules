import re

def convert():
    # 读取同目录下的源 AdGuard 规则文件
    try:
        with open("adblock.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("未找到源 adblock.txt 文件")
        return

    sr_rules = [
        "# ======= Jeans App AdBlock Rule-Set (Auto Generated) ======= #\n",
        "# 自动从 AdGuard 规则转换，供 Shadowrocket 使用\n\n"
    ]

    for line in lines:
        line = line.strip()
        # 用正则匹配像 ||domain.com^ 格式的行
        m = re.match(r"^\|\|([^^]+)\^$", line)
        if m:
            sr_rules.append(f"DOMAIN-SUFFIX,{m.group(1)}\n")

    # 输出为小火箭专用的 .list 文件
    with open("jeans-adblock.list", "w", encoding="utf-8") as f:
        f.writelines(sr_rules)
    print(f"转换成功！共生成 {len(sr_rules) - 2} 条小火箭规则。")

if __name__ == "__main__":
    convert()
