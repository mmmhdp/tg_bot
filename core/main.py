from weather_api.api_call import WeatherApi
from telegram import (
    ReplyKeyboardMarkup,
    Update
)
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = "6545388422:AAEewfhbnRhYSuHOyKxuxFzj6Ta5vFSf3Cw"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Как там сейчас на улице?"],
                      ["А что там на недельке?"],
                      ["А как по погоде в городе N?"]]
    user = update.message.from_user
    user_name = user.full_name
    await update.message.reply_text(
        f"Привет {user_name}!\n"
        f"Я тут за погоду отвечаю. Что тебя интересует?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False,
            input_field_placeholder="А эта погода, она сейчас c нами в одной комнате?"
        ),
    )


async def after_answer(update, context):
    reply_keyboard = [["Как там сейчас на улице?"],
                      ["А что там на недельке?"],
                      ["А как по погоде в городе N?"]]
    await update.message.reply_text(
        f"Что ещё тебя интересует?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False,
            input_field_placeholder="А эта погода, она сейчас c нами в одной комнате?"
        ),
    )


async def get_current_location_for_current_info(update, context):
    await update.message.reply_text(
        "а вы сейчас где находитесь?\n"
        "если это не секрет, то отправьте мне свою геолокацию и я с удовольствием расскажу вам о погоде в вашем "
        "регионе."
    )
    return 0


async def get_current_location_for_week_info(update, context):
    await update.message.reply_text(
        "а вы сейчас где находитесь?\n"
        "если это не секрет, то отправьте мне свою геолокацию и я с удовольствием расскажу вам о погоде в вашем "
        "регионе."
    )
    return 0


async def get_location_and_show_weather(update, context):
    user_location = update.message.location
    w_api = WeatherApi()
    weather_info = w_api.get_weather_by_lat_and_lon(user_location.latitude, user_location.longitude)
    await update.message.reply_text(weather_info)


async def get_location_and_show_week_weather(update, context):
    user_location = update.message.location
    w_api = WeatherApi()
    weather_info = w_api.get_weather_for_week(user_location.latitude, user_location.longitude)
    await update.message.reply_text(weather_info)


async def get_another_city_location(update, context):
    await update.message.reply_text(
        "Отправьте название города N и я расскажу, как там сейчас с погодными условиями."
    )
    return 0


async def get_city_name_and_show_weather(update, context):
    city = update.message.text
    w_api = WeatherApi()
    weather_info = w_api.get_weather_by_city(city)
    await update.message.reply_text(weather_info)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handlers([
        CommandHandler("start", start),
    ])

    curr_day_conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[
            MessageHandler(filters.Regex("Как там сейчас на улице"), get_current_location_for_current_info),
        ],
        states={
            0: [MessageHandler(filters.LOCATION, get_location_and_show_weather)]
        },
        fallbacks=[CommandHandler("start", start)],
    )
    next_week_conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[
            MessageHandler(filters.Regex("А что там на недельке?"), get_current_location_for_week_info),
        ],
        states={
            0: [MessageHandler(filters.LOCATION, get_location_and_show_week_weather)],
        },
        fallbacks=[CommandHandler("start", start)]
    )
    another_city_conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[
            MessageHandler(filters.Regex("А как по погоде в городе N?"), get_another_city_location),
        ],
        states={
            0: [MessageHandler(filters.TEXT, get_city_name_and_show_weather)],
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(curr_day_conv_handler)
    application.add_handler(next_week_conv_handler)
    application.add_handler(another_city_conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
