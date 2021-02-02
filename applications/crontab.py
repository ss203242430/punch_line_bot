from linebot.models import *
import rand

def npc_attack_cat_monster():
	if Damage_Statistics.objects.filter(source_type='npc', cat_monster_id=1).exists():
        damage_statistics_list = Damage_Statistics.objects.filter(source_type='npc', cat_monster_id=1)
        last_place = {
            'npc_id': damage_statistics_list[0].source_id,
            'damage': damage_statistics_list[0].damage
        }
    else:
        last_place = {
            'npc_id': 0,
            'damage': 0
        }
    cat_monster = Cat_Monster.objects.get(id=1)
    npc_list = Npc.objects.all()
    random.shuffle(npc_list)
    for npc in npc_list:
        if npc.id == last_place['npc_id']:
            rice = random.randint(3, 6)
        else:
            rice = random.randint(1, 6)
        if rice == 6:
            rice += random.randint(1, 6)
        damage = rice * npc.attack
        if cat_monster.current_hp < damage:
            damage = cat_monster.current_hp
        cat_monster.current_hp -= damage
        cat_monster.save()
        if Damage_Statistics.objects.filter(source_id=npc.id, source_type='npc').exists():
            damage_statistics = Damage_Statistics.objects.get(source_id=npc.id, source_type='npc')
            damage_statistics.damage += damage
            damage_statistics.save()
        else:
            Damage_Statistics.objects.create(source_id=npc.id, source_type='npc', cat_monster_id=1, damage=damage)
        if cat_monster.current_hp == 0:
        	damage_statistics_list = Damage_Statistics.objects.all()
	        champion = {
	            'source_id': damage_statistics_list[0].source_id,
	            'damage': damage_statistics_list[0].damage
	        }
	        for damage_statistics in damage_statistics_list:
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
	        damage_statistics_list.delete()
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
