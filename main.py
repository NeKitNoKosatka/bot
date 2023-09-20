import dearpygui.dearpygui as dpg
import parsing_system as ps
import vk
import time
import functions as fun
import os
#from dotenv import load_dotenv
import configparser

import tkinter as tk
from tkinter import messagebox as mb

dpg.create_context()
dpg.create_viewport(title='Bot itprotect', x_pos=0, y_pos=0)
dpg.maximize_viewport()



# path = os.path.join(os.path.dirname(__file__), 'data.env')
# load_dotenv(path)
# access_token = os.getenv("ACCESS_TOKEN")

#all_api_tokens = fun.get_all_tokens()
#all_api_tokens.append("qwerty")
# os.environ['TOKENS'] = ",".join(all_api_tokens)




#config["DATA"]['TOKENS'] = ",".join(all_api_tokens)

#print(config["DATA"]['TOKENS'])
# config["DATA"]['ACCESS_TOKEN'] = access_token
#config["DATA"]['TOKENS'] = ",".join(all_api_tokens)




#dpg.set_viewport_small_icon("path/to/icon.ico")
#dpg.set_viewport_large_icon("path/to/icon.ico")


with dpg.font_registry():
    with dpg.font("LCDNOVA.ttf", 14, default_font=True) as font1:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        # dpg.add_font_range(0x0400, 0x04FF)

    # with dpg.font("VinSlabPro.ttf", 14) as font2:
    #     dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    #     dpg.add_char_remap(0x007A, 0x044F)    #[0x00E0, 0x00E4],[0x0430,0x0434]


def start_parsing():
    if dpg.is_item_enabled(input_parsing_1):
        groupid = dpg.get_value(input_parsing_1)

        try:
            users = ps.get_members(groupid)
            ps.save_data(users)
            dpg.configure_item("parsing_success", show=True)
        except vk.exceptions.VkAPIError:
            dpg.configure_item("group_access_error", show=True)
            #users = None
        print(ps.get_members(groupid))
    elif dpg.is_item_enabled(input_parsing_2_1) and dpg.is_item_enabled(input_parsing_2_2):
        g_1 = dpg.get_value(input_parsing_2_1)
        g_2 = dpg.get_value(input_parsing_2_2)

        try:
            groupid_1 = ps.get_members(g_1)
            groupid_2 = ps.get_members(g_2)
            users = ps.union_members(groupid_1, groupid_2)
            print(users)
            ps.save_data(users)
            dpg.configure_item("parsing_success", show=True)
        except vk.exceptions.VkAPIError:
            dpg.configure_item("group_access_error", show=True)
        print(ps.get_members(g_1))
        print(ps.get_members(g_2))
    elif dpg.is_item_enabled(input_parsing_3_1) and dpg.is_item_enabled(input_parsing_3_2):
        g_1 = dpg.get_value(input_parsing_3_1)
        g_2 = dpg.get_value(input_parsing_3_2)

        try:
            groupid_1 = ps.get_members(g_1)
            groupid_2 = ps.get_members(g_2)
            users = ps.get_intersection(groupid_1, groupid_2)
            print(users)
            ps.save_data(users)
            dpg.configure_item("parsing_success", show=True)
        except vk.exceptions.VkAPIError:
            dpg.configure_item("group_access_error", show=True)
        print(ps.get_members(g_1))
        print(ps.get_members(g_2))


def parsing_1():
    dpg.configure_item(input_parsing_1, show=True, enabled=True)
    dpg.configure_item(input_parsing_2_1, show=False, enabled=False)
    dpg.configure_item(input_parsing_2_2, show=False, enabled=False)
    dpg.configure_item(input_parsing_3_1, show=False, enabled=False)
    dpg.configure_item(input_parsing_3_2, show=False, enabled=False)

def parsing_2():
    dpg.configure_item(input_parsing_2_1, show=True, enabled=True)
    dpg.configure_item(input_parsing_2_2, show=True, enabled=True)
    dpg.configure_item(input_parsing_1, show=False, enabled=False)
    dpg.configure_item(input_parsing_3_1, show=False, enabled=False)
    dpg.configure_item(input_parsing_3_2, show=False, enabled=False)

