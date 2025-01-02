import os

from app.binary_file import BinaryFile


class SequentialFile(BinaryFile):

    def __init__(self, filename, record, blocking_factor, empty_key=-1):
        BinaryFile.__init__(self, filename, record, blocking_factor, empty_key)

    def init_file(self):
        with open(self.filename, "wb") as f:
            block = self.blocking_factor * [self.get_empty_rec()]
            self.write_block(f, block)

    def __find_in_block(self, block, rec):
        for j in range(self.blocking_factor):
            if block[j].get("id") == self.empty_key or block[j].get("id") > rec.get("id"):
                return True, j

        return False, None

    def insert_record(self, rec):
        if self.find_by_id(rec.get("id")):
            print("Already exists with ID {}".format(rec.get("id")))
            return

        with open(self.filename, "rb+") as f:
            while True:
                block = self.read_block(f)

                if not block:  # EOF
                    break

                last = self.__is_last(block)
                here, j = self.__find_in_block(block, rec)

                if not here:
                    continue

                # save last record for inserting into next block
                tmp_rec = block[self.blocking_factor - 1]
                for k in range(self.blocking_factor - 1, j, -1):
                    block[k] = block[k - 1]  # move records
                block[j] = rec  # insert
                rec = tmp_rec  # new record for insertion

                f.seek(-self.block_size, 1)
                self.write_block(f, block)

                # last block without empty rec?
                if last and block[self.blocking_factor - 1].get("id") != self.empty_key:
                    if len(rec)==6:
                        block = self.blocking_factor * [{"id": self.empty_key, "opis_prekrsaja:": "", "datum_i_vreme": "", "lista_izvrsilaca":"","iznos":0,"status": 0}]
                    elif len(rec)==2:
                        block = self.blocking_factor * [{"id": self.empty_key, "opis_greske": ""}]

                    else:
                        block = self.blocking_factor * [self.get_empty_rec()]
                    self.write_block(f, block)

    def insert_record_no_id_check(self, rec):
        self.find_by_id(rec.get("id"))
        with open(self.filename, "rb+") as f:
            while True:
                block = self.read_block(f)

                if not block:  # EOF
                    break

                last = self.__is_last(block)
                here, j = self.__find_in_block(block, rec)

                if not here:
                    continue

                # save last record for inserting into next block
                tmp_rec = block[self.blocking_factor - 1]
                for k in range(self.blocking_factor - 1, j, -1):
                    block[k] = block[k - 1]  # move records
                block[j] = rec  # insert
                rec = tmp_rec  # new record for insertion

                f.seek(-self.block_size, 1)
                self.write_block(f, block)

                # last block without empty rec?
                if last and block[self.blocking_factor - 1].get("id") != self.empty_key:
                    block = self.blocking_factor * [self.get_empty_rec()]
                    self.write_block(f, block)

    def __is_last(self, block):
        for i in range(self.blocking_factor):
            if block[i].get("id") == self.empty_key:
                return True
        return False

    def print_file(self):
        i = 0
        with open(self.filename, "rb") as f:
            while True:
                block = self.read_block(f)

                if not block:
                    break

                i += 1
                print("Block {}".format(i))
                self.print_block(block)

    def find_by_id(self, id):
        i = 0
        with open(self.filename, "rb") as f:
            while True:
                block = self.read_block(f)

                if not block:
                    return None

                for j in range(self.blocking_factor):
                    if block[j].get("id") == id:
                        return i, j
                    if block[j].get("id") > id:
                        return None

                i += 1

    def delete_by_id(self, id):
        found = self.find_by_id(id)

        if not found:
            return

        block_idx = found[0]
        rec_idx = found[1]
        next_block = None

        with open(self.filename, "rb+") as f:
            while True:
                f.seek(block_idx * self.block_size)  # last block
                block = self.read_block(f)

                for i in range(rec_idx, self.blocking_factor - 1):
                    block[i] = block[i + 1]  # move records

                if self.__is_last(block):  # is last block full?
                    f.seek(-self.block_size, 1)
                    self.write_block(f, block)
                    break

                next_block = self.read_block(f)
                # first record of next block is now the last of current one
                block[self.blocking_factor - 1] = next_block[0]
                f.seek(-2 * self.block_size, 1)
                self.write_block(f, block)

                block_idx += 1
                rec_idx = 0

        if next_block and next_block[0].get("id") == self.empty_key:
            os.ftruncate(os.open(self.filename, os.O_RDWR),
                         block_idx * self.block_size)

    def create_active_file(self):
        #izmenjena lista izvrsilaca-"", a ne []? probaj posle da li puca
        with open(self.filename, "wb") as f:
            block = self.blocking_factor * [{"id": self.empty_key, "opis_prekrsaja": "", "datum_i_vreme": "",
                                             "lista_izvrsilaca": "", "iznos": 0, "status": 0}]
            self.write_block(f, block)

    def create_error_file(self):
        with open(self.filename, "wb") as f:
            block = self.blocking_factor*[{"id": self.empty_key, "opis_greske":""}]
            self.write_block(f, block)

    def copy_my_file(self, activeFile):
        with open(activeFile.filename, "rb") as f:
            while True:
                block = activeFile.read_block(f)
                if not block:
                    break
                for i in range(5):
                    if block[i]["id"] == -1:
                        break
                    self.insert_record(block[i])

    # logicko brisanje prema id-ju
    def logical_delete(self, new_item):
        found = self.find_by_id(new_item["id"])
        if not found:
            return 0
        block_idx = found[0]
        rec_idx = found[1]
        with open(self.filename, "rb+") as f:
            f.seek(block_idx * self.block_size)
            block = self.read_block(f)
            temp = block[rec_idx]
            temp["status"] = 0
            f.seek(-1 * self.block_size, 1)
            self.write_block(f, block)


    def object_update(self, item):
        found = self.find_by_id(item["id"])
        if not found:
            return 0

        block_idx = found[0]
        rec_idx = found[1]

        with open(self.filename, "rb+") as f:
            f.seek(block_idx * self.block_size)
            block = self.read_block(f)
            updated_object = block[rec_idx]

            if item["opis_prekrsaja"] !="":
                updated_object["opis_prekrsaja"] = item["opis_prekrsaja"]

            if item["datum_i_vreme"] !="":
                updated_object["datum_i_vreme"] = item["datum_i_vreme"]

            if item["lista_izvrsilaca"]!="":
                updated_object["lista_izvrsilaca"] = item["lista_izvrsilaca"]

            if item["iznos"] != -1:
                updated_object["iznos"] = item["iznos"]

            f.seek(-1 * self.block_size, 1)
            self.write_block(f, block)


    def perform_operations(self, outf, error):

            num_of_an_object=0
            with open(self.filename, "rb+") as f:

                while True:
                    block = self.read_block(f)
                    if not block:
                        break

                    for object in block:
                        if object["id"] == -1:
                            break

                        # 1 - kreiranje , 2 - azuriranje, 3 - logicko brisanje, 4 - fizicko brisanje
                        if object["svrha"] == 1:
                            #proveravamo da li vec postoji kreiran objekat pod datim id-jem
                            if outf.find_by_id(object["id"]) is not None :
                                num_of_an_object+=1
                                error.insert_record({"id": object["id"],"opis_greske":"Duplikat! Objekat pod datim id-jem vec postoji!["+str(object["id"])+"]"})

                            else:
                                outf.insert_record({"id": object["id"], "opis_prekrsaja": object["opis_prekrsaja"],
                                                    "datum_i_vreme": object["datum_i_vreme"],
                                                 "lista_izvrsilaca": object["lista_izvrsilaca"],
                                                 "iznos": object["iznos"], "status": object["status"]})

                        elif object["svrha"]==2:
                            if outf.find_by_id(object["id"]) is None:
                                num_of_an_object+=1
                                error.insert_record({"id": num_of_an_object, "opis_greske": "Ne postoji objekat sa ID-jem ["+str(object["id"])+"], s toga se ne moze izvrsiti azuriranje!"})

                            else:
                                outf.object_update(object)


                        elif object["svrha"]==3:
                            if outf.find_by_id(object["id"]) is None:
                                num_of_an_object+=1
                                error.insert_record({"id": object["id"],
                                "opis_greske":"Trazeni ID ne postoji["+str(object["id"])+"]"+", nije "
                                "moguce"
                                "izvrsiti logicko brisanje!"})

                            else:
                                outf.logical_delete(object)


                        elif object["svrha"]==4:

                            if outf.find_by_id(object["id"]) is None:
                                error.insert_record({"id": object["id"],
                                "opis_greske":"Trazeni ID ne postoji["+str(object["id"])+"]"+", nije "
                                "moguce"
                                "izvrsiti fizicko brisanje!"})

                            else:
                                outf.delete_by_id(object["id"])
