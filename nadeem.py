#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import uuid
import time
import random
import sqlite3
import threading
import subprocess
from queue import Queue

DB_PATH = "message_logs.db"
QUEUE = Queue()
SPAMMERS = {}

# === UTILITY FUNCTIONS ===
def fancy_print_line(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

def generate_stop_key():
    return uuid.uuid4().hex[:20].upper()

# === DB SETUP ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        convo_id TEXT,
                        token TEXT,
                        message TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    conn.commit()
    conn.close()

# === GSM Fallback ===
def send_sms_via_gsm(message):
    try:
        os.system(f"termux-sms-send -n +919999999999 '{message}'")
    except Exception as e:
        print("[!] GSM Fallback failed:", e)

# === MESSAGE SENDER ===
def spammer_thread(convo_id, token, message_lines, delay, stop_key):
    while SPAMMERS.get(stop_key, True):
        for msg in message_lines:
            if not SPAMMERS.get(stop_key, True):
                break
            try:
                os.system(f"curl -s -X POST https://graph.facebook.com/v19.0/{convo_id}/messages?access_token={token} -F 'message={{\"text\":\"{msg}\"}}' > /dev/null")
                log_message(convo_id, token, msg)
                time.sleep(delay)
            except Exception as e:
                print("[!] Error sending message:", e)
                send_sms_via_gsm(f"Failed: {msg}")

# === LOGGING ===
def log_message(convo_id, token, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (convo_id, token, message) VALUES (?, ?, ?)", (convo_id, token, message))
    conn.commit()
    conn.close()

# === MAIN FUNCTIONS ===
def start_loder():
    token_path = input("[?] Token File Path: ")
    convo_id = input("[?] Conversation ID: ")
    hater_name = input("[?] Hater Name: ")
    message_file = input("[?] Message File Path: ")
    delay = int(input("[?] Speed (seconds): "))

    with open(token_path) as tf:
        tokens = tf.read().splitlines()
    with open(message_file) as mf:
        message_lines = mf.read().splitlines()

    stop_key = generate_stop_key()
    SPAMMERS[stop_key] = True

    for token in tokens:
        t = threading.Thread(target=spammer_thread, args=(convo_id, token, message_lines, delay, stop_key))
        t.daemon = True
        t.start()

    print(f"\n[✓] STARTED | HATER: {hater_name} | STOP KEY: {stop_key}\n")

def stop_loder():
    stop_key = input("[?] Enter STOP KEY to terminate: ").strip().upper()
    if stop_key in SPAMMERS:
        SPAMMERS[stop_key] = False
        print("[✓] Stopped successfully.")
    else:
        print("[!] Invalid STOP KEY.")

def show_messages():
    convo_id = input("[?] Enter Conversation ID: ").strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, message FROM messages WHERE convo_id = ? ORDER BY timestamp DESC", (convo_id,))
    results = cursor.fetchall()
    if results:
        for ts, msg in results:
            print(f"[{ts}] {msg}")
    else:
        print("[!] No messages found.")
    conn.close()

# === UI MENU ===
def menu():
    os.system("clear")
    fancy_print_line("\033[1;33m== BROKEN NADEEM OFFLINE SPAMMER ==\033[0m")
    print("\n[1] START LODER")
    print("[2] STOP LODER")
    print("[3] SHOW MESSAGE")
    print("[0] EXIT")

    choice = input("\n[?] Select Option: ")
    if choice == "1":
        start_loder()
    elif choice == "2":
        stop_loder()
    elif choice == "3":
        show_messages()
    elif choice == "0":
        print("[✓] Exiting...")
        sys.exit()
    else:
        print("[!] Invalid Choice.")

# === DAEMON MAIN LOOP ===
if __name__ == '__main__':
    init_db()
    while True:
        try:
            menu()
            input("\n[Press Enter to continue]")
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user.")
            sys.exit()
