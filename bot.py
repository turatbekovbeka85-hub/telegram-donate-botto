from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ---------- АЛМАЗЫ ----------
PRICES = {
    1: ("105💎 или 180💎 бонусом", 85),
    2: ("210💎 или 285💎 бонусом", 170),
    3: ("326💎 или 559💎 бонусом", 250),
    4: ("431💎 или 664💎 бонусом", 335),
    5: ("546💎 или 936💎 бонусом", 430),
    6: ("651💎 или 1041💎 бонусом", 515),
    7: ("756💎 или 1146💎 бонусом", 600),
    8: ("872💎 или 1262💎 бонусом", 680),
    9: ("1113💎 или 1908💎 бонусом", 820),
    10: ("1439💎 или 2234💎 бонусом", 1070),
    11: ("1659💎 или 2454💎 бонусом", 1250),
    12: ("1985💎 или 2780💎 бонусом", 1500),
    13: ("2398💎 или 4033💎 бонусом", 1650),
    14: ("2724💎 или 4359💎 бонусом", 1900),
    15: ("2944💎 или 4579💎 бонусом", 2080),
    16: ("3511💎 или 5146💎 бонусом", 2470),
    17: ("4796💎 или 6431💎 бонусом", 3300),
    18: ("6160💎 или 10360💎 бонусом", 4300),
    19: ("8558💎 или 12758💎 бонусом", 5950),
    20: ("12320💎 или 16520💎 бонусом", 8600),
}

# ---------- ВАУЧЕРЫ ----------
VOUCHERS = {
    1: ("🎫 Ваучер 1 неделя — 450💎", 150),
    2: ("🎫 Ваучер 2 недели — 900💎", 300),
    3: ("🎫 Ваучер 3 недели — 1350💎", 450),
    4: ("🎫 Ваучер 1 месяц — 2600💎", 750),
}

ORDERS = {}

# ---------- УДАЛЕНИЕ ----------
async def cleanup_messages(context, uid):
    order = ORDERS.get(uid)
    if not order:
        return
    for mid in order.get("messages", []):
        try:
            await context.bot.delete_message(uid, mid)
        except:
            pass

# ---------- МЕНЮ ----------
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Купить алмазы", callback_data="buy")],
        [InlineKeyboardButton("🎫 Ваучеры", callback_data="voucher")],
        [InlineKeyboardButton("🆘 Поддержка", callback_data="support")],
        [InlineKeyboardButton("ℹ️ Информация", callback_data="info")]
    ])

def back_btn():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
    ])

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id

    if uid in ORDERS:
        await cleanup_messages(context, uid)
        ORDERS.pop(uid, None)

    msg = await update.message.reply_text(
        "💎 Донат Free Fire\nВыберите действие:",
        reply_markup=main_menu()
    )

    ORDERS[uid] = {"messages": [msg.message_id]}

