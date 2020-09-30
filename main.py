from classes.game import Person,bcolors
from classes.magic import Spell
from classes.inventory import Item
import random
#create black magic
fire = Spell("Fire",10,600,"black")
thunder = Spell("Thunder",10,600,"black")
blizzard = Spell("Blizarrd",10,600,"black")
meteor = Spell("Meteor",20,1200,"black")
quake = Spell("Quake",14,140,"black")

#create white magic
cure = Spell("Cure",12,620,"white")
cura = Spell("Cura",18,1500,"white")

#create some item

potion =Item("Potion","potion",'Heals 50 HP',50)
hipotion =Item("Hi-Potion","potion",'Heals 100 HP',100)
superpotion =Item("Super Potion","potion",'Heals 500 HP',500)
elixer =Item("Elixer","elixer",'Fully restores HP/MP of one member',9999)
hielixer =Item("MegaElixer","elixer","Fully restores  party's HP/MP of one member",9999)


grenade =Item("Grenade","attack",'Deals 500 damage',500)

player_spells =[fire,thunder,blizzard,meteor,cure,cura]
enemy_spells =[ fire,meteor,cure ]
player_items = [{"item":potion, "quantity":15},{"item":hipotion, "quantity":5},{"item":superpotion, "quantity":5},
                {"item":elixer, "quantity":5},{"item":hielixer, "quantity":2},{"item":grenade, "quantity":5}]
#Instantiate people
player1 =Person('Valos:',3260,132,300,34,player_spells,player_items)
player2 =Person('Nick :',4160,188,260,34,player_spells,player_items)
player3 =Person('Robot:',3090,174,289,34,player_spells,player_items)

enemy1 =Person('Imp  :',1250,130,560,325,enemy_spells,[])
enemy2 =Person('Magus:',11200,221,525,20,enemy_spells,[])
enemy3 =Person('Imp  :',1250,130,560,325,enemy_spells,[])

players =[player1,player2,player3]
enemies =[enemy1,enemy2,enemy3]

running =True

print(bcolors.FAIL+bcolors.BOLD+"AN ENEMY ATTACKS" +bcolors.ENDC)

while running:
    print("=====================")
    print("\n\n")
    print("NAME:       HP:          ")
    for player in players:
        player.get_stats()
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy =player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("you attacked "+enemies[enemy].name
                  +"for", dmg, "points for damage.")

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough mp" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for" + str(magic_dmg) + "HP." + bcolors.ENDC)
            elif spell.type == 'black':

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)


                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to"+enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp()==0:
                    print(enemies[enemy].name.replace(" ","")+"has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    choose item:")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]['quantity'] -= 1
            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL + '\n' + " None left...." + bcolors.ENDC)
                continue
            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for" + bcolors.ENDC)
            elif item.type == 'elixer':
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp =i.maxhp
                        i.mp =i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores MP/HP" + bcolors.ENDC)
            elif item.type == "attack":

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)


                print(bcolors.FAIL + "\n" + item.name + "deals" + str(item.prop) + ' points of damageto'+enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp()==0:
                    print(enemies[enemy].name.replace(" ","")+ "has died.")
                    del enemies[enemy]
     #battle is over or not
    defeated_enemies = 0
    defeated_players = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False


    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!!" + bcolors.ENDC)
        running = False

    for enemy in enemies:
        enemy_choice =random.randrange(0,3)
        if enemy_choice == 0:
            target =random.randrange(0,3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ","")+ " attacks"+player[target].name.replace(
            " ","") +"for", enemy_dmg)


        elif enemy_choice == 1:
            spell,magic_dmg =enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals" +enemy.name+"for" + str(magic_dmg) + "HP." + bcolors.ENDC)
            elif spell.type == 'black':

                target =random.randrange(0,3)

                players[target].take_damage(magic_dmg)


                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" " ,"")+"'s"+spell.name + " deals", str(magic_dmg), "points of damage to"+players[target].name.replace(" ","") + bcolors.ENDC)
                if players[target].get_hp()==0:
                    print(players[target].name.replace(" ","")+"has died.")
                    del players[player]
            # print("Enemy chose",spell,"damage is",magic_dmg)

