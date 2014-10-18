#!/usr/bin/env python
# coding=utf-8

from gi.repository import Gtk, GObject
import sqlite3

# Connecting to DATABASE
connection = sqlite3.connect('db/dict.db')
sql = connection.cursor()


def eng2bn(word):
    # FETCHING INDEX
    sql.execute('SELECT * FROM english WHERE word=?', (word.upper(),))
    try:
        bn_index = sql.fetchone()[0]
        # FETCHING MEANING
        sql.execute('SELECT * FROM bengali WHERE serial=?', (bn_index,))
        meaning = sql.fetchone()[1]
        return meaning
    except TypeError:
        return "শব্দটি পাওয়া যায়নি!"


class DictGui:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui.glade")
        self.window = builder.get_object("main_window")
        self.search_en = builder.get_object("search_en")
        self.result_view = builder.get_object("result_lab")
        self.mnu_about = builder.get_object("mnu_about")
        self.about_dialog = builder.get_object("aboutdialog")
        builder.connect_signals(self)

    def show_about(self, about):
        abt = self.about_dialog.run()
        self.about_dialog.hide()

    def on_search_activate(self, search_en):
        # Main Event Handler

        word = self.search_en.get_text()
        if word == '':
            self.result_view.set_text('')
            return
        result = eng2bn(word)
        if result != None:
            self.result_view.set_text(result)

    def mnu_quite_app(self, window):
        Gtk.main_quit()

if __name__ == '__main__':
    dict = DictGui()
    dict.window.connect("delete-event", Gtk.main_quit)
    dict.window.show_all()
    Gtk.main()
