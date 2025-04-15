# app/handlers.py
import datetime
import dateparser
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from src.google_calendar import (
    create_event,
    delete_event,
    get_user_events,
    update_event,
)
from src.app.config import query_engine

# Define conversation states
(
    CHOOSING_ACTION,
    ENTERING_DATE,
    CONFIRMING_DATE,
    ENTERING_NAME,
    SELECTING_EVENT,
    ENTERING_NEW_DATE,
) = range(6)

# User state tracking
user_context = {}

# Timezone from environment variable
TIMEZONE = os.getenv("TIMEZONE", "America/Mexico_City")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_context[user_id] = {}

    # Reset the state
    context.user_data["state"] = CHOOSING_ACTION

    keyboard = [
        [InlineKeyboardButton("📅 Schedule Appointment", callback_data="agendar")],
        [InlineKeyboardButton("📍 View Hours", callback_data="horarios")],
        [InlineKeyboardButton("ℹ️ Company Information", callback_data="empresa")],
        [InlineKeyboardButton("💬 Contact Human", callback_data="humano")],
        [InlineKeyboardButton("❌ Cancel Appointment", callback_data="cancelar")],
        [InlineKeyboardButton("✏️ Edit Appointment", callback_data="editar")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "Hello! 👋 I'm *CusChatAI*, your virtual assistant.\n\n"
        "I'm here to help with your questions or to schedule an appointment.\n"
        "Please select an option from the menu below 👇"
    )

    await update.message.reply_text(
        welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
    )
    return CHOOSING_ACTION


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Initialize user context if not exists
    if user_id not in user_context:
        user_context[user_id] = {}

    data = query.data
    if data == "agendar":
        await query.edit_message_text(
            "🗓️ Great! To schedule an appointment, please tell me your preferred date and time. "
            "For example: 'Tomorrow at 3pm' or 'April 20 at 10am'"
        )
        context.user_data["state"] = ENTERING_DATE
        return ENTERING_DATE
    elif data == "horarios":
        await query.edit_message_text(
            "📍 Our available hours are:\n- Monday to Friday: 10am - 6pm\n- Saturday: 11am - 3pm\n\n"
            "Would you like to book an appointment? If so, please type 'Yes'"
        )
        return CHOOSING_ACTION
    elif data == "empresa":
        company_info = (
            "🏢 *About Our Company*\n\n"
            "We specialize in providing high-quality services tailored to your needs. "
            "Our experienced team is dedicated to delivering excellent results and ensuring customer satisfaction.\n\n"
            "*Our Services:*\n"
            "• Professional consulting\n"
            "• Customized solutions\n"
            "• Technical support\n"
            "• Training and workshops\n\n"
            "Would you like to schedule an appointment to discuss how we can help you? "
            "Just type 'Yes' to get started."
        )
        await query.edit_message_text(company_info, parse_mode="Markdown")
        return CHOOSING_ACTION
    elif data == "humano":
        await query.edit_message_text(
            "💬 A human agent will contact you shortly. In the meantime, you can ask me anything."
        )
        return CHOOSING_ACTION
    elif data == "cancelar":
        # Get user's events
        try:
            events = get_user_events(user_id)
            if not events:
                await query.edit_message_text(
                    "You don't have any upcoming appointments to cancel."
                )
                return CHOOSING_ACTION

            user_context[user_id]["events"] = events

            # Create buttons for each event
            keyboard = []
            for i, event in enumerate(events):
                start_time = event["start"]["dateTime"]
                formatted_time = datetime.datetime.fromisoformat(
                    start_time.replace("Z", "+00:00")
                ).strftime("%b %d, %Y at %I:%M %p")
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            f"{formatted_time}", callback_data=f"cancel_{i}"
                        )
                    ]
                )

            keyboard.append(
                [InlineKeyboardButton("« Back", callback_data="back_to_menu")]
            )
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                "🗓 Please select the appointment you wish to cancel:",
                reply_markup=reply_markup,
            )
            return SELECTING_EVENT
        except Exception as e:
            print(f"Error fetching events: {e}")
            await query.edit_message_text(
                "❌ Sorry, I couldn't retrieve your appointments. Please try again later."
            )
            return CHOOSING_ACTION
    elif data == "editar":
        # Similar to cancel but for editing
        try:
            events = get_user_events(user_id)
            if not events:
                await query.edit_message_text(
                    "You don't have any upcoming appointments to edit."
                )
                return CHOOSING_ACTION

            user_context[user_id]["events"] = events

            # Create buttons for each event
            keyboard = []
            for i, event in enumerate(events):
                start_time = event["start"]["dateTime"]
                formatted_time = datetime.datetime.fromisoformat(
                    start_time.replace("Z", "+00:00")
                ).strftime("%b %d, %Y at %I:%M %p")
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            f"{formatted_time}", callback_data=f"edit_{i}"
                        )
                    ]
                )

            keyboard.append(
                [InlineKeyboardButton("« Back", callback_data="back_to_menu")]
            )
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                "🗓 Please select the appointment you wish to edit:",
                reply_markup=reply_markup,
            )
            return SELECTING_EVENT
        except Exception as e:
            print(f"Error fetching events: {e}")
            await query.edit_message_text(
                "❌ Sorry, I couldn't retrieve your appointments. Please try again later."
            )
            return CHOOSING_ACTION
    elif data == "back_to_menu":
        # Return to main menu
        keyboard = [
            [InlineKeyboardButton("📅 Schedule Appointment", callback_data="agendar")],
            [InlineKeyboardButton("📍 View Hours", callback_data="horarios")],
            [InlineKeyboardButton("ℹ️ Company Information", callback_data="empresa")],
            [InlineKeyboardButton("💬 Contact Human", callback_data="humano")],
            [InlineKeyboardButton("❌ Cancel Appointment", callback_data="cancelar")],
            [InlineKeyboardButton("✏️ Edit Appointment", callback_data="editar")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        welcome_text = (
            "Hello! 👋 I'm *CusChatAI*, your virtual assistant.\n\n"
            "I'm here to help with your questions or to schedule an appointment.\n"
            "Please select an option from the menu below 👇"
        )

        await query.edit_message_text(
            welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
        )
        return CHOOSING_ACTION
    elif data.startswith("cancel_"):
        # Cancel the selected event
        try:
            event_index = int(data.split("_")[1])
            events = user_context[user_id]["events"]
            event_id = events[event_index]["id"]

            delete_event(event_id)
            await query.edit_message_text(
                "✅ Your appointment has been successfully canceled!"
            )
            return CHOOSING_ACTION
        except Exception as e:
            print(f"Error canceling event: {e}")
            await query.edit_message_text(
                "❌ An error occurred while canceling your appointment. Please try again later."
            )
            return CHOOSING_ACTION
    elif data.startswith("edit_"):
        # Store the event to edit and ask for new date
        try:
            event_index = int(data.split("_")[1])
            user_context[user_id]["edit_event_index"] = event_index

            await query.edit_message_text(
                "Please enter the new date and time for your appointment. "
                "For example: 'Tomorrow at 3pm' or 'April 20 at 10am'"
            )
            context.user_data["state"] = ENTERING_NEW_DATE
            return ENTERING_NEW_DATE
        except Exception as e:
            print(f"Error preparing event edit: {e}")
            await query.edit_message_text(
                "❌ An error occurred. Please try again later."
            )
            return CHOOSING_ACTION
    else:
        await query.edit_message_text("❌ Invalid option. Please try again.")
        return CHOOSING_ACTION


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text.strip()

    # Initialize user context if not exists
    if user_id not in user_context:
        user_context[user_id] = {}

    # Check if we're in a conversation flow
    state = context.user_data.get("state", CHOOSING_ACTION)

    print(f"Current state for user {user_id}: {state}")

    # Handle "Yes" responses for booking after viewing hours
    if state == CHOOSING_ACTION and message.lower() in ["yes", "y", "si", "sí"]:
        await update.message.reply_text(
            "🗓️ Great! To schedule an appointment, please tell me your preferred date and time. "
            "For example: 'Tomorrow at 3pm' or 'April 20 at 10am'"
        )
        context.user_data["state"] = ENTERING_DATE
        return ENTERING_DATE

    # Handle date entry
    elif state == ENTERING_DATE:
        parsed_date = dateparser.parse(
            message, settings={"PREFER_DATES_FROM": "future"}
        )
        if parsed_date:
            # Store the date and ask for confirmation
            user_context[user_id]["start_time"] = parsed_date

            formatted_date = parsed_date.strftime("%A, %B %d at %I:%M %p")
            await update.message.reply_text(
                f"📅 I found this date: {formatted_date}\n\nDo you confirm this appointment? (Yes/No)"
            )
            context.user_data["state"] = CONFIRMING_DATE
            return CONFIRMING_DATE
        else:
            await update.message.reply_text(
                "❌ I couldn't understand that date. Please try again with a clearer format like 'Tomorrow at 3pm' or 'April 20 at 10am'"
            )
            return ENTERING_DATE

    # Handle date confirmation
    elif state == CONFIRMING_DATE:
        if message.lower() in ["yes", "y", "confirm", "ok", "sure", "yep", "si", "sí"]:
            # Ask for the user's name
            await update.message.reply_text(
                "Great! 😊 Please tell me your name for the appointment:"
            )
            context.user_data["state"] = ENTERING_NAME
            return ENTERING_NAME
        else:
            await update.message.reply_text(
                "No problem. Please provide a different date and time for your appointment:"
            )
            context.user_data["state"] = ENTERING_DATE
            return ENTERING_DATE

    # Handle name entry
    elif state == ENTERING_NAME:
        # Store the name and create the event
        user_context[user_id]["client_name"] = message

        try:
            start_time = user_context[user_id]["start_time"]
            client_name = user_context[user_id]["client_name"]

            event_id = create_event(
                summary=f"Appointment with {client_name}",
                description=f"Scheduled by user {user_id} via CusChatAI bot",
                start_time=start_time,
                duration_minutes=30,
            )

            # Store the event ID for future reference
            user_context[user_id]["event_id"] = event_id

            # Reset state
            context.user_data["state"] = CHOOSING_ACTION

            formatted_date = start_time.strftime("%A, %B %d at %I:%M %p")
            await update.message.reply_text(
                f"✅ Perfect! Your appointment has been scheduled for {formatted_date}.\n\n"
                f"Name: {client_name}\n"
                f"Duration: 30 minutes\n\n"
                "You can say 'menu' anytime to return to the main menu."
            )
            return CHOOSING_ACTION
        except Exception as e:
            print(f"Error creating event: {e}")
            await update.message.reply_text(
                "❌ I'm sorry, there was an error scheduling your appointment. Please try again later."
            )
            context.user_data["state"] = CHOOSING_ACTION
            return CHOOSING_ACTION

    # Handle entering new date for editing
    elif state == ENTERING_NEW_DATE:
        parsed_date = dateparser.parse(
            message, settings={"PREFER_DATES_FROM": "future"}
        )
        if parsed_date:
            try:
                # Get the event to edit
                event_index = user_context[user_id]["edit_event_index"]
                event = user_context[user_id]["events"][event_index]
                event_id = event["id"]

                # Update the event
                event_summary = event["summary"]
                client_name = event_summary.replace("Appointment with ", "")
                if client_name == event_summary:  # No replacement happened
                    client_name = update.effective_user.first_name or "Client"

                update_event(
                    event_id=event_id,
                    summary=f"Appointment with {client_name}",
                    description=f"Edited by user {user_id} via CusChatAI bot",
                    start_time=parsed_date,
                    duration_minutes=30,
                )

                # Reset state
                context.user_data["state"] = CHOOSING_ACTION

                formatted_date = parsed_date.strftime("%A, %B %d at %I:%M %p")
                await update.message.reply_text(
                    f"✅ Your appointment has been rescheduled for {formatted_date}."
                )
                return CHOOSING_ACTION
            except Exception as e:
                print(f"Error editing event: {e}")
                await update.message.reply_text(
                    "❌ There was an error updating your appointment. Please try again later."
                )
                context.user_data["state"] = CHOOSING_ACTION
                return CHOOSING_ACTION
        else:
            await update.message.reply_text(
                "❌ I couldn't understand that date. Please try again with a clearer format."
            )
            return ENTERING_NEW_DATE

    # Check for menu command
    if message.lower() == "menu":
        await start(update, context)
        return CHOOSING_ACTION

    # If no conversation is active or we're in CHOOSING_ACTION, try to answer with the query engine
    try:
        # Check if message might be appointment-related
        if any(
            word in message.lower()
            for word in [
                "appointment",
                "book",
                "schedule",
                "reservation",
                "cita",
                "agendar",
            ]
        ):
            await update.message.reply_text(
                "It looks like you want to schedule an appointment. Please select 'Schedule Appointment' from the menu or type 'Yes' to proceed."
            )
            return CHOOSING_ACTION

        response = query_engine.query(message)
        await update.message.reply_text(str(response))
        return CHOOSING_ACTION
    except Exception as e:
        print(f"Error querying: {e}")
        await update.message.reply_text(
            "I'm not sure how to respond to that. Can you try rephrasing your question or type 'menu' to see the main options?"
        )
        return CHOOSING_ACTION
