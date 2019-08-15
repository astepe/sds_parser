import os
import tkinter

from tkinter import ttk
from tabulate import tabulate
from pymongo import MongoClient

from sdsparser.regexes import compile_regexes, search_sds_text
from sdsparser.configs import Configs as PConfigs
from configs import Configs
from configs import MongoServer
from sds_file_manager import update_sds_pool


class RegexDeveloper:
    def __init__(self):
        # repopulates any missing txt files using SDSParser
        update_sds_pool()
        self.manufacturer_name = ""
        self.request_key = ""
        self.SDS_POOL_MANUFACTURERS = [manufacturer for manufacturer in os.listdir(Configs.SDS_PDF_DIRECTORY)]
        self.find_new_manufacturers()
        print("Ready for regex development...")

    def find_new_manufacturers(self):

        with MongoClient() as client:
            regex_collection = client.sdsparser.sdsRegexes
            for manufacturer in self.SDS_POOL_MANUFACTURERS:
                if not regex_collection.find_one({"name": manufacturer}):
                    print(f"New sds pdf manufacturer directory found at {os.path.join(Configs.SDS_PDF_DIRECTORY, manufacturer)}")
                    answer = input(f"Would you like to the new manufacturer {manufacturer} to SDSParser? (Y/N) ")
                    if answer.lower() == "yes" or answer.lower() == "y":
                        print(f"adding new manufacturer {manufacturer} to db. Using default request keys.")
                        default_regexes = regex_collection.find_one({"name": "default"})
                        default_regexes["name"] = manufacturer
                        del default_regexes["_id"]
                        regex_collection.insert_one(default_regexes)
                    else:
                        self.SDS_POOL_MANUFACTURERS.remove(manufacturer)

    @property
    def manufacturer_name(self):
        return self.__manufacturer_name

    @manufacturer_name.setter
    def manufacturer_name(self, manufacturer_name):
        self.__manufacturer_name = manufacturer_name
        if hasattr(self, "request_key") and self.request_key:
            self.refresh_regex()
        self.txt_dir = os.path.join(Configs.SDS_TEXT_DIRECTORY, manufacturer_name)

    @property
    def request_key(self):
        return self.__request_key

    @request_key.setter
    def request_key(self, key):
        self.__request_key = key
        if hasattr(self, "manufacturer_name") and self.manufacturer_name:
            self.refresh_regex()

    def get_regexes_from_database(self, manufacturer_name=None, request_keys=None):
        """
        connect to MongoDB to retrieve current regular expressions
        """

        with MongoClient() as client:

            regex_collection = client.sdsparser.sdsRegexes

            filters = {"_id": 0, "name": 1}
            if request_keys is not None and request_keys:
                filters.update({"regexes." + key: 1 for key in request_keys})

            query = None
            if manufacturer_name is not None:
                query = dict()
                if regex_collection.find_one({"name": manufacturer_name}) is None:
                    print(f"manufacturer {manufacturer_name} not"
                          " currently supported, using default")
                    query.update({"name": "default"})
                else:
                    query.update({"name": manufacturer_name})

            cursor = regex_collection.find(query, filters)

            for regex_dict in cursor:
                yield regex_dict

    def refresh_regex(self):
        regex_gen = self.get_regexes_from_database(
            manufacturer_name=self.manufacturer_name, request_keys=[self.request_key]
        )

        regex_list = list(regex_gen)
        self.db_regex = regex_list[0]["regexes"]
        self.comp_regex_dict = compile_regexes(self.db_regex)

        self.regex = self.comp_regex_dict[self.request_key]

    def execute_search(self):

        regex_dict = dict(self.db_regex)

        regex_dict[self.request_key]["regex"] = self.regex_entry.get()

        comp_regex_dict = compile_regexes(regex_dict)

        self.sds_data = dict()

        for file in os.listdir(self.txt_dir):
            with open(os.path.join(self.txt_dir, file)) as txt:
                text = txt.read()
                self.sds_data[file] = search_sds_text(text, comp_regex_dict)

        self.display_results()

    def display_results(self):
        print("=" * 100)
        headers = ["file name", self.request_key]
        out = [
            [file_name, result[self.request_key]]
            for file_name, result in self.sds_data.items()
        ]
        out.sort(key=lambda x: int(x[0].split("_")[-2]))

        print(tabulate(out, headers=headers, tablefmt="orgtbl"))
        print("=" * 100)
        print()

    def save_regex(self):

        with MongoClient() as client:

            collection = client.sdsparser.sdsRegexes

            new_regex = self.regex_entry.get()

            collection.update_one(
                {"name": self.manufacturer_name},
                {"$set": {"regexes." + self.request_key + ".regex": new_regex}},
            )

    def start(self):
        def get_regex():
            self.manufacturer_name = manufacturer.get()
            self.request_key = request_key.get()
            self.regex_entry.delete(0, tkinter.END)
            self.regex_entry.insert(0, self.regex.pattern)

        root = tkinter.Tk()
        root.title("SDS Regular Expression Developer")

        manufacturer = tkinter.StringVar(root)
        manufacturer.set(self.manufacturer_name)
        manufacturer_menu = ttk.OptionMenu(
            root, manufacturer, *sorted(self.SDS_POOL_MANUFACTURERS)
        )
        manufacturer_menu.pack()

        request_key = tkinter.StringVar(root)
        request_key.set("flash_point")
        request_key_menu = ttk.OptionMenu(
            root, request_key, *sorted(PConfigs.REQUEST_KEYS)
        )
        request_key_menu.pack()

        get_button = ttk.Button(root, text="Get Regex", command=get_regex)
        get_button.pack()

        self.regex_entry = ttk.Entry(root, width=100, font="Helvetica 18")
        self.regex_entry.pack()

        save = ttk.Button(root, text="Save Regex", command=self.save_regex)
        save.pack()

        execute_button = ttk.Button(
            root, text="Execute", command=self.execute_search
        )
        execute_button.pack()

        root.mainloop()


if __name__ == "__main__":
    with MongoServer() as server:

        if 'sdsparser' not in MongoClient().list_database_names():
            print("'sdsparser' not a defined db, "
                  "importing regexes.json to new mongo db...")
            server.import_from_static_file()
            
        rd = RegexDeveloper()
        rd.start()
