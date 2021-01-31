from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=50)
    name = models.CharField(max_length=255, blank=True)
    attack = models.IntegerField(default=1)
    attack_remaining = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    mdt = models.DateTimeField(auto_now=True)

class Custom_Statement(models.Model):
    _type = models.CharField(max_length=50, default='')
    statement = models.CharField(max_length=255, blank=True)
    mdt = models.DateTimeField(auto_now=True)

class Cat_Monster(models.Model):
    max_hp = models.IntegerField()
    current_hp = models.IntegerField()
    description = models.CharField(max_length=255, blank=True)
    mdt = models.DateTimeField(auto_now=True)

class Damage_Statistics(models.Model):
    source_id = models.IntegerField()
    source_type = models.CharField(max_length=64)
    cat_monster_id = models.IntegerField()
    damage = models.IntegerField()
    mdt = models.DateTimeField(auto_now=True)

class Learn_Punch(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=256, blank=True, default=' ')
    clock_in = models.DateTimeField(auto_now_add=True)
    clock_out = models.DateTimeField(null=True)
    mdt = models.DateTimeField(auto_now=True)

class Npc(models.Model):
    name = models.CharField(max_length=64, blank=True)
    job = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=256, blank=True)
    attack = models.IntegerField()
    mdt = models.DateTimeField(auto_now=True)

class Betting(models.Model):
    user_id = models.IntegerField()
    point = models.IntegerField(default=0)
    npc_id = models.IntegerField()
    mdt = models.DateTimeField(auto_now=True)