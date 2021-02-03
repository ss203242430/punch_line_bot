from django.shortcuts import render
from django.views.generic import TemplateView

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from applications.models import *
from applications.flex_msg import *
import random
import string
import datetime

class HomePage(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
        

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                message = []
                if event.message.type == 'sticker':
                    if event.message.package_id == '11537' and event.message.sticker_id == '52002771':
                        message = StickerSendMessage(package_id=11537, sticker_id=52002771)
                        line_bot_api.reply_message(event.reply_token,message)
                elif event.message.type == 'text':
                    mtext = event.message.text
                    custom_statement_types = Custom_Statement.objects.values_list('_type').distinct()
                    for custom_statement_type in custom_statement_types:
                        if mtext == custom_statement_type[0]:
                            statements = Custom_Statement.objects.filter(_type=mtext)
                            random_number = random.randint(0, len(statements) - 1)
                            message.append(TextSendMessage(text=statements[random_number].statement))
                    if mtext == '貓貓怪':
                        message.append(cat_monster_flex(1))
                    elif mtext == '傷害統計':
                        message.append(damage_statistics_flex())
                    elif mtext == '建立會員資料':
                        uid = event.source.user_id
                        if not User.objects.filter(uid=uid).exists():
                            profile = line_bot_api.get_profile(uid)
                            name = profile.display_name
                            User.objects.create(uid=uid, name=name)
                            response_msg = '會員資料新增完畢'
                            message.append(TextSendMessage(text=response_msg))
                        else:
                            response_msg = '已經有建立會員資料囉'
                            message.append(TextSendMessage(text=response_msg))
                    elif mtext == '人生啊':
                        message = StickerSendMessage(package_id=11538, sticker_id=51626522)
                    elif mtext[:6] == '建立自訂語句':
                        mtext_split = mtext.split(',')
                        if len(mtext_split) < 3:
                            response_msg = '請輸入正確格式\n建立自訂語句,{關鍵字},{回覆語句}'
                            message.append(TextSendMessage(text=response_msg))
                        else:
                            Custom_Statement.objects.create(
                                _type=mtext_split[1],
                                statement=mtext_split[2]
                            )
                            response_msg = '建立自訂語句成功'
                            message.append(TextSendMessage(text=response_msg))
                    elif mtext[:6] == '刪除自訂語句':
                        mtext_split = mtext.split(',')
                        if len(mtext_split) < 2:
                            response_msg = '請輸入正確格式\n刪除自訂語句,{關鍵字},{回覆語句}'
                            message.append(TextSendMessage(text=response_msg))
                        elif len(mtext_split) == 2:
                            custom_statement = Custom_Statement.objects.filter(
                                _type=mtext_split[1],
                            )
                            if len(custom_statement) == 1:
                                custom_statement.delete()
                                response_msg = '刪除自訂語句成功'
                                message.append(TextSendMessage(text=response_msg))
                            elif len(custom_statement) > 1:
                                response_msg = '請輸入要刪除的回覆語句\n刪除自訂語句,{關鍵字},{回覆語句}'
                                message.append(TextSendMessage(text=response_msg))
                            else:
                                response_msg = '查無此自訂語句'
                                message.append(TextSendMessage(text=response_msg))
                        else:
                            custom_statement = Custom_Statement.objects.filter(
                                _type=mtext_split[1],
                                statement=mtext_split[2]
                            )
                            if custom_statement:
                                custom_statement.delete()
                                response_msg = '刪除自訂語句成功'
                                message.append(TextSendMessage(text=response_msg))
                            else:
                                response_msg = '查無此自訂語句'
                                message.append(TextSendMessage(text=response_msg))
                    elif mtext == '關鍵字':
                        key_word_list = [
                            '貓貓怪', '傷害統計', '建立會員資料', '人生啊', '建立自訂語句', '刪除自訂語句',
                            '攻擊貓貓怪', '貓貓點數查詢', '學習打卡', '打卡記錄查詢', '打卡記錄週查詢', '喵', '貓',
                            '打卡記錄報表', '打卡記錄週報表', '下注'
                        ]
                        for custom_statement_type in custom_statement_types:
                            key_word_list.append(custom_statement_type[0])
                        message.append(key_word_flex(key_word_list))

                    if message:
                        line_bot_api.reply_message(event.reply_token, message)
                    else:
                        uid = event.source.user_id
                        if User.objects.filter(uid=uid).exists():
                            user = User.objects.get(uid=uid)
                            if mtext == '攻擊貓貓怪':
                                if user.attack_remaining > 0:
                                    user.attack_remaining -= 1
                                    user.save()
                                    damage = random.randint(1, 5) * user.attack
                                    response_msg = f'造成{damage}點傷害'
                                    message.append(TextSendMessage(text=response_msg))
                                    response_msg = '(^=QᴥQ=^)'
                                    message.append(TextSendMessage(text=response_msg))
                                    cat_monster = Cat_Monster.objects.get(id=1)
                                    cat_monster.current_hp = cat_monster.current_hp - damage
                                    cat_monster.save()
                                    Damage_Statistics.objects.create(source_id=user.id, source_type='user', cat_monster_id=1, damage=damage)
                                else:
                                    response_msg = '剩餘攻擊次數不足'
                                    message.append(TextSendMessage(text=response_msg))
                            elif mtext == '貓貓點數查詢':
                                response_msg = f'貓貓點數: {user.point}'
                                message.append(TextSendMessage(text=response_msg))
                            elif mtext[:2] == '下注':
                                mtext_split = mtext.split(',')
                                if len(mtext_split) == 3:
                                    cat_monster = Cat_Monster.objects.get(id=1)
                                    if cat_monster.current_hp < cat_monster.max_hp / 2:
                                        response_msg = '貓貓怪血量已小於一半，無法進行下注'
                                        message.append(TextSendMessage(text=response_msg))
                                    elif Betting.objects.filter(user_id=user.id).exists():
                                        response_msg = '已下注，無法再次下注'
                                        message.append(TextSendMessage(text=response_msg))
                                    else:
                                        point = int(mtext_split[1])
                                        user = User.objects.get(id=user.id)
                                        if user.point < point:
                                            response_msg = '貓貓點數不足'
                                            message.append(TextSendMessage(text=response_msg))
                                        else:
                                            user.point -= point
                                            user.save()
                                            npc_id = int(mtext_split[2])
                                            Betting.objects.create(user_id=user.id, point=point, npc_id=npc_id)
                                            response_msg = '下注成功'
                                            message.append(TextSendMessage(text=response_msg))
                                else:
                                    response_msg = '請輸入正確格式\n下注,{貓貓點數},{NPC_id}'
                                    message.append(TextSendMessage(text=response_msg))
                            elif mtext[:4] == '學習打卡':
                                new_punch_flag = False
                                if Learn_Punch.objects.filter(user_id=user.id).exists():
                                    last_learn_punch = Learn_Punch.objects.filter(user_id=user.id).order_by('-id')[0]
                                    if last_learn_punch.clock_out is None:
                                        if len(mtext.split(',')) > 1:
                                            message.append(TextSendMessage(text='請先進行刷退\n刷退指令為\n學習打卡'))
                                        else:
                                            last_learn_punch.clock_out = timezone.now()
                                            last_learn_punch.save()
                                            message.append(learn_punch_flex(user.id, 1))
                                    else:
                                        new_punch_flag = True
                                else:
                                    new_punch_flag = True
                                if new_punch_flag:
                                    mtext_split = mtext.split(',')
                                    if len(mtext_split) == 1:
                                        response_msg = '請輸入正確格式\n學習打卡,{標題},{描述(可省略)}'
                                        message.append(TextSendMessage(text=response_msg))
                                    else:
                                        if len(mtext_split) == 2:
                                            Learn_Punch.objects.create(
                                                user_id=user.id,
                                                title=mtext_split[1]
                                            )
                                            message.append(learn_punch_flex(user.id, 1))
                                        elif len(mtext_split) == 3:
                                            Learn_Punch.objects.create(
                                                user_id=user.id,
                                                title=mtext_split[1],
                                                description=mtext_split[2]
                                            )
                                            message.append(learn_punch_flex(user.id, 1))
                            elif mtext[:6] == '打卡記錄查詢':
                                if Learn_Punch.objects.filter(user_id=user.id).exists():
                                    mtext_split = mtext.split(',')
                                    if len(mtext_split) == 1:
                                        message.append(learn_punch_flex(user.id, 1))
                                    elif len(mtext_split) > 2:
                                        if mtext_split[1] == '數量':
                                            quantity = int(mtext_split[2])
                                            message.append(learn_punch_flex(user.id, quantity=quantity))
                                        elif mtext_split[1] == '時間':
                                            time_split = mtext_split[2].split('~')
                                            start_time = time_split[0]
                                            end_time = time_split[1]
                                            message.append(learn_punch_time_flex(user.id, start_time, end_time))
                                        elif mtext_split[1] == '標題':
                                            title = mtext_split[2]
                                            message.append(learn_punch_flex(user.id, title=title))
                                    else:
                                        response_msg = '請輸入正確格式\n打卡記錄查詢,{數量 or 時間 or 標題},{參數}'
                                        message.append(TextSendMessage(text=response_msg))
                                else:
                                    response_msg = '尚未擁有打卡紀錄'
                                    message.append(TextSendMessage(text=response_msg))
                            elif mtext[:7] == '打卡記錄週查詢':
                                if Learn_Punch.objects.filter(user_id=user.id).exists():
                                    mtext_split = mtext.split(',')
                                    if len(mtext_split) == 1:
                                        message.append(learn_punch_week_flex(user.id, 1))
                                    elif len(mtext_split) == 2:
                                        page = mtext_split[1]
                                        message.append(learn_punch_week_flex(user.id, int(page)))
                                else:
                                    response_msg = '尚未擁有打卡紀錄'
                                    message.append(TextSendMessage(text=response_msg))
                            elif mtext[:6] == '打卡記錄報表':
                                if Learn_Punch.objects.filter(user_id=user.id).exists():
                                    mtext_split = mtext.split(',')
                                    if len(mtext_split) > 2:
                                        if mtext_split[1] == '標題':
                                            title = mtext_split[2]
                                            msg, plt = learn_punch_report_flex(user.id, title=title)
                                            message.append(msg)
                                            if plt:
                                                message.append(plt)
                                    else:
                                        response_msg = '請輸入正確格式\n打卡記錄報表,{標題},{參數}'
                                        message.append(TextSendMessage(text=response_msg))
                                else:
                                    response_msg = '尚未擁有打卡紀錄'
                                    message.append(TextSendMessage(text=response_msg))
                            elif mtext[:7] == '打卡記錄週報表':
                                if Learn_Punch.objects.filter(user_id=user.id).exists():
                                    mtext_split = mtext.split(',')
                                    if len(mtext_split) == 1:
                                        msg, plt = learn_punch_week_report_flex(user.id, 1)
                                        message.append(msg)
                                        if plt:
                                            message.append(plt)
                                    elif len(mtext_split) == 2:
                                        weeks_ago = mtext_split[1]
                                        msg, plt = learn_punch_week_report_flex(user.id, int(weeks_ago))
                                        message.append(msg)
                                        if plt:
                                            message.append(plt)
                                else:
                                    response_msg = '尚未擁有打卡紀錄'
                                    message.append(TextSendMessage(text=response_msg))
                        else:
                            if mtext == '攻擊貓貓怪' or mtext == '貓貓點數查詢' or mtext[:2] == '下注' or mtext[:4] == '學習打卡' or\
                                mtext[:6] == '打卡記錄查詢' or mtext[:7] == '打卡記錄週查詢' or mtext[:6] == '打卡記錄報表' or \
                                mtext[:7] == '打卡記錄週報表':
                                response_msg = '請先輸入「建立會員資料」'
                                message.append(TextSendMessage(text=response_msg))

                    if message:
                        line_bot_api.reply_message(event.reply_token, message)
                    else:
                        if '貓' in mtext or '喵' in mtext:
                            domain = 'pieta.myddns.me:3001'
                            random_number = random.randint(1, 970)
                            if random_number <= 855:
                                cat_img_url = f'https://{domain}/static/cat/cat_100_days.mp4_20201226160529_{str(random_number).zfill(4)}.JPEG'
                            else:
                                cat_img_url = f'https://{domain}/static/cat/funy_cat.mp4_20210112134813_{str(random_number - 855).zfill(4)}.JPEG'
                            message.append(ImageSendMessage(original_content_url=cat_img_url, preview_image_url=cat_img_url))
                        if message:
                            line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()