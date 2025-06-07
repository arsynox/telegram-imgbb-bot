from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import io
from utils.imgbb import ImgBBUploader
from utils.subscription import check_subscription
from database import Database
from keyboards.inline import get_main_menu_keyboard

db = Database()
imgbb = ImgBBUploader()

async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image uploads"""
    user = update.effective_user
    
    # Check subscription
    is_subscribed = await check_subscription(context.bot, user.id)
    if not is_subscribed:
        await update.message.reply_text(
            "🔒 Please join our channel first to use this service!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get user's selected server
    selected_server = db.get_user_server(user.id)
    
    # Send processing message
    processing_msg = await update.message.reply_text(
        f"🔄 **Processing your image...**\n📡 Using {config.IMGBB_SERVERS[selected_server]['name']}",
        parse_mode=ParseMode.MARKDOWN
    )
    
    try:
        # Download image
        if update.message.photo:
            file = await context.bot.get_file(update.message.photo[-1].file_id)
        elif update.message.document and update.message.document.mime_type.startswith('image/'):
            file = await context.bot.get_file(update.message.document.file_id)
        else:
            await processing_msg.edit_text("❌ Please send a valid image file!")
            return
        
        # Get image data
        image_data = await file.download_as_bytearray()
        
        # Upload to ImgBB
        result = await imgbb.upload_image(image_data, selected_server)
        
        if result and result.get('success'):
            # Log upload
            db.log_image_upload(
                user.id, 
                result['url'], 
                result.get('delete_url', ''), 
                selected_server
            )
            
            # Format size
            size_mb = round(result.get('size', 0) / (1024 * 1024), 2)
            
            success_text = f"""
🎉 **Upload Successful!**

🔗 **Direct Link:**
`{result['url']}`

📊 **Details:**
• 📏 Size: {size_mb} MB
• 🖥️ Server: {result.get('server_name', 'Unknown Server')}
• ⏰ Expires: {result.get('expiration_info', 'Unknown')}
• ⚡ Status: Ready to share!

💡 *Tip: Click the link to copy it easily!*
            """
            
            await processing_msg.edit_text(
                success_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_main_menu_keyboard()
            )
            
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'Upload failed'
            await processing_msg.edit_text(
                f"❌ **Upload Failed**\n\n🔍 Error: {error_msg}\n\n💡 Try again or change server!",
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        await processing_msg.edit_text(
            f"❌ **Error occurred**\n\n🔍 Details: {str(e)}\n\n💡 Please try again!",
            parse_mode=ParseMode.MARKDOWN
        )
