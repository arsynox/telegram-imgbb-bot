from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from keyboards.inline import get_server_selection_keyboard, get_subscription_keyboard, get_main_menu_keyboard
from utils.subscription import check_subscription
from database import Database

db = Database()

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    data = query.data
    
    if data.startswith("server_"):
        if data == "server_info":
            info_text = """
🖥️ **Server Information**

🚀 **Server 1 (6 Months):** 
   • Files auto-delete after 6 months
   • Best for temporary sharing
   • High-speed uploads

⚡ **Server 2 (1 Month):**
   • Files auto-delete after 1 month  
   • Perfect for short-term use
   • Maximum reliability

🔥 **Server 3 (Permanent):**
   • Files stored permanently
   • Never expires automatically
   • Best for long-term storage

💡 **Choose based on your needs:**
• Short-term sharing → Server 1 or 2
• Long-term storage → Server 3
            """
            await query.edit_message_text(
                info_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_server_selection_keyboard()
            )
        else:
            server = data.replace("server_", "")
            db.update_user_server(user.id, server)
            
            server_info = config.IMGBB_SERVERS.get(server, {})
            server_name = server_info.get('name', 'Unknown Server')
            server_desc = server_info.get('description', 'No description')
            server_icon = server_info.get('icon', '📁')
            
            await query.edit_message_text(
                f"✅ **Server Selected!**\n\n"
                f"{server_icon} **Active Server:** {server_name}\n"
                f"📝 **Info:** {server_desc}\n\n"
                f"🚀 **Ready to upload!** Send me any image and I'll give you an instant link!\n\n"
                f"💡 *Tip: You can change servers anytime using the menu below.*",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_main_menu_keyboard()
            )
    
    elif data == "check_subscription":
        is_subscribed = await check_subscription(context.bot, user.id)
        
        if is_subscribed:
            await query.edit_message_text(
                "✅ **Subscription Verified!**\n\n" + config.WELCOME_MESSAGE,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_server_selection_keyboard()
            )
        else:
            await query.edit_message_text(
                "❌ **Not subscribed yet!**\n\n" + 
                config.SUBSCRIPTION_MESSAGE.format(channel=config.CHANNEL_USERNAME),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_subscription_keyboard()
            )
    
    elif data == "change_server":
        await query.edit_message_text(
            "🔄 **Choose New Server:**\n\nSelect your preferred server for optimal performance:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_server_selection_keyboard()
        )
    
    elif data == "my_stats":
        # Implementation for user statistics
        await query.edit_message_text(
            "📊 **Your Statistics**\n\n"
            "🚧 Statistics feature coming soon!\n"
            "Stay tuned for detailed upload analytics.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu_keyboard()
        )
    
    elif data == "help":
        help_text = """
🔥 **Quick Help**

**Steps:**
1️⃣ Choose server
2️⃣ Send image  
3️⃣ Get link instantly!

**Server Types:**
• 🚀 Server 1: 6 months storage
• ⚡ Server 2: 1 month storage  
• 🔥 Server 3: Permanent storage

**Tips:**
• Use Server 1/2 for temporary sharing
• Use Server 3 for permanent storage
• All servers have high-speed upload

Need more help? Use /help command!
        """
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu_keyboard()
        )
    
    elif data == "tips":
        tips_text = """
💡 **Pro Tips**

🚀 **For best results:**
• Compress large images before upload
• Use PNG for quality, JPG for size
• Clear image names work better

⚡ **Server Selection:**
• Server 1 (6 months): Best for sharing
• Server 2 (1 month): Quick temporary use
• Server 3 (Permanent): Long-term storage

🔥 **Advanced:**
• Bookmark permanent links from Server 3
• Use Server 1/2 for social media sharing
• Server 3 ideal for portfolios & archives
        """
        await query.edit_message_text(
            tips_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu_keyboard()
        )
