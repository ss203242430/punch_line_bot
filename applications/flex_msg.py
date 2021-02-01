from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from applications.models import *
from applications.flex_template import *
from applications.plot import *

import math
import pytz
import datetime
from datetime import timedelta

flex_max_quantity = 12 # flex_msg一次最多顯示數量上限

def cat_monster_flex(cat_monster_id):
    data = Cat_Monster.objects.get(id=cat_monster_id)
    max_hp = data.max_hp
    current_hp = data.current_hp
    hp_percent = math.floor(current_hp / max_hp * 100)
    description = data.description
    content = cat_monster_flex_template(hp_percent, description)
    message = FlexSendMessage(alt_text='貓貓怪', contents=content)
    return message

def damage_statistics_flex():
    npc_damage = {}
    npcs = Npc.objects.all()
    for npc in npcs:
        if Damage_Statistics.objects.filter(source_id=npc.id, source_type='npc', cat_monster_id=1).exists():
            damage_statisticss = Damage_Statistics.objects.get(source_id=npc.id, source_type='npc', cat_monster_id=1)
            npc_damage[npc.id] = {
                'name': npc.name,
                'damage': damage_statisticss.damage
            }
        else:
            npc_damage[npc.id] = {
                'name': npc.name,
                'damage': 0
            }

    cat_monster = Cat_Monster.objects.get(id=1)
    all_damage = cat_monster.max_hp - cat_monster.current_hp

    content = damage_statistics_flex_template()

    for npc_id, item in npc_damage.items():
        if all_damage != 0:
            damage_percentage = round(item['damage'] / all_damage * 100, 2)
        else:
            damage_percentage = 0
        npc_info = npc_info_flex_template(npc_id, item, damage_percentage)
        content['contents'][0]['header']['contents'].append(npc_info)
        damage_bar_graph = damage_bar_graph_flex_template(damage_percentage)
        content['contents'][0]['header']['contents'].append(damage_bar_graph)
    message = FlexSendMessage(alt_text='傷害統計', contents=content)
    return message

def learn_punch_flex(user_id, quantity=None, title=None):
    content = {
        "type": "carousel",
        "contents": []
    }
    tz = pytz.timezone('Asia/Taipei')
    if quantity:
        if quantity > flex_max_quantity:
            quantity = flex_max_quantity
        learn_punch_list = Learn_Punch.objects.filter(user_id=user_id).order_by('-id')[:quantity]
    elif title:
        learn_punch_list = Learn_Punch.objects.filter(user_id=user_id, title=title)[:flex_max_quantity]
    for learn_punch in learn_punch_list:
        title = learn_punch.title
        description = learn_punch.description
        clock_in = learn_punch.clock_in.astimezone(tz)
        clock_in_str = clock_in.strftime('%Y-%m-%d %H:%M:%S')
        clock_out = learn_punch.clock_out
        if clock_out is None:
            clock_out_str = ' '
            total_time = ' '
        else:
            clock_out = clock_out.astimezone(tz)
            clock_out_str = clock_out.strftime('%Y-%m-%d %H:%M:%S')
            total_time = clock_out - clock_in
            total_time = str(total_time).split('.')[0]
        bubble = learn_punch_flex_template(title, description, total_time, clock_in_str, clock_out_str)
        content['contents'].append(bubble)
    message = FlexSendMessage(alt_text='打卡記錄查詢', contents=content)
    return message

def learn_punch_week_flex(user_id, page):
    content = {
        "type": "carousel",
        "contents": []
    }
    week_start, week_end = get_week_start_end()
    learn_punch_list = Learn_Punch.objects.filter(user_id=user_id, clock_in__range=[week_start, week_end])
    if not learn_punch_list:
        response_msg = '查無打卡紀錄'
        message = TextSendMessage(text=response_msg)
        return message
    tz = pytz.timezone('Asia/Taipei')
    learn_punch_list = learn_punch_list[flex_max_quantity * (page - 1) : flex_max_quantity * page]
    for learn_punch in learn_punch_list:
        title = learn_punch.title
        description = learn_punch.description
        clock_in = learn_punch.clock_in.astimezone(tz)
        clock_in_str = clock_in.strftime('%Y-%m-%d %H:%M:%S')
        clock_out = learn_punch.clock_out
        if clock_out is None:
            clock_out_str = ' '
            total_time = ' '
        else:
            clock_out = clock_out.astimezone(tz)
            clock_out_str = clock_out.strftime('%Y-%m-%d %H:%M:%S')
            total_time = clock_out - clock_in
            total_time = str(total_time).split('.')[0]
        bubble = learn_punch_flex_template(title, description, total_time, clock_in_str, clock_out_str)
        content['contents'].append(bubble)
    message = FlexSendMessage(alt_text='打卡記錄查詢', contents=content)
    return message

