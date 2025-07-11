import random

text_list = []
for i in range(13):
    text_list.append(i + 0.75)
for j in range(13):
    text_list.append(j + 0.5)
for k in range(13):
    text_list.append(k + 0.25)
for l in range(13):
    text_list.append(l + 0.0)
new_text_list = []


def wash():
    """隨機洗牌"""
    global text_list
    global new_text_list
    new_text_list.clear()  # 清空新列表
    # 隨機選擇一個起始位置和結束位置
    random_start = random.randint(0, len(text_list) - 1)
    random_end = random.randint(random_start, len(text_list) - 1)
    range_text = random_end - random_start + 1
    # 建立一個新的列表，包含從起始位置到結束位置的元素
    # 注意：這裡的 random_start 和 random_end 是包含在內的
    # 這裡的 m 是從 random_start 到 random_end 的索引
    # 這樣可以確保新列表的長度與 range_text 相同
    for m in range(range_text):
        new_text_list.append(text_list[random_start] + m - 1)
    # 從原始列表中刪除這些元素
    # 注意：這裡的 m 是從 random_start 到 random_end 的索引
    # 這裡的 n 是從 0 到 range_text - 1 的索引
    # 這樣可以確保新列表的長度與 range_text 相同


for item in new_text_list:
    if item in text_list:
        text_list.remove(item)
    # 將新列表中的元素添加到原始列表的開頭
    text_list = new_text_list + text_list


def deal_open():
    """發牌"""
    global text_list
    global new_text_list
    for o in range(5):
        # 刪除已發的牌
        with open(f"text/text{o + 1}", "w", encoding="utf-8") as file:
            if int(text_list[o - 1]) - (o - 1) == 0.75:
                file.write(f"黑桃{int(text_list[o - 1])}\n")
            elif int(text_list[o - 1]) - (o - 1) == 0.5:
                file.write(f"紅心{int(text_list[o - 1])}\n")
            elif int(text_list[o - 1]) - (o - 1) == 0.25:
                file.write(f"梅花{int(text_list[o - 1])}\n")
            elif int(text_list[o - 1]) - (o - 1) == 0:
                file.write(f"方塊{int(text_list[o - 1])}\n")
    for p in range(5):
        # 寫入牌的內容
        with open(f"text/text{p + 4}", "a", encoding="utf-8") as file:
            if int(text_list[p + 9]) - (p + 9) == 0.75:
                file.write(f"黑桃{int(text_list[p + 9])}\n")
            elif int(text_list[p + 9]) - (p + 9) == 0.5:
                file.write(f"紅心{int(text_list[p + 9])}\n")
            elif int(text_list[p + 9]) - (p + 9) == 0.25:
                file.write(f"梅花{int(text_list[p + 9])}\n")
            elif int(text_list[p + 9]) - (p + 9) == 0:
                file.write(f"方塊{int(text_list[p + 9])}\n")


# 主程式
while True:
    for q in range(20):
        wash()
    deal_open()
    for r in range(2):
        if text_list[r + 9] < 13:
            if int(text_list[r + 9]) - text_list[r + 9] == 0.75:
                print(f"黑桃{int(text_list[r + 9])}")
            elif int(text_list[r + 9]) - text_list[r + 9] == 0.5:
                print(f"紅心{int(text_list[r + 9])}")
            elif int(text_list[r + 9]) - text_list[r + 9] == 0.25:
                print(f"梅花{int(text_list[r + 9])}")
            elif int(text_list[r + 9]) - text_list[r + 9] == 0:
                print(f"方塊{int(text_list[r + 9])}")
        else:
            while text_list[r + 9] >= 13:
                # 將牌值減去13
                text_list[r + 9] -= 13
                if text_list[r + 9] < 13:
                    if int(text_list[r + 9]) - text_list[r + 9] == 0.75:
                        print(f"黑桃{int(text_list[r + 9])}")
                elif int(text_list[r + 9]) - text_list[r + 9] == 0.5:
                    print(f"紅心{int(text_list[r + 9])}")
                elif int(text_list[r + 9]) - text_list[r + 9] == 0.25:
                    print(f"梅花{int(text_list[r + 9])}")
                elif int(text_list[r + 9]) - text_list[r + 9] == 0:
                    print(f"方塊{int(text_list[r + 9])}")
    for s in range(2):
        if text_list[s + 11] < 13:
            if int(text_list[s + 11]) - text_list[s + 11] == 0.75:
                input(f"黑桃{str(int(text_list[s + 11]))}")
            elif int(text_list[s + 11]) - text_list[s + 11] == 0.5:
                input(f"紅心{str(text_list[s + 11])}")
            elif int(text_list[s + 11]) - text_list[s + 11] == 0.25:
                input(f"梅花{str(text_list[s + 11])}")
            elif int(text_list[s + 11]) - text_list[s + 11] == 0:
                input(f"方塊{str(text_list[s + 11])}")
        else:
            while text_list[s + 11] >= 13:
                # 將牌值減去13
                text_list[s + 11] -= 13
                if text_list[s + 11] < 13:
                    if int(text_list[s + 11]) - text_list[s + 11] == 0.75:
                        input(f"黑桃{str(text_list[s + 11])}")
                    elif int(text_list[s + 11]) - text_list[s + 11] == 0.5:
                        input(f"紅心{str(text_list[s + 11])}")
                    elif int(text_list[s + 11]) - text_list[s + 11] == 0.25:
                        input(f"梅花{str(text_list[s + 11])}")
                    elif int(text_list[s + 11]) - text_list[s + 11] == 0:
                        input(f"方塊{str(text_list[s + 11])}")
    print(text_list[14])
