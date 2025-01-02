from datetime import datetime


# 1 - kreiranje , 2 - azuriranje, 3 - logicko brisanje, 4 - fizicko brisanje


class Komunalna:
    def __init__(self):
        self.id=-1
        self.opis_prekrsaja=""
        self.datum_izvrsenja=""
        self.lista_izvrsilaca=""
        self.kazna=-1
        self.status=1
        self.svrha=-1

    def return_value(self):
        return {"id": self.id, "opis_prekrsaja": self.opis_prekrsaja, "datum_izvrsenja": self.datum_izvrsenja,
                "lista_izvrsilaca": self.lista_izvrsilaca, "kazna": self.kazna,
                "status": self.status, "svrha": self.svrha}

    def set_value(self, object1):
        self.id = int(object1["id"])
        self.opis_prekrsaja = object1["opis_prekrsaja"]
        self.datum_izvrsenja = object1["datum_i_vreme"]
        self.lista_izvrsilaca = object1["lista_izvrsilaca"]
        self.kazna = float(object1["kazna"])
        self.status = int(object1["status"])
        self.svrha = int(object1["svrha"])

    def make_an_object(self):

        while True:
            id = input("Unesite evidencioni broj:")
            if (not id.isnumeric()) and int(id)>999999999:
                continue
            else:
                self.id = int(id)
                break


        while True:
            try:
                self.datum_i_vreme = input("Unesite datum u formatu '%d.%m.%Y %H:%M':")
                datum=self.datum_i_vreme
                datum = (datetime.now()).strftime("%d.%m.%Y %H:%M")

            except (ValueError, TypeError):
                print("Greska! Pokusajte ponovo sa ispravnim formatom datuma!")
            else:
                break

        flag=True

        print("Unesite imena pocinitelja prekrsaja")
        list = []
        sum = 0
        while flag:

            for word in list:
                sum+=len(word)

            name = input("Ime: ")
            surname = input("Prezime: ")
            convicted = name + " " + surname

            sum1=sum+len(convicted)
            if(sum1<1500):
                list.append(convicted)
                convicted1 = ','.join(str(x) for x in list)
                self.lista_izvrsilaca=convicted1
            if sum1>1500:
                print("Ne mozete dodati vise prekrsilaca u listu! Dostignut je maksimum za ovaj dan!")
                flag=False
                break
            else:
                print("--- Ukoliko zelite da zavrsite sa dodavanjem pocinilaca, pritisnite 0 --- ")
                userChoice=input(">>>")
                if(userChoice)=="0":
                    flag=False
                    break



        while True:
            print("Unesite opis prekrsaja: ")
            opis=input(">>>")
            if len(opis) > 220:
                print("Opis prekrsaja moze imati max 220 karaktera!")
                opis= input(">>>")
            else:
                self.opis_prekrsaja=opis
                break



        while True:
            #self.kazna=kazna
            kazna = input("Cena kazne:")
            if (not kazna.isnumeric()) and float(kazna) > 1000000:
                print("Cena kazne moze biti samo izrazena ciframa i manja od 1 000 000 !")
                kazna=float(input(">>>"))
            else:
                self.kazna=float(kazna)
                break


        self.status = 1
        self.svrha = 1

    def delete_logical(self):
        while True:
            try:
                id = int(input("Unesite evidencioni broj:"))
            except(ValueError, TypeError):
                print("Morate uneti cifre!")
            if id > 999999999:
                print("Evidencioni broj ne sadrzi vise od 9 cifara")
            else:
                self.id = int(id)
                break
        self.status=0
        self.svrha=3

    def set_new_value(self):
        while True:
            id = input("Unesite evidencioni broj: \n"
                       ">>>")
            if not id.isnumeric():
                print("Evidencioni broj mora biti sastavljen od cifara!\n")
            elif int(id)>999999999:
                print("Evidencioni br. moze imati max 9 cifara!\n")
            else:
                self.id = int(id)
                break

        flag=True

        while flag:

            print("Izaberite atribut za koji se vrsi izmena:\n"
                  ""
                  "[1]Opis prekrsaja\n"
                  "[2]Datum i vreme izvrsenja prekrsaja\n"
                  "[3]Lista pocinilaca prekrsaja\n"
                  "[4]Iznos kazne za pocinjeni prekrsaj\n"
                  "[0] Izlaz\n")

            while True:
                try:
                    userChoice = int(input("Unesite opciju:"))
                except(ValueError, TypeError):
                    print("Unesite jedan od ponudjenih brojeva!")
                else:
                    break

            if userChoice==0:
                break

            if userChoice==1:
                while True:
                    print("Unesite opis prekrsaja: ")
                    opis = input(">>>")
                    if len(opis) > 220:
                        print("Opis prekrsaja moze imati max 220 karaktera!")
                        opis = input(">>>")
                    else:
                        self.opis_prekrsaja = opis
                        break


            if userChoice==2:

                while True:
                    try:
                        self.datum_i_vreme = input("Unesite datum u formatu '%d.%m.%Y %H:%M':")
                        datum = (datetime.now()).strftime("%d.%m.%Y %H:%M")
                        datum=self.datum_i_vreme


                    except (ValueError, TypeError):
                        print("Greska! Pokusajte ponovo sa ispravnim formatom datuma!")
                    else:
                        break

            if userChoice==3:
                print("Unesite imena pocinitelja prekrsaja")
                list = []
                sum = 0
                while flag:

                    for word in list:
                        sum += len(word)

                    name = input("Ime:\n"
                                 ">>> ")
                    surname = input("Prezime:\n"
                                    ">>> ")
                    convicted = name + " " + surname

                    sum1 = sum + len(convicted)
                    if (sum1 < 1500):
                        list.append(convicted)
                        convicted1 = ','.join(str(x) for x in list)
                        self.lista_izvrsilaca = convicted1

                    if sum1 > 1500:
                        print("Ne mozete dodati vise prekrsilaca u listu! Dostignut je maksimum za ovaj dan!")
                        flag = False
                        break
                    else:
                        print("--- Ukoliko zelite da zavrsite sa dodavanjem pocinilaca, pritisnite 0 --- ")
                        userChoice = input(">>>")
                        if (userChoice) == "0":
                            flag = False
                            break

            if userChoice==4:
                while True:
                    # self.kazna=kazna
                    kazna = input("Cena kazne:")
                    if not kazna.isnumeric():
                        print("Cena kazne moze biti samo izrazena ciframa!")
                        kazna = float(input(">>>"))
                    else:
                        if float(kazna) > 1000000:
                            print("Max cena kazne je 1 000 000 din!")
                            kazna = float(input(">>>"))
                        else:
                            self.kazna = float(kazna)
                            break
            lista=[2,3,4,1]
            if userChoice not in lista:
                print("Uneli ste nepostojecu opciju! Pokusajte ponovo!")

            self.svrha = 2

    def delete_physical(self):

        while True:
            try:
                id = int(input("Unesite evidencioni broj:"))
            except(ValueError, TypeError):
                print("Morate uneti cifre!")
            if id>999999999:
                print("Evidencioni broj ne sadrzi vise od 9 cifara")
            else:
                self.id=id
                break


        self.svrha = 4