def parsing_3():
    dpg.configure_item(input_parsing_3_1, show=True, enabled=True)
    dpg.configure_item(input_parsing_3_2, show=True, enabled=True)
    dpg.configure_item(input_parsing_1, show=False, enabled=False)
    dpg.configure_item(input_parsing_2_1, show=False, enabled=False)
    dpg.configure_item(input_parsing_2_2, show=False, enabled=False)

def open_parsing_system(sender, app_data):
    def back():
        dpg.delete_item(parsing_window)
        dpg.show_item(main_window)
        dpg.set_primary_window("main", True)

    dpg.hide_item(main_window)
    parsing_window = dpg.add_window(tag="parsing")
    dpg.set_primary_window("parsing", True)

    back_button = dpg.add_button(label="Назад", parent=parsing_window, callback=back)

    global input_parsing_1
    global input_parsing_2_1
    global input_parsing_2_2
    global input_parsing_3_1
    global input_parsing_3_2

    parsing_button_1 = dpg.add_button(label="Парсинг участников одного сообщества", parent=parsing_window, callback=parsing_1)
    input_parsing_1 = dpg.add_input_text(hint="Введите id группы для парсинга участников", parent=parsing_window, before=parsing_button_1, show=False, enabled=False)

    parsing_button_2 = dpg.add_button(label="Парсинг участников двух сообществ (без повторов)", parent=parsing_window, callback=parsing_2)
    input_parsing_2_2 = dpg.add_input_text(hint="Введите id 2-ой группы для парсинга участников:", parent=parsing_window, before=parsing_button_2, show=False, enabled=False)
    input_parsing_2_1 = dpg.add_input_text(hint="Введите id 1-ой группы для парсинга участников:", parent=parsing_window, before=input_parsing_2_2, show=False, enabled=False)

    parsing_button_3 = dpg.add_button(label="Найти пересечение участников двух сообществ", parent=parsing_window, callback=parsing_3)
    input_parsing_3_2 = dpg.add_input_text(hint="Введите id 2-ой группы для парсинга участников:", parent=parsing_window, before=parsing_button_3, show=False, enabled=False)
    input_parsing_3_1 = dpg.add_input_text(hint="Введите id 1-ой группы для парсинга участников:", parent=parsing_window, before=input_parsing_3_2, show=False, enabled=False)


    # dpg.bind_item_font(parsing_button_1, font1)
    # dpg.bind_item_font(input_parsing_1, font1)
    # dpg.bind_item_font(parsing_button_2, font1)
    # dpg.bind_item_font(input_parsing_2_1, font1)
    # dpg.bind_item_font(input_parsing_2_2, font1)
    # dpg.bind_item_font(parsing_button_3, font1)
    # dpg.bind_item_font(input_parsing_3_1, font1)
    # dpg.bind_item_font(input_parsing_3_2, font1)

    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")

    with dpg.table(header_row=False, before=input_parsing_1, parent=parsing_window, policy=dpg.mvTable_SizingFixedSame):
        dpg.add_table_column()
        dpg.add_table_column()
        with dpg.table_row():
            text_2 = dpg.add_text("Система парсинга:")
            #dpg.bind_item_font(text_2, font1)
            ok_button = dpg.add_button(label="Старт", callback=start_parsing)
            #dpg.bind_item_font(ok_button, font1)


def edit_bot(sender):
    def close_button_fun():
        dpg.delete_item(ch)
        dpg.delete_item("show_bots")

    def save_token_change():
        all_api_tokens[n] = dpg.get_value(edited_token)
        dpg.configure_item("text_token_"+str(n), default_value=dpg.get_value(edited_token))
        dpg.delete_item("show_bots")
        dpg.configure_item(ch, show=False)
        fun.edit_tokens(all_api_tokens)
        #os.environ['TOKENS'] = ",".join(all_api_tokens)
        print (all_api_tokens)

    print("edited")
    n = int(sender[11:])
    token_to_edit = all_api_tokens[n]

    with dpg.window(autosize=True,no_title_bar=True) as ch:
        dpg.add_button(label="X", pos=[790,5], callback=close_button_fun)
        dpg.add_text("Изменить токен")
        edited_token = dpg.add_input_text(default_value=token_to_edit, width=800)
        dpg.add_button(label="Сохранить", callback=save_token_change)
    print(n)
    print(token_to_edit)

