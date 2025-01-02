
from app.komunalna_policija import Komunalna
from app.record import *
from app.binary_file import *
from app.constants import *
from app.sequential_file import *
from app.serial_file import *
import os

if __name__ =='__main__':
    #svi podaci moraju biti smesteni u binarno SERIJSKU datoteku-aka aktivna!
    sequential_binary_active= ""
    binary_file_errors=""
    binary_out=""

    flag=True
    while flag:
        list_choice=[1,2,3,4,5,6,7, 8, 0]
        print("Dobrodosli u korisnicki meni! Na raspolaganju se nalaze sledece opcije: ")
        print()
        print()
        print("----------------------- MENI -------------------------")
        print("[1] Formiranje prazne datoteke")
        print("[2] Formiranje aktivne datoteke, sa ucitanim test podacima")
        print("[3] Prikaz naziva aktivne datoteke")
        print("[4] Formiranje serijske i sekvencijalne datoteke promena, zajedno sa izlaznom datotekom")
        print("[5] Prikaz aktivne datoteke")
        print("[6] Prikaz datoteke gresaka")
        print("[7] Prikaz izlazne datoteke")
        print("[0] Izlaz")
        userChoice = (input(">>> "))
   # try:
        userInt=int(userChoice)
        if not (int(userInt) in list_choice):
            print("Odabrali ste nepostojecu opciju! Pokusajte ponovo!!!\n")

        if userInt == 0:
            print("Vidimo se sledeci put! Caos :)")
            break


        if userInt==1:

            while True:
                fileName = input("Unesite naziv aktivne datoteke nad kojom se radi:\n>>> ")
                if fileName=="":
                    print("Ne mozete uneti prazan string!")
                else:

                    file="data/"+fileName+"_sequential.dat"
                    constAttributes=["id", "opis_prekrsaja", "datum_i_vreme","lista_izvrsilaca", "iznos", "status"]
                    formating_s = "i220s17s1500sfi"

                    rec=Record(constAttributes, formating_s, CODING)

                    sequential_binary_active=SequentialFile(file, rec, F)
                    sequential_binary_active.create_active_file()

                    file_serial="data/"+fileName+"_serial.dat"
                    rec = Record(ATTRIBUTES, FMT, CODING)
                    binary_serial = SerialFile(file_serial, rec, F)
                    binary_serial.init_file()


                    break
        #biramo datoteku nad kojom radimo, pre toga zadajemo njen naziv
        if userInt==2:

            while True:
                active_name = input("Unesite naziv aktivne datoteke: ")
                if active_name=="":
                    print("Ne mozete uneti prazan string!")

                else:
                    active_file = "data/" + active_name + "_sequential.dat"

                    constAttributes=["id", "opis_prekrsaja", "datum_i_vreme","lista_izvrsilaca", "iznos", "status"]
                    formating_s = "i220s17s1500sfi"

                    rec=Record(constAttributes, formating_s, CODING)

                    sequential_binary_active=SequentialFile(active_file, rec, F)
                    sequential_binary_active.create_active_file()

                    #umetnuti deo
                    putanja = sequential_binary_active.filename.split("_")[0] + "_serial.dat"
                    rec = Record(ATTRIBUTES, FMT, CODING)
                    binary_file_serial = SerialFile(putanja, rec, F)
                    binary_file_serial.init_file()

                    if sequential_binary_active != "":
                        with open("data/test.csv", "r") as fin:
                            while True:
                                # list_convicted=[]
                                line = fin.readline()
                                if not line:
                                    break
                                list = line.split(';')
                                criminals = list[3].split(",")
                                convicted = ','.join(str(x) for x in criminals)
                                # print(line)
                                # print("-----------------------------------------")
                                #
                                for item in list:
                                    print(item)

                                # print("---------------------------------------------------------------------------")

                                sequential_binary_active.insert_record({"id": int(list[0]),
                                                                        "opis_prekrsaja": list[1],
                                                                        "datum_i_vreme": list[2],
                                                                        "lista_izvrsilaca": convicted,
                                                                        "iznos": float(list[4]),
                                                                        "status": 1}
                                                                       )
                                print("Uspesno ucitani test podaci!")
                break 
        # prikaz naziva aktivne datoteke
        if userInt==3:
            if sequential_binary_active != "":
                print(sequential_binary_active.filename)
                print("Naziv aktivne sekvencijalne datoteke je: ", sequential_binary_active.filename.split("/")[1])

            else:
                print("Ne postoji aktivna datoteka za prikaz!")


        # 4. i 5. stavka zadatka
        if userInt==4:
                if sequential_binary_active=="":
                    print("Greska! Morate kreirati aktivnu datoteku!")


                else:

                    #formiranje vodece serijske datoteke
                    path=sequential_binary_active.filename.split("_")[0]+"_serial.dat"
                    rec=Record(ATTRIBUTES, FMT, CODING)
                    binary_serial=SerialFile(path, rec, F)
                    binary_serial.init_file()

                    print("Odaberite jednu od ponudjenih opcija")


                    print("[1] Kreiraj slog")
                    print("[2] Izmeni slog")
                    print("[3] Fizicki obrisi slog")
                    print("[4] Logicki obrisi slog")
                    print("[0] Izlaz")
                    choices=["1","2","3","4"]

                    while True:
                        userChoice = input(">>>")
                        if userChoice == "" and not choices.__contains__(userChoice):
                            print("Morate uneti jednu od navedenih opcija! Pokusajte ponovo")


                        if userChoice=="0":
                            break


                        if userChoice=="1":
                            if sequential_binary_active!="":
                                object=Komunalna()
                                object.make_an_object()
                                binary_serial.insert_record_no_id_check(object.return_value())

                        if userChoice=="2":
                            if sequential_binary_active != "":
                                object = Komunalna()
                                object.set_new_value()
                                binary_serial.insert_record_no_id_check(object.return_value())


                        if userChoice=="3":
                            if sequential_binary_active!="":
                                object=Komunalna()
                                object.delete_physical()
                                binary_serial.insert_record_no_id_check(object.return_value())


                        if userChoice=="4":
                            if sequential_binary_active!="":
                                object=Komunalna()
                                object.delete_logical()
                                binary_serial.insert_record_no_id_check(object.return_value())

                    #5. stavka-sortiraj serijsku, formiraj sekv
                    sorted_content=binary_serial.get_sorted_content_of_file()

                    pathS=sequential_binary_active.filename.split("_")[0]+"_sequentialNew.dat"
                    rec=Record(ATTRIBUTES, FMT, CODING)
                    new_sequential=SequentialFile(pathS, rec, F)
                    new_sequential.init_file()

                    for content in sorted_content:
                        new_sequential.insert_record_no_id_check(content)

                    #datoteka gresaka, prikaz gresaka na ekranu
                    error_path = sequential_binary_active.filename.split("_")[0] + "_greske.dat"
                    tempAttributes = ["id", "opis_greske"]
                    tempFMT = "i120s"
                    rec = Record(tempAttributes, tempFMT, CODING)
                    binary_file_errors = SequentialFile(error_path, rec, F)
                    binary_file_errors.create_error_file()

                    path_out=sequential_binary_active.filename.split("_")[0]+"_izlazna.dat"
                    attributes_out = ["id", "opis_prekrsaja", "datum_i_vreme", "lista_izvrsilaca", "iznos",
                                       "status"]
                    fmt_out = "i220s17s1500sfi"

                    rec=Record(attributes_out, fmt_out, CODING)
                    binary_out=SequentialFile(path_out, rec,F )
                    binary_out.create_active_file()
                    binary_out.copy_my_file(sequential_binary_active)

                    #izlazna sekvencijalna datoteka
                    new_sequential.perform_operations(binary_out, binary_file_errors)

        if userInt==5:
            if sequential_binary_active!="":
                print("-- Prikaz aktivne datoteke --")
                sequential_binary_active.print_file()
            else:
                print("Aktivna datoteka nije formirana, samim time ne moze se ni prikazati!")

        if userInt == 6:
            if binary_file_errors!="":
                print("-- Prikaz datoteke gresaka --")
                binary_file_errors.print_file()
            else:
                print("Nemoguce prikazati datoteku gresaka, jer nije formirana!")

        if userInt == 7:
            if binary_out!="":
                print("-- Prikaz izlazne datoteke --")
                binary_out.print_file()
            else:
                print("Nemoguce prikazati izlaznu datoteku, jer nije izvrsena nijedna promena!")
        # if userInt==7:
        #
        #
        #
        #     else:
        #         print("\nNemoguce ucitati test podatke u NEICIJALIZOVANU AKTIVNU DATOTEKU!\nPrvo formirajte datoteku, pa pokusajte ponovo :)\n")
