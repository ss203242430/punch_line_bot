from django.contrib import admin

from applications.models import *

class User_Admin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'attack', 'attack_remaining', 'point', 'mdt')
admin.site.register(User, User_Admin)

class Custom_Statement_Admin(admin.ModelAdmin):
    list_display = ('id', '_type', 'statement', 'mdt')
admin.site.register(Custom_Statement, Custom_Statement_Admin)

class Cat_Monster_Admin(admin.ModelAdmin):
    list_display = ('id', 'max_hp', 'current_hp', 'description', 'mdt')
admin.site.register(Cat_Monster, Cat_Monster_Admin)

class Damage_Statistics_Admin(admin.ModelAdmin):
	list_display = ('id', 'source_id', 'source_type', 'cat_monster_id', 'damage', 'mdt')
admin.site.register(Damage_Statistics, Damage_Statistics_Admin)

class Learn_Punch_Admin(admin.ModelAdmin):
	list_display = ('id', 'user_id', 'title', 'description', 'clock_in', 'clock_out', 'mdt')
admin.site.register(Learn_Punch, Learn_Punch_Admin)

class Npc_Admin(admin.ModelAdmin):
	list_display = ('id', 'name', 'job', 'description', 'attack', 'mdt')
admin.site.register(Npc, Npc_Admin)

class Betting_Admin(admin.ModelAdmin):
	list_display = ('id', 'user_id', 'point', 'npc_id', 'mdt')
admin.site.register(Betting, Betting_Admin)