def delete_bot(sender):
    def cansel_button_fun():
        dpg.delete_item(dl)
        dpg.delete_item("show_bots")

    def save_token_change():
        all_api_tokens.pop(n)
        dpg.delete_item("bots")
        dpg.delete_item("show_bots")
        dpg.configure_item(dl, show=False)
        open_bots_menu_system(sender="deleting",app_data="deleting")
        fun.edit_tokens(all_api_tokens)
        #os.environ['TOKENS'] = ",".join(all_api_tokens)
        print (all_api_tokens)

    print("deleted")
    #print(all_api_tokens)
    n = int(sender[13:])
    #print(n)
    token_to_edit = all_api_tokens[n]

    with dpg.window(autosize=True,no_title_bar=True) as dl:
        dpg.add_button(label="X", pos=[790,5], callback=cansel_button_fun)
        dpg.add_text(f"Удалить токен (id:{n})?")

        with dpg.group(horizontal=True):
            dpg.add_button(label="Удалить", width=85, callback=save_token_change)
            dpg.add_button(label="Отмена", width=75, callback=cansel_button_fun)
    #print(n)
    print(token_to_edit)

def open_all_bots_window():
    global all_api_tokens

    config = configparser.ConfigParser()
    config.read('db.config')

    all_api_tokens = fun.get_all_tokens()
    #print(all_api_tokens)
    with dpg.window(autosize=True, modal=True, show=True, tag="show_bots", no_title_bar=True) as all_bots:
        token_tag = "token_"
        main_text = dpg.add_text("Доступные боты:")
        dpg.add_separator()
        dpg.add_button(label="X", pos=[170,8], width=50, callback=lambda: dpg.delete_item("show_bots"))
        with dpg.table(header_row=False, parent=all_bots, policy=dpg.mvTable_SizingFixedFit):
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            for i in range(len(all_api_tokens)):
                with dpg.table_row():
                    token_tag += str(i)
                    id_text = dpg.add_text(f"id:{i}")
                    edit_button = dpg.add_button(label="Изменить", tag="edit_"+token_tag, callback=edit_bot)
                    delete_button = dpg.add_button(label="Удалить", tag="delete_"+token_tag, callback=delete_bot)
                    #print(fun.get_all_tokens()[i])
                    api_token_text = dpg.add_text(all_api_tokens[i], tag="text_"+token_tag)
                    token_tag = "token_"


def add_bots():
    def save_token_change():
        is_api_entered = False
        token_tag = "token_"

        config = configparser.ConfigParser()
        config.read('db.config')
        #has_option = config.has_option("DATA", 'access_token')

        for i in range(new_bots_num):
            token_tag += str(i)
            new_token = dpg.get_value("api_input_" + token_tag)

            if new_token != "":
                if config['DATA']["ACCESS_TOKEN"] == "":
                    config['DATA']['ACCESS_TOKEN'] = new_token
                    with open('db.config', 'w') as configfile:
                        config.write(configfile)
                    print("access token: ", new_token)

                new_bots.append(new_token)
                is_api_entered = True
            elif new_token == "":

                is_api_entered = False
                print("no_api_error")

            token_tag = "token_"

        if is_api_entered:
            print("saved")
            dpg.delete_item("add_bots")
        else:
            dpg.configure_item("no_api_error", show=True)

        fun.add_bots(new_bots_num, enter=new_bots)

        #fun.edit_tokens(all_api_tokens)
        #os.environ['TOKENS'] = ",".join(all_api_tokens)
        #print (all_api_tokens)
        print(new_bots)

    new_bots_num = dpg.get_value("add_bots_num")
    new_bots = []
    token_tag = "token_"

    save_button = dpg.add_button(label="Сохранить", callback=save_token_change, parent="add_bots")

    for i in range(new_bots_num):
        token_tag += str(i)
        # print(fun.get_all_tokens()[i])
        api_token_input = dpg.add_input_text(default_value="", label="Введите API токен", tag="api_input_" + token_tag, parent="add_bots", before=save_button)
        token_tag = "token_"

    #add_button = dpg.add_button(label="Добавить", tag="add_" + token_tag, callback=save_token_change)

    # with dpg.table(header_row=False, parent=all_bots, policy=dpg.mvTable_SizingFixedFit):
    #     dpg.add_table_column()
    #     dpg.add_table_column()
    #     for i in range(len(new_bots_num)):
    #         with dpg.table_row():
    #             token_tag += str(i)
    #             add_button = dpg.add_button(label="Добавить", tag="add_"+token_tag, callback=save_token_change)
    #             #print(fun.get_all_tokens()[i])
    #             api_token_input = dpg.add_input_text(hint="Введите API токен", tag="api_input_"+token_tag)
    #             token_tag = "token_"


