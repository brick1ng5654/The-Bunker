import random
from random import randint
from const import CPERCENT, UPERCENT

def load_characteristic(filename1, filename2, filename3, multiply):
    if(multiply == 0): 
        characteristic = [a for a in open(filename1, 'r', encoding='utf-8')]
        return characteristic
    common = [x for x in open(filename1, 'r', encoding='utf-8')]
    unusual = [y for y in open(filename2, 'r', encoding='utf-8')]
    rare = [z for z in open(filename3, 'r', encoding='utf-8')]
    characteristic = [common, unusual, rare]
    return characteristic

def pick(characteristic, to_delete):
    i = randint(1,100)
    if(i<=CPERCENT): k = 0
    elif(i<=CPERCENT+UPERCENT): k = 1
    else: k = 2
    value = random.choice(characteristic[k])
    if(to_delete == 1): characteristic[k].remove(value)
    return value

def load_array():
    age_array = load_characteristic("data/age/common_age.txt","data/age/unusual_age.txt","data/age/rare_age.txt",1)
    bagage_array = load_characteristic("data/bagage/common_bagage.txt","data/bagage/unusual_bagage.txt","data/bagage/rare_bagage.txt",1)
    fact_array = load_characteristic("data/fact/common_fact.txt","data/fact/unusual_fact.txt","data/fact/rare_fact.txt",1)
    gender_array = load_characteristic("data/gender/common_gender.txt","data/gender/unusual_gender.txt","data/gender/rare_gender.txt",1)
    health_array = load_characteristic("data/health/common_health.txt","data/health/unusual_health.txt","data/health/rare_health.txt",1)
    job_array = load_characteristic("data/job/common_job.txt","data/job/unusual_job.txt","data/job/rare_job.txt",1)
    sex_array = load_characteristic("data/sex/common_sex.txt","data/sex/unusual_sex.txt","data/sex/rare_sex.txt",1)
    action_array = load_characteristic("data/action.txt","","",0)
    condition_array = load_characteristic("data/condition.txt","","",0)
    fobia_array = load_characteristic("data/fobia.txt","","",0)
    knowledge_array = load_characteristic("data/knowledge.txt","","",0)
    personality_array = load_characteristic("data/personality.txt","","",0)

def pick_value(age_array, bagage_array, fact_array, gender_array, health_array, hobby_array, job_array, sex_array, action_array, condition_array, fobia_array, knowledge_array, personality_array):
    age = pick(age_array, 1)
    fact = pick(fact_array, 1)
    gender = pick(gender_array, 0)
    health = pick(health_array, 0)
    hobby = pick(hobby_array, 1)
    job = pick(job_array, 1)
    sex = pick(sex_array, 0)
    action = pick(action_array, 1)
    condition = pick(condition_array, 1)
    fobia = pick(fobia_array, 1)
    knowledge = pick(knowledge_array, 1)
    personality = pick(personality_array, 1)
    
def create_player(x, y, n, age, fact, gender, health, hobby, job, sex, action, condition, fobia, knowledge, personality):
    profile = []
    profile.append('КАРТОЧКА ИГРОКА ' + str(n))
    profile.append

if (__name__ == "__main__"):
    main()