import tkinter
from tkinter import ttk
from tkinter import messagebox

from cargo_accounting import CargoAccounting
from cargo import Cargo
from truck import Truck, TRUCKS

BG_COLOR = "#0d47a1"
BUTTON_COLOR = "#cfd8dc"
FRAME_COLOR = "#eceff1"

DEFAULT_FONT_SMALL = ("Arial", 10)
DEFAULT_FONT = ("Arial", 12)
DEFAULT_FONT_BIG = ("Arial", 16)


class AccountingApp:
    def __init__(self):
        self.running = True
        self.root = tkinter.Tk()
        self.account = CargoAccounting()

        self.listbox_values = self.account.show_all_trucks()
        self.listbox = tkinter.Listbox()
        self.info_label = None
        self.left_frame = tkinter.LabelFrame(self.root, bg=FRAME_COLOR)
        self.center_frame = tkinter.Frame(self.root, bg=FRAME_COLOR)
        self.right_frame = tkinter.Frame(self.root, bg=FRAME_COLOR)

    def setup_window(self):
        self.root['bg'] = BG_COLOR
        self.root.title("Транспортный учет перевозок")
        self.root.geometry("1280x720")
        self.root.resizable(True, True)
        self.root.minsize(1160, 630)

    def setup_frames(self):
        left_width = 0.33
        self.left_frame.config(text="Бронирование перевозок", font=DEFAULT_FONT)
        self.left_frame.place(relx=0.01, rely=0.01, relwidth=left_width, relheight=0.98)
        self.center_frame.place(relx=left_width + 0.02, rely=0.01, relwidth=left_width - 0.01, relheight=0.98)
        self.right_frame.place(relx=left_width * 2 + 0.02, rely=0.01, relwidth=left_width - 0.02, relheight=0.98)

    def setup_sort_buttons(self):
        sort_button = tkinter.Button(master=self.right_frame,
                                     text="Показать машины в работе",
                                     font=DEFAULT_FONT,
                                     bg=BUTTON_COLOR)
        sort_button.config(command=lambda: (self.update_listbox(self.account.show_trucks_at_work())))
        sort_button.pack(side="top", fill="x")

        sort_button1 = tkinter.Button(master=self.right_frame,
                                      text="Показать доступные машины",
                                      font=DEFAULT_FONT,
                                      bg=BUTTON_COLOR)
        sort_button1.config(command=lambda: (self.update_listbox(self.account.show_available_trucks())))
        sort_button1.pack(side="top", fill="x")

        sort_button2 = tkinter.Button(master=self.right_frame,
                                      text="Показать все машины",
                                      font=DEFAULT_FONT,
                                      bg=BUTTON_COLOR)

        sort_button2.config(command=lambda: (self.update_listbox(self.account.show_all_trucks())))
        sort_button2.pack(side="top", fill="x")

        sort_button3 = tkinter.Button(master=self.right_frame,
                                      text="Отсортировать по грузоподъемности",
                                      font=DEFAULT_FONT,
                                      bg=BUTTON_COLOR)
        sort_button3.config(
            command=lambda: self.update_listbox(self.account.sort_by_load_capacity(self.listbox_values, from_max=True)))
        sort_button3.pack(side="top", fill="x")

    def setup_add_button(self):
        add_button = tkinter.Button(master=self.center_frame,
                                    text="Добавить машины в автопарк",
                                    font=DEFAULT_FONT,
                                    bg=BUTTON_COLOR)

        def add_trucks():
            window = tkinter.Toplevel()
            window['bg'] = BG_COLOR
            window.geometry("300x200+300+200")
            window.resizable(False, False)
            window.title("Добавление машины")

            type_label_frame = tkinter.LabelFrame(master=window,
                                                  bg=FRAME_COLOR,
                                                  text="Выберите тип машины",
                                                  font=DEFAULT_FONT)

            trucks_options = [truck.upper() for truck in TRUCKS.keys()]
            choose_type = ttk.Combobox(master=type_label_frame,
                                       values=trucks_options)

            type_label_frame.place(rely=0.01, relx=0.01, relwidth=0.98, relheight=0.4)
            choose_type.set(trucks_options[0])
            choose_type.pack()

            amount_label_frame = tkinter.LabelFrame(master=window,
                                                    bg=FRAME_COLOR,
                                                    text="Укажите количество",
                                                    font=DEFAULT_FONT)

            choose_amount = tkinter.Scale(master=amount_label_frame,
                                          from_=1,
                                          to=10,
                                          orient="horizontal",
                                          troughcolor=FRAME_COLOR,
                                          relief=tkinter.FLAT)

            amount_label_frame.place(rely=0.42, relx=0.01, relwidth=0.98, relheight=0.4)
            choose_amount.pack(fill="x")

            submit_button = tkinter.Button(master=window,
                                           text="Принять",
                                           font=DEFAULT_FONT,
                                           bg=BUTTON_COLOR)

            def submit():
                for _ in range(int(choose_amount.get())):
                    truck = Truck(choose_type.get())
                    self.account.add_truck(truck)

            submit_button.config(command=lambda: (submit(),
                                                  self.update_listbox(self.account.show_all_trucks()),
                                                  window.destroy()))
            submit_button.pack(side="bottom", fill="x")

        add_button.config(command=add_trucks)
        add_button.pack(side="top", fill="x")

    def setup_remove_info_button(self):
        remove_info_button = tkinter.Button(master=self.center_frame,
                                            text="Скрыть информацию",
                                            font=DEFAULT_FONT,
                                            bg=BUTTON_COLOR)

        def remove_info():
            self.info_label.config(text='', compound='top')

        remove_info_button.config(command=remove_info)
        remove_info_button.pack(side="top", fill="x")

    def setup_remove_button(self):
        remove_button = tkinter.Button(master=self.center_frame,
                                       text="Удалить машины из автопарка",
                                       font=DEFAULT_FONT,
                                       bg=BUTTON_COLOR)

        def remove_trucks():
            window = tkinter.Toplevel()
            window['bg'] = BG_COLOR
            window.geometry("300x100+300+200")
            window.resizable(False, False)
            window.title("Удаление машин")

            label_frame = tkinter.LabelFrame(master=window,
                                             bg=FRAME_COLOR)

            label = tkinter.Label(master=label_frame,
                                  text="Удалить выделенные машины?\n\n"
                                       "(это действие нельзя отменить)",
                                  font=DEFAULT_FONT,
                                  bg=FRAME_COLOR)

            submit_button = tkinter.Button(master=label_frame,
                                           text="Да",
                                           font=DEFAULT_FONT,
                                           bg=BUTTON_COLOR)

            def delete_trucks():
                for item in self.listbox.curselection()[::-1]:
                    removed_truck = self.listbox_values.pop(item)
                    self.listbox.delete(item)
                    self.account.remove_truck(removed_truck)
                    self.info_label.config(text='', compound='top')

            submit_button.config(command=lambda: (window.destroy(),
                                                  delete_trucks()))
            label_frame.pack(fill="both", expand=True)
            submit_button.pack(fill="x", side="bottom")
            label.pack()

        remove_button.config(command=remove_trucks)
        remove_button.pack(side="top", fill="x")

    # noinspection PyTypeChecker
    def setup_request_frame(self):

        cargo_list_label = tkinter.Label(master=self.left_frame,
                                         font=DEFAULT_FONT,
                                         bg=FRAME_COLOR,
                                         text="Список грузов на доставку:")

        cargos_var = tkinter.StringVar(value=[])

        cargo_listbox = tkinter.Listbox(master=self.left_frame,
                                        listvariable=cargos_var,
                                        bg=FRAME_COLOR,
                                        font=DEFAULT_FONT,
                                        selectmode="extended",
                                        relief=tkinter.FLAT)

        scrollbar = tkinter.Scrollbar(master=self.left_frame,
                                      orient="vertical",
                                      command=cargo_listbox.yview)

        cargo_listbox["yscrollcommand"] = scrollbar.set

        cargo_list_label.place(rely=0.2, relx=0.05, relwidth=0.9, relheight=0.05)
        scrollbar.place(rely=0.25, relx=0.91, relwidth=0.04, relheight=0.5)
        cargo_listbox.place(rely=0.25, relx=0.05, relwidth=0.9, relheight=0.5)

        self.setup_request_buttons(cargo_listbox)

    def setup_request_buttons(self, cargo_listbox):

        add_cargo_button = tkinter.Button(master=self.left_frame,
                                          text="Добавить груз",
                                          font=DEFAULT_FONT,
                                          bg=BUTTON_COLOR)

        def add_cargo():
            window = tkinter.Toplevel()
            window['bg'] = BG_COLOR
            window.geometry("300x450+600+200")
            window.resizable(False, False)
            window.title("Добавление груза")

            widget_height = 0.14

            # ----------------------------------------------------------------
            name_label_frame = tkinter.LabelFrame(master=window,
                                                  bg=FRAME_COLOR,
                                                  text="Название груза",
                                                  font=DEFAULT_FONT)
            name_label_frame.place(rely=0.01, relheight=widget_height, relx=0.01, relwidth=0.98)

            entry_name = tkinter.Entry(master=name_label_frame,
                                       font=DEFAULT_FONT,
                                       textvariable=tkinter.StringVar(value="ГРУЗ"))
            entry_name.pack(fill="x")
            # ----------------------------------------------------------------
            dimensions_label_frame = tkinter.LabelFrame(master=window,
                                                        bg=FRAME_COLOR,
                                                        text="Информация о грузе",
                                                        font=DEFAULT_FONT)
            dimensions_label_frame.place(rely=0.01 + widget_height, relheight=widget_height * 4, relx=0.01,
                                         relwidth=0.98)

            tkinter.Label(master=dimensions_label_frame,
                          font=DEFAULT_FONT_SMALL,
                          text="Масса груза (кг)").pack(fill="x")

            entry_mass = tkinter.Entry(master=dimensions_label_frame,
                                       font=DEFAULT_FONT,
                                       textvariable=tkinter.StringVar(value="1"))
            entry_mass.pack(fill="x")
            # ----------------------------------------------------------------
            tkinter.Label(master=dimensions_label_frame,
                          font=DEFAULT_FONT_SMALL,
                          text="Длина груза (м)").pack(fill="x")

            entry_length = tkinter.Entry(master=dimensions_label_frame,
                                         font=DEFAULT_FONT,
                                         textvariable=tkinter.StringVar(value="1"))
            entry_length.pack(fill="x")
            # ----------------------------------------------------------------
            tkinter.Label(master=dimensions_label_frame,
                          font=DEFAULT_FONT_SMALL,
                          text="Ширина груза (м)").pack(fill="x")

            entry_width = tkinter.Entry(master=dimensions_label_frame,
                                        font=DEFAULT_FONT,
                                        textvariable=tkinter.StringVar(value="1"))
            entry_width.pack(fill="x")
            # ----------------------------------------------------------------
            tkinter.Label(master=dimensions_label_frame,
                          font=DEFAULT_FONT_SMALL,
                          text="Высота груза (м)").pack(fill="x")

            entry_height = tkinter.Entry(master=dimensions_label_frame,
                                         font=DEFAULT_FONT,
                                         textvariable=tkinter.StringVar(value="1"))
            entry_height.pack(fill="x")
            # ----------------------------------------------------------------
            tkinter.Label(master=dimensions_label_frame,
                          font=DEFAULT_FONT_SMALL,
                          text="Адрес назначения (город)").pack(fill="x")

            entry_city = tkinter.Entry(master=dimensions_label_frame,
                                       font=DEFAULT_FONT,
                                       textvariable=tkinter.StringVar(value="Москва"))
            entry_city.pack(fill="x")
            # ----------------------------------------------------------------
            amount_label_frame = tkinter.LabelFrame(master=window,
                                                    bg=FRAME_COLOR,
                                                    text="Количество",
                                                    font=DEFAULT_FONT)
            amount_label_frame.place(rely=0.01 + widget_height * 5, relheight=widget_height * 1.5, relx=0.01,
                                     relwidth=0.98)

            choose_amount = tkinter.Scale(master=amount_label_frame,
                                          from_=1,
                                          to=100,
                                          orient="horizontal",
                                          troughcolor=FRAME_COLOR,
                                          relief=tkinter.FLAT)

            choose_amount.pack(fill="both", expand=True)
            # ----------------------------------------------------------------
            submit_button = tkinter.Button(master=window,
                                           text="Принять",
                                           font=DEFAULT_FONT,
                                           bg=BUTTON_COLOR)

            def submit():
                for i in range(int(choose_amount.get())):
                    assert entry_name.get().isalpha(), "Название должно состоять только из букв"
                    assert all([entry_mass.get().isdecimal(),
                                entry_length.get().isdecimal(),
                                entry_width.get().isdecimal(),
                                entry_height.get().isdecimal()]), "Неверная информация о грузе\n" \
                                                                  "В полях должно быть числовое значение"
                    assert entry_city.get(), "Поле адреса не должно быть пустым"

                    new_cargo = f"{entry_name.get()} | {entry_mass.get()} кг | " \
                                f"{entry_length.get()} x {entry_width.get()} x {entry_height.get()} | " \
                                f"{entry_city.get()}"
                    cargo_listbox.insert(i, new_cargo)

            def destroy_window():
                try:
                    submit()
                    window.destroy()
                except AssertionError as error:
                    messagebox.showerror(title='Ошибка', message=str(error))

            submit_button.config(command=destroy_window)
            submit_button.place(rely=0.01 + widget_height * 6, relheight=widget_height, relx=0.01, relwidth=0.98)

        add_cargo_button.config(command=add_cargo)
        add_cargo_button.place(rely=0.1, relx=0.05, relwidth=0.45, relheight=0.1)

        remove_cargo_button = tkinter.Button(master=self.left_frame,
                                             text="Удалить выделенное",
                                             font=DEFAULT_FONT,
                                             bg=BUTTON_COLOR)

        remove_cargo_button.config(
            command=lambda: [cargo_listbox.delete(i) for i in cargo_listbox.curselection()[::-1]])
        remove_cargo_button.place(rely=0.1, relx=0.5, relwidth=0.45, relheight=0.1)

        request_button = tkinter.Button(master=self.left_frame,
                                        text="Забронировать\n перевозку",
                                        font=DEFAULT_FONT_BIG,
                                        bg=BUTTON_COLOR)

        def request():
            cargos_str = cargo_listbox.get(0, tkinter.END)
            cargos = {}
            for cargo in cargos_str:
                cargo = cargo.split("|")
                name = cargo[0]
                weight = float(cargo[1].split(" ")[1])
                length, width, height = map(lambda x: float(x.strip()), cargo[2].split("x"))
                destination = cargo[3]
                new_cargo = Cargo(
                    name=name,
                    weight=weight,
                    length=length,
                    width=width,
                    height=height,
                )
                if cargos.get(destination):
                    cargos[destination].append(new_cargo)
                else:
                    cargos[destination] = [new_cargo]

            for where_to_ship in cargos:
                if self.account.request_transportation(cargos[where_to_ship], where_to_ship):
                    cargo_listbox.delete(0, tkinter.END)
                else:
                    window = tkinter.Toplevel()
                    window['bg'] = BUTTON_COLOR
                    window.geometry("350x150+400+50")
                    window.resizable(False, False)
                    window.title("Ошибка")

                    tkinter.Label(window, text=f"Нельзя забронировать перевозку"
                                               f'\nгруза в "{where_to_ship}".'
                                               f"\nНе хватает вместимости машин.",
                                  bg=BUTTON_COLOR,
                                  font=DEFAULT_FONT).pack(side="top", fill="both")

                    tkinter.Button(window, text="Okay", command=window.destroy).pack(side="bottom", fill="x")

            self.update_listbox(self.account.show_all_trucks())

        request_button.config(command=request)
        request_button.place(rely=0.8, relx=0.05, relwidth=0.9, relheight=0.15)

    def update_truck_info_box(self):
        if self.info_label is None:
            self.info_label = tkinter.Label(master=self.center_frame,
                                            font=DEFAULT_FONT,
                                            bg=FRAME_COLOR)

            self.info_label.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.7)

        text = "ХАРАКТЕРИСТИКИ МАШИНЫ:\n\n"
        try:
            if self.listbox.curselection():
                selected_truck = self.listbox_values[self.listbox.curselection()[0]]
            else:
                selected_truck = self.listbox_values[0]
        except IndexError:
            return

        text += f"Модель: {selected_truck.name};\n"
        text += f"Номер: {selected_truck.plate};\n"
        text += f"Грузоподъемность: {selected_truck.load_capacity} т;\n"
        text += f"Длина: {selected_truck.length} м;\n"
        text += f"Ширина: {selected_truck.width} м;\n"
        text += f"Высота: {selected_truck.height} м;\n"
        text += f"Объем кузова: {selected_truck.holding_capacity} м^3;\n"
        text += f"Статус: {'работает' if selected_truck.at_work else 'свободен'};\n"
        text += f"Назначение: {selected_truck.destination}.\n"
        self.info_label.config(text=text, compound='top')

    def setup_listbox(self):
        trucks_var = tkinter.StringVar(value=self.listbox_values)

        self.listbox = tkinter.Listbox(master=self.right_frame,
                                       listvariable=trucks_var,
                                       bg=FRAME_COLOR,
                                       font=DEFAULT_FONT,
                                       selectmode="extended",
                                       relief=tkinter.FLAT)

        scrollbar = tkinter.Scrollbar(master=self.right_frame,
                                      orient="vertical",
                                      command=self.listbox.yview)

        self.listbox["yscrollcommand"] = scrollbar.set

        scrollbar.pack(side="right", fill="y")

        self.listbox.bind("<<ListboxSelect>>", self.update_truck_info_box)

        self.listbox.pack(fill="both", expand=True)

    def update_listbox(self, trucks):
        if self.listbox is None:
            self.setup_listbox()
        self.listbox_values = trucks
        trucks_var = tkinter.StringVar(value=trucks)
        self.listbox.config(listvariable=trucks_var)

    def start(self):
        self.setup_window()
        self.setup_frames()
        self.setup_sort_buttons()
        self.setup_add_button()
        self.setup_remove_button()
        self.setup_remove_info_button()
        self.setup_request_frame()

        self.listbox_values = self.account.show_all_trucks()
        self.setup_listbox()

        self.update_truck_info_box()

        if self.running:
            self.root.mainloop()