def learn_punch_time_flex(user_id, start_time, end_time):
    content = {
        "type": "carousel",
        "contents": []
    }
    tz = pytz.timezone('Asia/Taipei')
    start_time = datetime.datetime.strptime(start_time, "%Y%m%d")
    start_time = start_time.astimezone(tz)
    end_time = datetime.datetime.strptime(end_time, "%Y%m%d")
    end_time = end_time.astimezone(tz)
    learn_punch_list = Learn_Punch.objects.filter(user_id=user_id, clock_in__range=[start_time, end_time])
    if not learn_punch_list:
        response_msg = '查無打卡紀錄'
        message = TextSendMessage(text=response_msg)
        return message
    learn_punch_list = learn_punch_list[:flex_max_quantity]
    for learn_punch in learn_punch_list:
        title = learn_punch.title
        description = learn_punch.description
        clock_in = learn_punch.clock_in.astimezone(tz)
        clock_in_str = clock_in.strftime('%Y-%m-%d %H:%M:%S')
        clock_out = learn_punch.clock_out
        if clock_out is None:
            clock_out_str = ' '
            total_time = ' '
        else:
            clock_out = clock_out.astimezone(tz)
            clock_out_str = clock_out.strftime('%Y-%m-%d %H:%M:%S')
            total_time = clock_out - clock_in
            total_time = str(total_time).split('.')[0]
        bubble = learn_punch_flex_template(title, description, total_time, clock_in_str, clock_out_str)
        content['contents'].append(bubble)
    message = FlexSendMessage(alt_text='打卡記錄查詢', contents=content)
    return message

def learn_punch_report_flex(user_id, title=None):
    if title:
        learn_punch_list = Learn_Punch.objects.filter(user_id=user_id, title=title)
    if not learn_punch_list:
        response_msg = '查無打卡紀錄'
        message = TextSendMessage(text=response_msg)
        return message, None
    total_time = datetime.timedelta()
    tz = pytz.timezone('Asia/Taipei')
    for learn_punch in learn_punch_list:
        clock_in = learn_punch.clock_in.astimezone(tz)
        clock_out = learn_punch.clock_out
        if clock_out is not None:
            total_time += clock_out - clock_in
    total_time = str(total_time).split('.')[0]
    result_msg = f'總學習時間: {total_time}'
    message = TextSendMessage(text=result_msg)
    plt_img_url = learn_punch_report_plot(learn_punch_list)
    plt_message = ImageSendMessage(original_content_url=plt_img_url, preview_image_url=plt_img_url)
    return message, plt_message

def learn_punch_week_report_flex(user_id, weeks_ago):
    week_start, week_end = get_week_start_end()
    learn_punch_list = Learn_Punch.objects.filter(user_id=user_id, clock_in__range=[week_start, week_end])
    if not learn_punch_list:
        response_msg = '查無打卡紀錄'
        message = TextSendMessage(text=response_msg)
        return message, None
    total_time = datetime.timedelta()
    tz = pytz.timezone('Asia/Taipei')
    for learn_punch in learn_punch_list:
        clock_in = learn_punch.clock_in.astimezone(tz)
        clock_out = learn_punch.clock_out
        if clock_out is not None:
            total_time += clock_out - clock_in
    total_time = str(total_time).split('.')[0]
    result_msg = f'總學習時間: {total_time}'
    message = TextSendMessage(text=result_msg)
    plt_img_url = learn_punch_week_report_plot(learn_punch_list, week_start)
    plt_message = ImageSendMessage(original_content_url=plt_img_url, preview_image_url=plt_img_url)
    return message, plt_message

def get_week_start_end():
    tz = pytz.timezone('Asia/Taipei')
    today = datetime.date.today()
    today = datetime.datetime.combine(today, datetime.datetime.min.time())
    week_start = today - timedelta(days=today.weekday())
    week_start = week_start.astimezone(tz)
    week_end = today + timedelta(days=7 - today.weekday())
    week_end = week_end.astimezone(tz)
    return week_start, week_end