# ---------- CALLBACK ----------
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    ORDERS.setdefault(uid, {"messages": []})
    ORDERS[uid]["messages"].append(q.message.message_id)

    # ---- АЛМАЗЫ ----
    if q.data == "buy":
        kb = [
            [InlineKeyboardButton(f"{v[0]} — {v[1]} сом", callback_data=f"item_{k}")]
            for k, v in PRICES.items()
        ]
        kb.append([InlineKeyboardButton("⬅️ Назад", callback_data="back")])
        await q.message.edit_text("💎 Выберите пакет:", reply_markup=InlineKeyboardMarkup(kb))

    # ---- ВАУЧЕРЫ ----
    elif q.data == "voucher":
        kb = [
            [InlineKeyboardButton(f"{v[0]} — {v[1]} сом", callback_data=f"voucher_{k}")]
            for k, v in VOUCHERS.items()
        ]
        kb.append([InlineKeyboardButton("⬅️ Назад", callback_data="back")])
        await q.message.edit_text("🎫 Выберите ваучер:", reply_markup=InlineKeyboardMarkup(kb))

    # ---- ВЫБОР АЛМАЗОВ ----
    elif q.data.startswith("item_"):
        item = int(q.data.split("_")[1])
        ORDERS[uid].update({"type": "diamonds", "item": item, "step": "wait_photo"})
        name, price = PRICES[item]

        await q.message.edit_text(
            f"💳 Оплата\n\n"
            f"О!Деньги: 0508077494\n"
            f"Получатель: Беглан К\n\n"
            f"💎 {name}\n"
            f"💰 {price} сом\n\n"
            f"📸 Отправьте ФОТО чека (без текста)",
            reply_markup=back_btn()
        )

    # ---- ВЫБОР ВАУЧЕРА ----
    elif q.data.startswith("voucher_"):
        item = int(q.data.split("_")[1])
        ORDERS[uid].update({"type": "voucher", "item": item, "step": "wait_photo"})
        name, price = VOUCHERS[item]

        await q.message.edit_text(
            f"💳 Оплата\n\n"
            f"О!Деньги: 0508077494\n"
            f"Получатель: Беглан К\n\n"
            f"{name}\n"
            f"💰 {price} сом\n\n"
            f"📸 Отправьте ФОТО чека (без текста)",
            reply_markup=back_btn()
        )

    elif q.data == "support":
        await q.message.edit_text("🆘 Поддержка\n\n@budget_shop1", reply_markup=back_btn())

    elif q.data == "info":
        await q.message.edit_text(
            "ℹ️ Информация\n\n"
            "• Оплата по чеку\n"
            "• Проверка администратором\n"
            "• Время: 5–30 минут",
            reply_markup=back_btn()
        )

    elif q.data == "back":
        await q.message.edit_text("Главное меню:", reply_markup=main_menu())

    elif q.data.startswith("check_ok_"):
        target = int(q.data.split("_")[2])
        ORDERS[target]["step"] = "wait_id"
        await context.bot.send_message(target, "✅ Оплата принята\n✏️ Отправьте игровой ID")

    elif q.data.startswith("check_no_"):
        target = int(q.data.split("_")[2])
        await cleanup_messages(context, target)
        ORDERS.pop(target, None)
        await context.bot.send_message(target, "❌ Платёж отклонён")

    elif q.data.startswith("id_ok_"):
        target = int(q.data.split("_")[2])
        await cleanup_messages(context, target)
        ORDERS.pop(target, None)
        await context.bot.send_message(target, "💎 Услуга успешно выполнена ✅")

    elif q.data.startswith("id_no_"):
        target = int(q.data.split("_")[2])
        await cleanup_messages(context, target)
        ORDERS.pop(target, None)
        await context.bot.send_message(target, "🚫 Неправильный ID, платёж отклонён")

# ---------- ФОТО ----------
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    if uid not in ORDERS or ORDERS[uid].get("step") != "wait_photo":
        return

    ORDERS[uid]["step"] = "wait_admin"
    ORDERS[uid]["messages"].append(update.message.message_id)

    order = ORDERS[uid]
    user = update.message.from_user

    if order["type"] == "diamonds":
        name, price = PRICES[order["item"]]
        title = "💎 АЛМАЗЫ"
    else:
        name, price = VOUCHERS[order["item"]]
        title = "🎫 ВАУЧЕР"

    caption = (
        f"🧾 ЧЕК ОПЛАТЫ ({title})\n\n"
        f"👤 @{user.username or 'без_username'}\n"
        f"🆔 {user.id}\n\n"
        f"{name}\n"
        f"💰 {price} сом"
    )

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Подтвердить", callback_data=f"check_ok_{uid}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"check_no_{uid}")
        ]
    ])

    await context.bot.send_photo(
        ADMIN_ID,
        update.message.photo[-1].file_id,
        caption=caption,
        reply_markup=kb
    )

    msg = await update.message.reply_text("⏳ Чек отправлен администратору")
    ORDERS[uid]["messages"].append(msg.message_id)

# ---------- ID ----------
async def id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    if uid not in ORDERS or ORDERS[uid].get("step") != "wait_id":
        return

    ORDERS[uid]["messages"].append(update.message.message_id)
    order = ORDERS[uid]
    user = update.message.from_user

    if order["type"] == "diamonds":
        name, price = PRICES[order["item"]]
    else:
        name, price = VOUCHERS[order["item"]]

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Выполнено", callback_data=f"id_ok_{uid}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"id_no_{uid}")
        ]
    ])

    await context.bot.send_message(
        ADMIN_ID,
        f"🎮 ID от @{user.username or 'без_username'}\n\n"
        f"🆔 {update.message.text}\n\n"
        f"{name}\n"
        f"💰 {price} сом",
        reply_markup=kb
    )

    msg = await update.message.reply_text("⏳ ID отправлен администратору")
    ORDERS[uid]["messages"].append(msg.message_id)

# ---------- RUN ----------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, id_handler))

    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":

    main()
