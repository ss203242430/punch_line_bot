from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView

from applications.models import *
import datetime
from datetime import timedelta
import pytz
import random

class Custom_Statement_View(GenericAPIView):
    def get(self, request, *args, **krgs):
        damage_statisticses = Damage_Statistics.objects.all()
        champion = {
            'source_id': damage_statisticses[0].source_id,
            'damage': damage_statisticses[0].damage
        }
        for damage_statistics in damage_statisticses:
            if champion['damage'] < damage_statistics.damage:
                champion = {
                    'source_id': damage_statistics.source_id,
                    'damage': damage_statistics.damage
                }
            elif champion['damage'] == damage_statistics.damage:
                random_number = random.randint(0, 1)
                if random_number == 1:
                    champion = {
                        'source_id': damage_statistics.source_id,
                        'damage': damage_statistics.damage
                    }
        damage_statisticses.delete()
        bettings = Betting.objects.all()
        for betting in bettings:
            if betting.npc_id == champion['source_id']:
                user = User.objects.get(id=betting.user_id)
                user.point += betting.point * 10
                user.save()
        bettings.delete()
        cat_monster = Cat_Monster.objects.get(id=1)
        cat_monster.current_hp = cat_monster.max_hp
        cat_monster.save()
        return JsonResponse('1', safe=False)