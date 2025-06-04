import os
import time
import threading
import random
import string
import json
import requests
import sys

STOP_KEYS_FILE = 'stop_keys.json'
MESSAGE_LOG_FILE = 'message_logs.json'
active_threads = {}

# ✨ Typing animation
def animate(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# 🔥 BROKEN NADEEM Logo
def show_logo():
    os.system('clear' if os.name != 'nt' else 'cls')
    logo = r"""
███╗   ██╗ █████╗ ██████╗ ███████╗███████╗███╗  ██╗
████╗  ██║██╔══██╗██╔══██╗██╔════╝██╔════╝████╗ ██║
██╔██╗ ██║███████║██████╔╝█████╗  █████╗  ██╔██╗██║
██║╚██╗██║██╔══██║██╔═══╝ ██╔══╝  ██╔══╝  ██║╚████║
██║ ╚████║██║  ██║██║     ███████╗███████╗██║ ╚███║
╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚══╝
           ⚔️ TOOL BY BROKEN NADEEM ⚔️
"""
    print(logo)
    time.sleep(1)

def load_tokens(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_messages(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def generate_stop_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

def save_stop_key(convo_id, stop_key, thread_id):
    try:
        data = json.load(open(STOP_KEYS_FILE))
    except:
        data = {}
    data[stop_key] = {'convo_id': convo_id, 'thread_id': thread_id}
    json.dump(data, open(STOP_KEYS_FILE, 'w'))

def log_message(convo_id, message):
    try:
        data = json.load(open(MESSAGE_LOG_FILE))
    except:
        data = {}
    if convo_id not in data:
        data[convo_id] = []
    data[convo_id].append(message)
    json.dump(data, open(MESSAGE_LOG_FILE, 'w'))

def send_real_message(token, convo_id, message):
    url = f"https://graph.facebook.com/v19.0/{convo_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_type": "MESSAGE_TAG",
        "tag": "POST_PURCHASE_UPDATE",
        "message": {"text": message}
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            animate(f"✅ SENT: {message}", 0.01)
            return True
        else:
            animate(f"❌ FAIL {response.status_code}: {response.text}", 0.01)
            return False
    except Exception as e:
        animate(f"⚠️ ERROR: {e}", 0.01)
        return False

def spammer(token_list, convo_id, messages, speed, hater_name, stop_key):
    while True:
        try:
            with open(STOP_KEYS_FILE) as f:
                stop_data = json.load(f)
            if stop_key not in stop_data:
                animate(f"🛑 STOP KEY {stop_key} REMOVED — TERMINATING SPAM", 0.02)
                break
        except:
            break

        for token in token_list:
            for msg in messages:
                if not os.path.exists(STOP_KEYS_FILE):
                    animate(f"🛑 STOP KEY FILE DELETED — STOPPING", 0.02)
                    return
                with open(STOP_KEYS_FILE) as f:
                    stop_data = json.load(f)
                    if stop_key not in stop_data:
                        animate(f"🛑 STOP KEY {stop_key} REMOVED DURING LOOP", 0.02)
                        return
                success = send_real_message(token, convo_id, msg)
                if success:
                    log_message(convo_id, f"{hater_name}: {msg}")
                time.sleep(speed)

def start_loder():
    animate("\n🔓 STARTING LODER...", 0.04)
    token_file = input("📁 Token file path: ")
    hater_name = input("😈 Hater name: ")
    convo_id = input("💬 Conversation ID: ")
    message_file = input("📝 Message file path: ")
    speed = float(input("⏱️ Delay (seconds): "))

    tokens = load_tokens(token_file)
    messages = load_messages(message_file)
    stop_key = generate_stop_key()

    thread = threading.Thread(target=spammer, args=(tokens, convo_id, messages, speed, hater_name, stop_key))
    thread.daemon = True
    thread.start()
    active_threads[stop_key] = thread
    save_stop_key(convo_id, stop_key, thread.ident)

    animate("\n🚀 SPAM STARTED SUCCESSFULLY!", 0.03)
    animate(f"🔑 YOUR STOP KEY: {stop_key}\n", 0.04)

def stop_loder():
    animate("\n🛑 STOP LODER", 0.04)
    stop_key = input("🔑 Enter STOP KEY: ")
    try:
        with open(STOP_KEYS_FILE) as f:
            stop_keys = json.load(f)
        if stop_key in stop_keys:
            del stop_keys[stop_key]
            json.dump(stop_keys, open(STOP_KEYS_FILE, 'w'))
            animate("✅ SPAM STOPPED FOR THAT KEY.", 0.04)
        else:
            animate("❌ STOP KEY NOT FOUND.", 0.04)
    except:
        animate("❌ NO ACTIVE STOP KEYS FOUND.", 0.04)

def show_messages():
    animate("\n📂 MESSAGE LOG VIEWER", 0.04)
    convo_id = input("💬 Enter conversation ID: ")
    try:
        with open(MESSAGE_LOG_FILE) as f:
            logs = json.load(f)
        if convo_id in logs:
            animate(f"\n📨 Messages sent to {convo_id}:\n", 0.02)
            for msg in logs[convo_id]:
                animate(f"➤ {msg}", 0.01)
        else:
            animate("❌ NO MESSAGES FOUND FOR THIS CONVO.", 0.04)
    except:
        animate("❌ MESSAGE LOG FILE NOT FOUND.", 0.04)

def main():
    while True:
        show_logo()
        animate("ALL OPTIONS ANIMATED ✅", 0.02)
        animate("1. START LODER", 0.02)
        animate("2. STOP LODER", 0.02)
        animate("3. SHOW MESSAGE", 0.02)
        choice = input("📲 Enter choice (1/2/3): ")

        if choice == '1':
            start_loder()
        elif choice == '2':
            stop_loder()
        elif choice == '3':
            show_messages()
        else:
            animate("❌ INVALID CHOICE.", 0.02)

        input("\n🔁 Press Enter to continue...")

if __name__ == "__main__":
    main()
