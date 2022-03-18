import time
from datetime import datetime
import os
import sqlite3
from sqlite3 import Error


class ReadLines:
    def __init__(self):
        self.gainedResidue = 0
        self.logFile = None
        self.time_gap_sec = None
        self.amount = None
        self.time_gap = None
        self.hour = None
        self.day = None
        self.conn = None
        self.running = None
        self.tz = 1
        self.item_time = self.item = self.value = ''
        self.click_value = 0
        self.click_cost = 0.34  # importar o custo do click da BP
        self.clicks = 0
        self.notable_loots = []
        self.run_value = 0.0
        self.previous_time = datetime.now()
        self.runClicks = 0

    def file_reader(self, logfile):
        logfile.seek(0, os.SEEK_END)
        i = 0
        while self.running:
            # read last line of file
            self.line = logfile.readline()
            # sleep if file hasn't been updated
            if not self.line:
                time.sleep(0.1)
                continue
            yield self.line
        print('this is no longer reading')

    def get_variables(self, line):
        # time
        split_1 = line.split(' [System] [] You received ')
        self.item_time = split_1[0]
        # name
        split_2 = split_1[1].split(' x (')
        self.item = split_2[0]
        # value
        split_3 = split_2[1].split(') Value: ')
        self.amount = split_3[0]
        split_3 = split_3[1].split(' ')
        self.value = float(split_3[0])

    def startRead(self, idRun, isLimited, clicksWin, metalWin):
        try:
            self.conn = sqlite3.connect(r"db_CM.db")
        except Error as e:
            print('Erro BD')
            print(e)
            return

        path = 'C:\\Users\$USERNAME\Documents\Entropia Universe\chat.log'

        filepath = os.path.expandvars(path)
        self.logFile = open(filepath, "r", encoding="Latin-1")
        logLines = self.file_reader(self.logFile)

        self.tz = 1
        self.item_time = self.item = self.value = ''
        self.click_value = 0.0
        self.click_cost = 0.34
        self.notable_loots = []
        self.run_value = 0.0
        self.clicks = 0
        self.gainedResidue = 0.0
        self.previous_time = datetime.strptime('2022-02-19 18:05:48', '%Y-%m-%d %H:%M:%S')

        for line in logLines:
            print(self.line)
            if '[] You received' in line:
                self.get_variables(line)
                if 'Metal Residue' in self.item or "Energy Matter Residue" in self.item:
                    self.gainedResidue += self.value
                self.item_time = datetime.strptime(self.item_time, '%Y-%m-%d %H:%M:%S')
                self.day = self.item_time.strftime("%d/%m/%Y")
                self.hour = self.item_time.strftime("%H:%M:%S")
                self.time_gap = self.item_time - self.previous_time
                self.time_gap_sec = self.time_gap.total_seconds()

                if self.time_gap_sec > 2:
                    self.run_value += self.click_value
                    self.click_value = 0
                    self.clicks += 1
                self.click_value += self.value
                self.run_value += self.value
                self.previous_time = self.item_time
                sql = f'INSERT INTO RunReturn (Data, Hora, Material, Amount, Value, idRun, nClick) ' \
                      f'VALUES (\'{self.day}\', \'{self.hour}\', \'{self.item}\', {self.amount}, {self.value}, {idRun}, {self.clicks} );'
                cur = self.conn.cursor()
                cur.execute(sql)

                sql = f'UPDATE Runs SET Clicks = {self.runClicks} WHERE id = {idRun};'
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
