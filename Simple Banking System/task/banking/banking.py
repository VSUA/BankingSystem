import random
import sqlite3

class BankingSystem:
    BIN = "400000"
    def __init__(self, currsor1, connection1):
        self.cursor = currsor1
        self.connection = connection1
        self.cursor.execute("SELECT count(*) FROM card;")
        self.id = int(self.cursor.fetchone()[0])

    def create_account(self):
        account_identifier = f"{random.randint(0, 999999999):09}"
        card_number = self.BIN + account_identifier
        card_number += str(self.luhn_algoritm(card_number))
        card_pin = f"{random.randint(0, 9999):04}"
        #print(card_pin)
        self.cursor.execute(f"SELECT count(number) FROM card WHERE number = {card_number};")
        if int(self.cursor.fetchone()[0]) == 0:  # card_number not in self.data_base:
            # self.data_base[card_number] = dict({"pin": card_pin, "balance": 0})
            self.cursor.execute(f"INSERT INTO card (id, number, pin) VALUES ({self.id}, '{card_number}', '{card_pin}')")
            self.connection.commit()
            print("Your card has been created")
            print("Your card number:")
            print(card_number)
            print("Your card PIN:")
            print(card_pin)
            self.id += 1

    def log_in(self):
        print("Enter your card number:")
        card_number = input()
        print("Enter your PIN:")
        card_pin = input()
        self.cursor.execute(f"SELECT count(number) FROM card WHERE number = '{card_number}' AND pin = '{card_pin}';")
        if int(self.cursor.fetchone()[0]) == 1:
            # card_number in self.data_base and self.data_base[card_number]["pin"] == card_pin:
            print("You have successfully logged in!")
            while True:
                print("1. Balance")
                print("2. Add income")
                print("3. Do transfer")
                print("4. Close account")
                print("5. Log out")
                print("0. Exit")

                choose = int(input())

                if choose == 1:
                    # print(f"Balance: {self.data_base[card_number]['balance']}")
                    self.cursor.execute(f"SELECT balance FROM card WHERE number = '{card_number}';")
                    print(self.cursor.fetchone()[0])
                elif choose == 2:
                    self.add_income(card_number)
                elif choose == 3:
                    self.transfer(card_number)
                elif choose == 4:
                    self.close_account(card_number)
                elif choose == 5:
                    print("You have successfully logged out!")
                    break
                elif choose == 0:
                    return True
        else:
            print("Wrong card number or PIN!")

    def main_menu(self):
        while True:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")

            number = input().strip()

            if number == "1":
                self.create_account()
            elif number == "2":
                if self.log_in():
                    break
            elif number == "0":
                print("Bye!")
                break

    def luhn_algoritm(self, account_identifier):
        sum_of_numbers = 0

        for i in range(len(account_identifier)):
            if i % 2 == 0:
                sum_of_numbers += (int(account_identifier[i]) * 2) - 9 if int(account_identifier[i]) * 2 > 9 else int(
                    account_identifier[i]) * 2
            else:
                sum_of_numbers += int(account_identifier[i])

        return 10 - (sum_of_numbers % 10) if sum_of_numbers % 10 != 0 else 0

    def add_income(self, card_number):
        print("Enter income:")
        income = int(input())
        self.cursor.execute(f"UPDATE card SET balance = balance + {income} WHERE number = '{card_number}';")
        self.connection.commit()
        print("Income was added!")

    def transfer(self, card_number):
        print("Transfer")
        print("Enter card number:")
        recipient_card = input()
        if str(self.luhn_algoritm(recipient_card[0:15])) != recipient_card[15]:
            print("Probably you made mistake in the card number. Please try again!")
            return

        self.cursor.execute(f"SELECT count(number) FROM card WHERE number = '{recipient_card}';")
        if int(self.cursor.fetchone()[0]) == 0:
            print("Such a card does not exist.")
            return
        else:
            print("Enter how much money you want to transfer:")
            money_to_transfer = int(input())
            self.cursor.execute(f"SELECT balance FROM card WHERE number = '{card_number}';")
            if int(self.cursor.fetchone()[0]) >= money_to_transfer:
                self.cursor.execute(f"UPDATE card SET balance = balance - {money_to_transfer} WHERE number = '{card_number}';")
                self.cursor.execute(f"UPDATE card SET balance = balance + {money_to_transfer} WHERE number = '{recipient_card}';")
                self.connection.commit()
            else:
                print("Not enough money!")
                return

    def close_account(self, card_number):
        self.cursor.execute(f"DELETE FROM card WHERE number = '{card_number}';")
        self.connection.commit()
        print("The account has been closed!")

conn = sqlite3.connect('card.s3db')
curr = conn.cursor()
curr.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='card';")
if int(curr.fetchone()[0]) == 0:
    curr.execute("CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
conn.commit()

system = BankingSystem(curr, conn)
system.main_menu()