def open_bots_add_window():
    with dpg.window(autosize=True, modal=True, show=True, tag="add_bots", no_title_bar=True) as add_bots_window: #, no_close=True, no_collapse=True
        def back():
            dpg.delete_item("add_bots")
            dpg.show_item("bots")
            # dpg.set_primary_window("main", True)

        back_button = dpg.add_button(label="Назад", callback=back)
        main_text = dpg.add_text("Добавить ботов:")
        dpg.add_separator()
        dpg.add_input_int(label="Введите количество ботов для добавления", tag="add_bots_num", width=150, min_value=1, min_clamped=True, default_value=1)
        add_bots_button = dpg.add_button(label="Добавить", callback=add_bots)

def open_bots_menu_system(sender, app_data):
    def back():
        dpg.delete_item(bots_menu_window)
        dpg.show_item(main_window)
        dpg.set_primary_window("main", True)

    dpg.hide_item(main_window)
    bots_menu_window = dpg.add_window(tag="bots")
    dpg.set_primary_window("bots", True)

    back_button = dpg.add_button(label="Назад", parent=bots_menu_window, callback=back)
    all_bots_button = dpg.add_button(label="Посмотреть доступных ботов", parent=bots_menu_window, callback=open_all_bots_window)
    add_bots_button = dpg.add_button(label="Добавить новых ботов", parent=bots_menu_window, callback=open_bots_add_window)


def open_message_menu():
    app = App()
    #app.Entry()
    app.mainloop()


    # with dpg.window(autosize=True, popup=True, show=True, tag="message", no_title_bar=True):
    #     def ok_button_fun():
    #         txt = dpg.get_value(message_text)
    #         print(txt)
    #         with open("message.txt", 'w', encoding='utf-8') as file:
    #             file.write(dpg.get_value(message_text))
    #         dpg.delete_item("message")
    #
    #     head_text = dpg.add_text("Введите сообщение для рассылки")
    #     dpg.add_separator()
    #     #txt = ""
    #     with open("message.txt", 'r', encoding='utf-8') as file:
    #         txt = file.read()
    #     message_text = dpg.add_input_text(default_value=txt, multiline=True)
    #     dpg.add_button(label="OK", width=75, callback=ok_button_fun)

        # dpg.bind_font(font2)
        #dpg.bind_item_font(message_text, font2)

def start_mailing():
    # all_time = int(fun.all_time())
    f = fun.start_mailing()
    if not f:
        dpg.configure_item("mailing_text", default_value="Рассылка завершена")
        dpg.configure_item("time", default_value={'hour': 0, 'min': 0, 'sec': 0})

    # progress_bar = dpg.add_progress_bar(parent="mailing", before="start_button")
    #
    # for i in range(all_time + 1):
    #     percent = i/all_time
    #     dpg.configure_item(progress_bar, default_value=percent)
    #     time.sleep(1)



