from os import stat
import random
import json

konst = 1.5
KERDESEK = json.load(open('kerdes_bank.json')).get('kerdesek')
KATEGORIZALT_KERDESEK = {}
for kerdes in KERDESEK:
    if kerdes['targy'] not in KATEGORIZALT_KERDESEK:
        KATEGORIZALT_KERDESEK[kerdes['targy']]={kerdes['tipus']:[kerdes]}
        # KATEGORIZALT_KERDESEK[kerdes['targy']]={}
        # KATEGORIZALT_KERDESEK[kerdes['targy']][kerdes['tipus']]=[]
        # KATEGORIZALT_KERDESEK[kerdes['targy']][kerdes['tipus']].append(kerdes)
    else:
        if kerdes['tipus'] not in KATEGORIZALT_KERDESEK[kerdes['targy']]:
            KATEGORIZALT_KERDESEK[kerdes['targy']][kerdes['tipus']]=[kerdes]
            # KATEGORIZALT_KERDESEK[kerdes['targy']][kerdes['tipus']]=[]
            # KATEGORIZALT_KERDESEK[kerdes['targy']][kerdes['tipus']].append(kerdes)
        else:
            KATEGORIZALT_KERDESEK[kerdes['targy']][kerdes['tipus']].append(kerdes)
            # KATEGORIZALT_KERDESEK[kerdes['targy']][kerdes['tipus']].append(kerdes)

# {
#     targy:{
#         tipus1:[]
#         tipus2:[]
#     }
# }

# False None '' "" [] == False

# lambdazas
# lambda kerdes,valasz: kerdes.get('answer')==valasz
# def _(kerdes,valasz):
#     return kerdes.get('answer')==valasz

KIERTEKELO = {
            'bhely': lambda kerdes, valasz: kerdes.get('answer') == valasz,
            'abcd': lambda kerdes, valasz: kerdes == valasz,
            'szam': lambda kerdes, valasz: abs(kerdes.get('answer') - valasz) <= kerdes.get('answer')*konst
            }

class Kikerdezo():
    # TODO MOD A ROSSZ VALASZT VISSZARAKJA (DUALINGO)

    def __init__(self,targy, tipus, mod='linear'):
        self.targy = targy
        self.tipus = tipus
        self.mod = mod
        self.previous = []
    
    def get_kerdes(self):
        lista = KATEGORIZALT_KERDESEK[self.targy][self.tipus]
        if self.mod == 'linear':
            lista = [l for l in lista if l not in self.previous]
            if not lista:
                exit()
            self.previous.append(lista[0])
            return lista[0]
        # TODO
        # RANDOM SORREND
    
    def kerdez(self):
        kerdes = self.get_kerdes()
        temp_out = ''
        if kerdes['tipus'] == 'szam':
            temp_out = kerdes.get('question').capitalize()
        elif kerdes['tipus'] == 'bhely':
            temp_out = kerdes.get('question').capitalize()
        elif kerdes['tipus'] == 'abcd':
            temp_out += f"{kerdes.get('question','Nincs kerdes').capitalize()}\n"
            shuffled_answers = [kerdes.get('answer','Nincs valasz')]+kerdes.get('bad_answer','Nincs valasz')

            random.shuffle(shuffled_answers)

            # print(shuffled_answers)
            # print(zip(shuffled_answers,['A','B','C','D']))
            # print(list(zip(shuffled_answers,['A','B','C','D'])))

            zipped_answer = [(answer,key) for answer,key in zip(shuffled_answers,['A','B','C','D'])]

            print(zipped_answer)


            for ans in zipped_answer:
                temp_out += f"{ans[1]}: {ans[0]}\n"
                # print(f"{ans[1]}: {ans[0]}\n")
                # print("{ans[1]}: {ans[0]}\n")
                if ans[0] == kerdes.get('answer','Nincs valasz'):
                    self.good_answer = ans[1]
                    



        Kikerdezo.kuld_kerdes(temp_out)
    
    def valasz(self, valasz):
        kerdes = self.previous[-1]
        # if kerdes['tipus'] == 'szam':
        #     kerdes.get('answer') == valasz
        # if kerdes['tipus'] == 'bhely':
        #     kerdes.get('answer').lower() == valasz.lower()
        # if kerdes['tipus'] == 'abcd':
        #     abs(kerdes.get('answer') - valasz) <= kerdes.get('answer')*konst
        Kikerdezo.kuld_valasz(KIERTEKELO[kerdes['tipus']](kerdes if not hasattr(self, "good_answer") else self.good_answer,valasz))
        # if KIERTEKELO[kerdes['tipus']](kerdes,valasz):
        #     Kikerdezo.kuld_valasz(True)
        # else:
        #     Kikerdezo.kuld_valasz(False)

        # TODO kulonbozo esetben mondja meg a megoldasmenetet




    @staticmethod
    def kuld_kerdes(kerdes):
        print(kerdes)
        



    
    @staticmethod
    def kuld_valasz(succes):
        if succes:
            print('Faszagyerek vagy!')
        else:
            print('Szopacs')

# statikus eset
# Kikerdezo.kuld_kerdes()

# peldanyositott eset
# a = Kikerdezo()
# a.kuld_kerdes()



    



def legyenonismilliomos(question):
    temp_out = ''
    temp_out += f"{question.get('question','Nincs kerdes').capitalize()}\n"

    # print([question.get('answer','Nincs valasz')]+question.get('bad_answer','Nincs valasz'))

    shuffled_answers = [question.get('answer','Nincs valasz')]+question.get('bad_answer','Nincs valasz')

    random.shuffle(shuffled_answers)

    # print(shuffled_answers)
    # print(zip(shuffled_answers,['A','B','C','D']))
    # print(list(zip(shuffled_answers,['A','B','C','D'])))

    zipped_answer = [(answer,key) for answer,key in zip(shuffled_answers,['A','B','C','D'])]

    print(zipped_answer)

    good_answer = ''

    for ans in zipped_answer:
        temp_out += f"{ans[1]}: {ans[0]}\n"
        # print(f"{ans[1]}: {ans[0]}\n")
        # print("{ans[1]}: {ans[0]}\n")
        if ans[0] == question.get('answer','Nincs valasz'):
            good_answer = ans[1]



    print(temp_out)

    answer = input()

    if answer == good_answer:
        print("Jo valasz!")
    else: print("Rossz valasz!")

def behely(question):
    print(question.get('question','error'))
    answer = input()
    if answer == question.get('answer','error'):
        print("Jo valasz!")
    else: print("Rossz valasz!")

def szamolos(question):
    print(question.get('question','error'))
    answer = input()
    
    real_answer  = question.get('answer')
    elteres = real_answer * konst
    if(abs(real_answer - answer) <= elteres):
        print("Jo valasz!")
    else: print("Rossz valasz!\n")
    print(question.get('explain','error'))


# n = random.randint(0,len(KERDESEK)-1)

# question = KERDESEK[n]

# if question.get('tipus') == 'abcd':
#     legyenonismilliomos(question)
# elif question.get('tipus') == 'bhely':
#     behely(question)
# elif question.get('tipus') == 'szam':
#     szamolos(question)
a = Kikerdezo(targy='Mernok Leszek',tipus='abcd')
while True:
    a.kerdez()
    valasz = input()
    a.valasz(valasz)

