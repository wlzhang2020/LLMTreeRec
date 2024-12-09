import re
import difflib

def get_cate(response):
    line_list = response.split('\n')
    cate_list = []

    if len(line_list) == 1:
        cate_list = [c.replace(" ", "").lower() for c in line_list[0].split(',')]
        return cate_list

    for line in line_list:
        if line and line[0].isdigit():
            cate_name = re.sub(r"[-:() ]", "", line.split(".", 1)[-1]).lower()
            cate_list.append(cate_name)

    return cate_list

def get_news_title(message):
    return [line.split('.', 1)[-1].strip() for line in message.split('\n') if line.strip() and line[0].isdigit()]

def get_subcate(response):
    line_list = response.split('\n')
    subcate_list = []

    for line in line_list:
        if line and line[0].isdigit():
            subcate_name = re.sub(r"[-:() ]", "", line.split(".", 1)[-1]).lower()
            subcate_list.append(subcate_name)

    return subcate_list

def get_pos_news(news_data, user_id, user_history):
    user_impression = user_history[user_history["User ID"] == user_id]["Impression News"]
    user_pos_news = set()

    for impression in user_impression:
        item_list = impression.split(' ')
        for item in item_list:
            newsid, label = item.split('-')
            if label == '1':
                news_title = news_data[news_data["NewsID"] == newsid]["NewsTitle"].iloc[0]
                user_pos_news.add(news_title)

    return user_pos_news

def get_answer_list(message):
    return [line.split('.', 1)[-1].strip() for line in message.split('\n') if line.strip() and line[0].isdigit()]
