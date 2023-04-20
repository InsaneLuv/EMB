import logging
import traceback

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import admins
from database import search_profile
from database.events.events import get_rabbit_event_member_count
from loader import dp, _
from tools.destroyed_monuments.dmonuments import get_destroyed_monuments

from database.events import get_rabbit_top

tools_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        # InlineKeyboardButton(text='🗂 Спарсить газеты', callback_data='Спарсить'),
                                        # InlineKeyboardButton(text='📍 Создать ивент', callback_data='Создать1'),
                                        # InlineKeyboardButton(text='💥 Сломанные монументы', callback_data='dmonuments')
                                        InlineKeyboardButton(text=_('🐰🩸 GENOCIDE TOP 🐰🩸'), callback_data='rabbit_top')
                                    ],
                                    # [
                                    #     InlineKeyboardButton(text='🚨 Troublelogs', callback_data='tlogs'),
                                    #     InlineKeyboardButton(text='🛎 Помощь', callback_data='Помощь')
                                    # ]
                                ])

# rabbit_event_membercount

# @dp.callback_query_handler(text="rabbit_event_membercount")
# async def rabbit_event_membercount(call: CallbackQuery):
#     count = await get_rabbit_event_member_count()
#     await call.bot.send_message(chat_id=call.from_user.id, text=_('Текущее количество участников - {count}').format(count=count))

@dp.callback_query_handler(text="rabbit_top")
async def rabbit_event_membercount(call: CallbackQuery):
    profile_info = await search_profile("tg_id", call.from_user.id)
    top = await get_rabbit_top(profile_info['game_name'])
    top_ikb = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text=_('😎 Таблица'),url='https://docs.google.com/spreadsheets/d/e/2PACX-1vTSeHG_8NkAugiMHy9E0sgZIIjCNVzdnOrjDUY8C5o8bkuZbrKJfflZZvJr4xhI7BzaXp4_2T1AJgl_/pubhtml?gid=0&single=true')
                                   ]
                                   ])
    if top['count'] != None:
        total = await get_rabbit_event_member_count()
        if top['rank'] > 3:
            text = _('☠ Вы уничтожили {count} зайцев 🐰🩸\n'
                     '🏆 Ваше место в топе - {place} из {total}.\n'
                     '⚰ Всего за период ивента уничтожено - 325294\n\n'
                     'Спасибо за участие, возвращайтесь позже... ❤').format(count=top['count'], place=top['rank'],
                                                                            total=total)
        elif top['rank'] == 3:
            text = _('😱 Вы уничтожили {count} зайцев 🐰🩸\n'
                     '🏆 Ваше почётное место в топе - {place}.\n'
                     '⚰ Всего за период ивента уничтожено - 325294\n\n'
                     'Спасибо за участие, возвращайтесь позже... ❤').format(count=top['count'], place=top['rank'],
                                                                            total=total)
        elif top['rank'] == 2:
            text = _('🫣 Вы исстребили {count} зайцев 🐰🩸\n'
                     '🏆 Ваше заслуженное место в топе - {place}.\n'
                     '😰 Это потрясающе.'
                     '⚰ Всего за период ивента уничтожено - 325294\n\n'
                     'Спасибо за участие, возвращайтесь позже... ❤').format(count=top['count'], place=top['rank'],
                                                                            total=total)
        elif top['rank'] == 1:
            text = _(
                     '🏆 Вы - Настоящая машина для убийств.\n'
                     '🫣 Страшно называть это число - {count}.\n'
                     '🥶 Именно столько мохнатых сейчас наблюдают за вами из ада.\n'
                     '⚰ Всего за период ивента уничтожено - 325294\n\n'
                     'Спасибо за участие, возвращайтесь позже... ❤').format(count=top['count'], place=top['rank'],
                                                                            total=total)
        await call.bot.send_message(chat_id=call.from_user.id,
                                    text=text, reply_markup=top_ikb)
    else:
        await call.bot.send_message(chat_id=call.from_user.id,
                                    text=_('😥 Мы не смогли найти твои результаты, может быть они где-то потерялись?\n'), reply_markup=top_ikb)