def open_mailing_window():
    with dpg.window(autosize=True, modal=True, show=True, tag="mailing", no_title_bar=True, no_close=True, no_collapse=True) as mailing_window:
        def back():
            dpg.delete_item("mailing")
            dpg.show_item("main")
            # dpg.set_primary_window("main", True)

        back_button = dpg.add_button(label="Назад", callback=back)
        main_text = dpg.add_text("Рассылка")
        dpg.add_separator()
        dpg.add_text("Рассылка займёт:", tag="mailing_text")
        # print(fun.get_time())
        time = fun.get_time()
        dpg.add_text(f"{time['hour']} часов {time['min']} минут {time['sec']} секунд")
        #dpg.add_time_picker(tag="time", default_value=, hour24=True)

        start_button = dpg.add_button(label="Начать", tag="start_button", callback=start_mailing)

with dpg.window(autosize=True, popup=True, show=False, tag="no_api_error", no_title_bar=True, no_open_over_existing_popup=False) as no_api_error:
    def ok_button_fun():
        dpg.delete_item("add_bots")
        dpg.configure_item(no_api_error, show=False)
        #open_bots_add_window()

    error_text = dpg.add_text("Ошибка: не введены API токены\n\nВведите API токены")
    dpg.add_separator()
    dpg.add_button(label="OK", pos=[95, 55], width=75, callback=ok_button_fun)

with dpg.window(autosize=True, modal=True, show=False, tag="group_access_error", no_title_bar=True):
    dpg.add_text("Ошибка: что-то пошло не так")
    #dpg.bind_item_font(error_text, font1)
    dpg.add_separator()
    dpg.add_button(label="OK", pos=[95,55], width=75, callback=lambda: dpg.configure_item("group_access_error", show=False))

with dpg.window(autosize=True, modal=True, show=False, tag="parsing_success", no_title_bar=True):
    success_text = dpg.add_text("Парсинг прошёл успешно\n\nДанные сохранены в файл users_id.txt")
    #dpg.bind_item_font(success_text, font1)
    dpg.add_separator()
    dpg.add_button(label="OK", pos=[145,70], width=75, callback=lambda: dpg.configure_item("parsing_success", show=False))


with dpg.window(tag="main") as main_window:
    #text_1 = dpg.add_text("Привет")
    open_parsing_button = dpg.add_button(label="Открыть систему парсинга", callback=open_parsing_system)
    open_bots_menu_button = dpg.add_button(label="Открыть меню ботов", callback=open_bots_menu_system)
    open_message_menu_button = dpg.add_button(label="Редактировать сообщение", callback=open_message_menu)
    open_mailing_button = dpg.add_button(label="Начать рассылку", callback=open_mailing_window)

    #dpg.add_button(label="test", callback= lambda: dpg.get_item_label("edit_token_1")) #print("Tokens: ", os.environ['TOKENS']))

    dpg.bind_font(font1)
    #dpg.bind_item_font(text_1, font1)
    #dpg.bind_item_font(open_parsing_button, font1)
    #dpg.bind_item_font(input_1, font1)



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        with open("message.txt", 'r', encoding='utf-8') as file:
            self.start_txt = file.read()

        self.title("Введите сообщение:")
        self.geometry("300x350")

        self.message_entry = tk.Text(width=35, height=20)   #textvariable=self.message)
        self.message_entry.pack(anchor="s")
        self.message_entry.insert(1.0, self.start_txt)
        self.message_entry.bind("<<Paste>>", self.handle_clipboard)

        self.message_button = tk.Button(text="Сохранить", width=20, command=self.save_message).pack(anchor="s", after=self.message_entry)

    def save_message(self):
        txt = self.message_entry.get(1.0, tk.END)

        with open("message.txt", 'w', encoding='utf-8') as file:
            file.write(txt)

        mb.showinfo("Сообщение сохранено", txt)
        print("Сообщение: {}".format(txt))
        self.destroy()

    def handle_clipboard(self, event):
        #self.delete(self.message_entry, 0, "end")
        line = self.clipboard_get()    #.split("\n")
        print("Вставлен текст из буфера обмена: ", line)
        self.message_entry.insert(1.0, line)
        return "break"




dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()

#while dpg.is_dearpygui_running():
    #print("this will run every frame")
    #dpg.render_dearpygui_frame()

dpg.destroy_context()