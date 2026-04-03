import telebot
import random
import time
from config import BOARD, START_MONEY, CIRCLE_BONUS, TAX_AMOUNT

# === ВПИШИ СВОЙ ТОКЕН НИЖЕ ===
TOKEN = '8483249261:AAF2GFIHmJ2uBXvXgeYR_nDf1JJ-SuE_7LI'
# =============================

bot = telebot.TeleBot(TOKEN)
games = {}

def get_rent(price):
    return int(price * 0.5)

def next_turn(chat_id):
    game = games[chat_id]
    game['turn_index'] = (game['turn_index'] + 1) % len(game['players'])
    game['awaiting_action'] = False
    p = game['players'][game['turn_index']]
    bot.send_message(chat_id, f"🎲 Ход {p['name']}. Баланс: {p['money']}$. Жми /roll!")

@bot.message_handler(commands=['monopoly'])
def start_monopoly(message):
    if message.chat.type == 'private':
        return bot.send_message(message.chat.id, "Игра только для групп!")
    games[message.chat.id] = {'title': message.chat.title, 'status': 'lobby', 'players': [], 'turn_index': 0, 'properties': {}, 'awaiting_action': False}
    bot.send_message(message.chat.id, "🎩 Набор открыт! Жми /join. После всех — /start_game.")

@bot.message_handler(commands=['join'])
def join_game(message):
    chat_id = message.chat.id
    if chat_id not in games or games[chat_id]['status'] != 'lobby': return
    if any(p['id'] == message.from_user.id for p in games[chat_id]['players']): return
    games[chat_id]['players'].append({'id': message.from_user.id, 'name': message.from_user.first_name, 'money': START_MONEY, 'position': 0})
    bot.send_message(chat_id, f"✅ {message.from_user.first_name} в деле!")

@bot.message_handler(commands=['start_game'])
def begin_game(message):
    cid = message.chat.id
    if cid in games and len(games[cid]['players']) >= 2:
        games[cid]['status'] = 'playing'
        bot.send_message(cid, f"🏁 Погнали! Первым ходит {games[cid]['players'][0]['name']}. /roll!")

@bot.message_handler(commands=['roll'])
def roll_dice(message):
    cid = message.chat.id
    if cid not in games or games[cid]['status'] != 'playing': return
    game = games[cid]
    p = game['players'][game['turn_index']]
    
    if message.from_user.id != p['id'] or game['awaiting_action']: return

    dice = random.randint(1, 6)
    old_pos = p['position']
    p['position'] = (old_pos + dice) % len(BOARD)
    
    msg = f"🎲 Выпало: {dice}. "
    if p['position'] < old_pos:
        p['money'] += CIRCLE_BONUS
        msg += f"💰 Круг пройден! +{CIRCLE_BONUS}$. "
    
    field = BOARD[p['position']]
    msg += f"\n📍 Поле: **{field['name']}**"
    bot.send_message(cid, msg, parse_mode="Markdown")

    if field['type'] == 'property':
        owner_id = game['properties'].get(p['position'])
        if owner_id is None:
            game['awaiting_action'] = True
            bot.send_message(cid, f"Купишь за {field['price']}$? /buy или /no_buy")
            return
        elif owner_id != p['id']:
            rent = get_rent(field['price'])
            p['money'] -= rent
            for owner in game['players']:
                if owner['id'] == owner_id: owner['money'] += rent
            bot.send_message(cid, f"💸 Платишь аренду {rent}$ владельцу!")
    
    elif field['type'] == 'tax':
        p['money'] -= TAX_AMOUNT
        bot.send_message(cid, f"📉 Налог {TAX_AMOUNT}$ уплачен!")
    elif field['type'] == 'go_to_jail':
        p['position'] = 6
        bot.send_message(cid, "🚓 В ТЮРЬМУ!")
    
    next_turn(cid)

@bot.message_handler(commands=['buy', 'no_buy'])
def handle_buy(message):
    cid = message.chat.id
    if cid not in games or not games[cid]['awaiting_action']: return
    game = games[cid]
    p = game['players'][game['turn_index']]
    if message.from_user.id != p['id']: return

    if message.text.startswith('/buy'):
        price = BOARD[p['position']]['price']
        if p['money'] >= price:
            p['money'] -= price
            game['properties'][p['position']] = p['id']
            bot.send_message(cid, "🏠 Куплено!")
        else: bot.send_message(cid, "❌ Нет денег!")
    
    next_turn(cid)

@bot.message_handler(commands=['status'])
def game_status(message):
    if message.chat.id not in games: return
    res = "📊 Баланс:\n" + "\n".join([f"{p['name']}: {p['money']}$" for p in games[message.chat.id]['players']])
    bot.send_message(message.chat.id, res)

@bot.message_handler(commands=['balance'])
def check_personal_balance(message):
    if message.chat.type != 'private': return
    res = "💰 Твой баланс:\n"
    found = False
    for gid, g in games.items():
        for p in g['players']:
            if p['id'] == message.from_user.id:
                res += f"- {g['title']}: {p['money']}$\n"
                found = True
    bot.send_message(message.chat.id, res if found else "Ты не в игре!")

if __name__ == "__main__":
    bot.infinity_polling()
