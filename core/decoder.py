def skill_btn(var):
    return {
    'a': int(1),
    'b': int(2),
    'c': int(3),
    'd': int(4),
    'e': int(5),
    'f': int(6),
    'g': int(7),
    'h': int(8),
    'i': int(9),
    'm': True,
    'x': True,
    }.get(var,False)  #'error'為預設返回值，可自設定

def crd_btn(var):
    return {
    'a': int(6),
    'b': int(7),
    'c': int(8),
    '1': int(1),
    '2': int(2),
    '3': int(3),
    '4': int(4),
    '5': int(5),
    }.get(var,'0')  #'error'為預設返回值，可自設定

def chk_card(crd):
    crd_list = []
    for i in range(len(crd)):
        if crd[i] != 'x':
            crd_list.append(crd_btn(crd[i]))
    return crd_list

def chk_skill(nextround, skill):
    cast_skill = []
    cast_skill.append("round.waiting_phase(%s)"%nextround)
    #print("round.waiting_phase(%s)"%nextround)
    for i in range(len(skill)):
        if skill_btn(skill[i]):
            if skill[i] == 'm':
                if not skill_btn(skill[i+1]):
                    if i + 2 < len(skill):
                        if not skill_btn(skill[i+2]):
                            cast_skill.append("round.select_master_skill(%s, %s)"%(skill[i+1], skill[i+2]))
                            #print("round.select_master_skill(%s, %s)"%(skill[i+1], skill[i+2]))
                    else:
                        cast_skill.append("round.select_master_skill(%s)"%skill[i+1])
                        #print("round.select_master_skill(%s)"%skill[i+1])
            elif skill[i] == 'x':
                cast_skill.append("round.select_master_skill(3, %s, %s)"%(skill[i+1], skill[i+2]))
                #print("round.select_master_skill(3, %s, %s)"%(skill[i+1], skill[i+2]))
            elif i + 1 < len(skill):
                if not skill_btn(skill[i+1]):
                    cast_skill.append("round.select_servant_skill(%s, %s)"%(skill_btn(skill[i]), skill[i+1]))
                    #print("round.select_servant_skill(%s, %s)"%(skill_btn(skill[i]), skill[i+1]))
                else:
                    cast_skill.append("round.select_servant_skill(%s)"%skill_btn(skill[i]))
                    #print("round.select_servant_skill(%s)"%skill_btn(skill[i]))
            else:
                cast_skill.append("round.select_servant_skill(%s)"%skill_btn(skill[i]))
                #print("round.select_servant_skill(%s)"%skill_btn(skill[i]))
    return cast_skill

def decode(code):
    combat_order = []
    combat_order.append("round.quick_start()")
    #print("round.quick_start()")
    for i in range(6):
        if i < 3:
            combat_order += chk_skill(i+1, code[i])
            if len(chk_card(code[i+3])) == 1:
                seq = chk_card(code[i+3])
                combat_order.append("round.select_cards([%d])"%seq[0])
            elif len(chk_card(code[i+3])) == 2:
                seq = chk_card(code[i+3])
                combat_order.append("round.select_cards([%d, %d])"%(seq[0], seq[1]))
            elif len(chk_card(code[i+3])) == 3:
                seq = chk_card(code[i+3])
                combat_order.append("round.select_cards([%d, %d, %d])"%(seq[0], seq[1], seq[2]))
    combat_order.append("round.finish_battle()")
    return combat_order
