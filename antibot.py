import asyncio
import random
from dataclasses import dataclass
from typing import Union

from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Filter
from aiogram.types import ChatMemberUpdated, Message, User
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.formatting import Bold, Text, TextMention

from captcha.image import ImageCaptcha


router = Router()


@dataclass
class AntibotUser:
	user: User
	code: str
	bot_message: Message


antibot_users: dict[int, AntibotUser] = {}


class IsCheckingFilter(Filter):
	def __init__(self, antibot_users: dict[int, AntibotUser]):
		self.antibot_users = antibot_users

	async def __call__(self, message: Message) -> bool:
		return message.from_user.id in self.antibot_users


def generate_captcha_code() -> str:
	return "".join(random.choices("1234567890", k=5))


async def send_antibot_message(user: User, source: Union[Message, ChatMemberUpdated]) -> None:
	bot = source.bot
	text = Text(
		"Привет, ",
		TextMention(user.full_name, user=user),
		"!\n",
		"\n",
		Bold("В целях безопасности"),
		", пожалуйста, вам необходимо пройти капчу:\n",
		"Для ответа просто ответьте <код> в вашем сообщении\n",
		"\n",
		"Если вы не пройдёте капчу в течение 2 минут, вы будете удалены из группы.\n",
	)
	captcha = ImageCaptcha(width=280, height=90)
	code = generate_captcha_code()
	data = BufferedInputFile(captcha.generate(code).read(), filename="captcha.png")
	match source:
		case Message() as message:
			bot_message = await message.answer_photo(
				**text.as_caption_kwargs(),
				photo=data,
				disable_notification=True,
				show_caption_above_media=True,
			)
		case ChatMemberUpdated() as update:
			bot_message = await update.answer_photo(
				**text.as_caption_kwargs(),
				photo=data,
				disable_notification=True,
				show_caption_above_media=True,
			)
	antibot_users[user.id] = AntibotUser(user=user, code=code, bot_message=bot_message)
	await asyncio.sleep(120)
	if user.id in antibot_users:
		await bot_message.delete()
		await bot.ban_chat_member(chat_id=bot_message.chat.id, user_id=user.id)
		await bot.unban_chat_member(chat_id=bot_message.chat.id, user_id=user.id)
		del antibot_users[user.id]


@router.chat_member()
async def chat_member_update_handler(update: ChatMemberUpdated) -> None:
	if update.new_chat_member.status != ChatMemberStatus.MEMBER:
		return
	from_member = await update.bot.get_chat_member(chat_id=update.chat.id, user_id=update.from_user.id)
	if from_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
		return
	if update.new_chat_member.user.is_bot:
		return
	await send_antibot_message(update.new_chat_member.user, update)


@router.message(IsCheckingFilter(antibot_users))
async def message_handler(message: Message) -> None:
	if message.from_user.id not in antibot_users:
		return
	antibot_user = antibot_users[message.from_user.id]
	await message.delete()
	if message.text and message.text.strip() == antibot_user.code:
		await antibot_user.bot_message.delete()
		success_message_text = Text(
			"Спасибо, ",
			TextMention(message.from_user.full_name, user=message.from_user),
			"!\n",
			"Добро пожаловать в группу!",
		)
		success_message = await message.answer(
			**success_message_text.as_kwargs(),
			disable_notification=True,
		)
		del antibot_users[message.from_user.id]
		await asyncio.sleep(3)
		await success_message.delete()
	else:
		wrong_message_text = Text(
			"Неправильный код, ",
			TextMention(message.from_user.full_name, user=message.from_user),
			". Попробуйте ещё раз.",
		)
		wrong_message = await message.answer(
			**wrong_message_text.as_kwargs(),
			disable_notification=True,
		)
		await asyncio.sleep(3)
		await wrong_message.delete()


