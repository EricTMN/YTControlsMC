# Modified from DougDoug's TwitchPlays template to support Minecraft control via YouTube chat
# No need to change the imports unless you plan to add something
import concurrent.futures
import time
import TwitchPlays_Connection
import mcrcon
from threading import Lock
import re
import json
import os
import sys



# Use sys.executable to get the path of the EXE when compiled, fallback to script path for dev
def get_resource_path(filename):
    if getattr(sys, 'frozen', False):
        # Running as a compiled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as a regular .py script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

def load_json(filename):
    full_path = get_resource_path(filename)
    with open(full_path, "r") as f:
        return json.load(f)

cfg = load_json("config.json")
COMMANDS = load_json("commands.json")
blacklists = load_json("blacklists.json")

# Basic settings
YOUTUBE_CHANNEL_ID = cfg["YOUTUBE_CHANNEL_ID"]
YOUTUBE_STREAM_URL = cfg["YOUTUBE_STREAM_URL"]
RCON_HOST = cfg["RCON_HOST"]
RCON_PORT = cfg["RCON_PORT"]
RCON_PASSWORD = cfg["RCON_PASSWORD"]
PLAYER_USERNAME = cfg["PLAYER_USERNAME"]
MESSAGE_RATE = cfg.get("MESSAGE_RATE", 0.5)
MAX_QUEUE_LENGTH = cfg.get("MAX_QUEUE_LENGTH", 5)
MAX_WORKERS = cfg.get("MAX_WORKERS", 15)

# Limits
MAX_ITEMS = cfg.get("MAX_ITEMS", 1)
MAX_EFFECT_DURATION = cfg.get("MAX_EFFECT_DURATION", 30)
MAX_EFFECT_AMPLIFIER = cfg.get("MAX_EFFECT_AMPLIFIER", 3)
MAX_MOBS = cfg.get("MAX_MOBS", 1)

# ========== CHAT MESSAGE FORMATS ==========
CHAT_FORMATS = {
    "summon": "[{}] summoned {} at {}!",
    "give": "[{}] gave {} to {}!",
    "effect": "[{}] gave {} to {}!"
}

# Blacklists
BLACKLIST_MOBS = set(map(str.lower, blacklists.get("MOBS", [])))
BLACKLIST_ITEMS = set(map(str.lower, blacklists.get("ITEMS", [])))
BLACKLIST_EFFECTS = set(map(str.lower, blacklists.get("EFFECTS", [])))

# Past here, you shouldn't need to change anything !!

# ========== GLOBAL STATE ==========
last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
rcon_lock = Lock()

# ========== INITIATE CONNECTIONS ==========
t = TwitchPlays_Connection.YouTube()
t.youtube_connect(YOUTUBE_CHANNEL_ID, YOUTUBE_STREAM_URL)

rcon_client = mcrcon.MCRcon(RCON_HOST, RCON_PASSWORD)
rcon_client.connect()

# ========== SAFE RCON EXECUTOR ==========
def safe_rcon_command(cmd):
    global rcon_client
    with rcon_lock:
        try:
            return rcon_client.command(cmd)
        except Exception as e:
            print(f"RCON command failed: {e}. Reconnecting...")
            try:
                rcon_client.disconnect()
            except:
                pass
            try:
                rcon_client = mcrcon.MCRcon(RCON_HOST, RCON_PASSWORD)
                rcon_client.connect()
                return rcon_client.command(cmd)
            except Exception as err:
                print(f"RCON reconnect failed: {err}")

# ========== HELPER FUNCTION ==========
def normalize_name(raw):
    return raw.lower().strip().replace(" ", "_")

#def tellraw_message(viewer, action, target, detail):
 #   if action in CHAT_FORMATS:
  #      text = CHAT_FORMATS[action].format(viewer, detail, target)
   # else:
    #    text = f"[{viewer}] {action} {target} with {detail}!"
    #cmd = f'tellraw @a {{"text":"{text}","color":"gold"}}'
    # safe_rcon_command(cmd)

# ========== MESSAGE HANDLER ==========
def handle_message(message):
    try:
        msg = message['message'].lower().strip()
        user = message['username']
        print(f"{user}: {msg}")

        if msg in COMMANDS:
            command = COMMANDS[msg].replace("{PLAYER}", PLAYER_USERNAME)
            print(f"(predefined) Executing: {command}")
            safe_rcon_command(command)
            return

        summon_match = re.match(r'^(summon|spawn)\s+(.+?)(?:\s+(\d+))?$', msg)
        if summon_match:
            mob = normalize_name(summon_match.group(2))
            count = int(summon_match.group(3)) if summon_match.group(3) else 1
            if mob in BLACKLIST_MOBS:
                print(f"Blocked mob: {mob}")
                return
            count = min(count, MAX_MOBS)
            for _ in range(count):
                cmd = f"execute at {PLAYER_USERNAME} run summon minecraft:{mob}"
                print(f"Executing: {cmd}")
                safe_rcon_command(cmd)
           # tellraw_message(user, "summon", PLAYER_USERNAME, mob)
            return

        give_match = re.match(r'^give\s+(.+?)(?:\s+(\d+))?$', msg)
        if give_match:
            item = normalize_name(give_match.group(1))
            amount = int(give_match.group(2)) if give_match.group(2) else 1
            if item in BLACKLIST_ITEMS:
                print(f"Blocked item: {item}")
                return
            amount = min(amount, MAX_ITEMS)
            cmd = f"give {PLAYER_USERNAME} minecraft:{item} {amount}"
            print(f"Executing: {cmd}")
            safe_rcon_command(cmd)
          #  tellraw_message(user, "give", PLAYER_USERNAME, f"{amount} {item}")
            return

        effect_match = re.match(r'^effect\s+(.+?)(?:\s+(\d+))?(?:\s+(\d+))?$', msg)
        if effect_match:
            effect = normalize_name(effect_match.group(1))
            duration = int(effect_match.group(2)) if effect_match.group(2) else MAX_EFFECT_DURATION
            amplifier = int(effect_match.group(3)) if effect_match.group(3) else 1
            if effect in BLACKLIST_EFFECTS:
                print(f"Blocked effect: {effect}")
                return
            duration = min(duration, MAX_EFFECT_DURATION)
            amplifier = min(amplifier, MAX_EFFECT_AMPLIFIER)
            cmd = f"effect give {PLAYER_USERNAME} minecraft:{effect} {duration} {amplifier}"
            print(f"Executing: {cmd}")
            safe_rcon_command(cmd)
           # tellraw_message(user, "effect", PLAYER_USERNAME, f"{effect} ({duration}s, amp {amplifier})")
            return

        print("Command not recognized.")
    except Exception as e:
        print(f"Error handling message: {e}")

# ========== MAIN LOOP ==========
try:
    while True:
        active_tasks = [t for t in active_tasks if not t.done()]

        new_messages = t.twitch_receive_messages()
        if new_messages:
            message_queue += new_messages
            message_queue = message_queue[-MAX_QUEUE_LENGTH:]

        messages_to_handle = []
        if message_queue:
            r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
            n = int(r * len(message_queue))
            if n > 0:
                messages_to_handle = message_queue[0:n]
                del message_queue[0:n]
                last_time = time.time()

        for msg in messages_to_handle:
            if len(active_tasks) < MAX_WORKERS:
                active_tasks.append(thread_pool.submit(handle_message, msg))
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    print("Disconnecting RCON...")
    rcon_client.disconnect()
