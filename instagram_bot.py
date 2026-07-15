import os
import time
import requests
import schedule
import logging
from instagrapi import Client
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import openai
import sys
from cfonts import render

# Load .env
load_dotenv()

# ============ LOGIN CREDENTIALS ============
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "your_username")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "your_password")
INSTAGRAM_SESSION_ID = os.getenv("INSTAGRAM_SESSION_ID", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
BANNER_TEXT = os.getenv("BANNER_TEXT", "Motivation Hub")

# Other Configs
SESSION_FILE = "session.json"
QUOTE_API_URL = "https://api.quotable.io/random?tags=motivational"

# ============ SETUP ============
logging.basicConfig(
    filename="insta_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Instagram Client
cl = Client()

def print_banner():
    """Display cfonts banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    logo = render('BOT', font='block', colors=['blue', 'white'], align='center', space=True)
    print(logo)
    
    credit = "𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗱 𝗯𝘆 — { @kozpy }"
    print(f"\033[91m{credit.center(60)}\033[0m")
    
    print("\n" + "="*60)
    print(f"\033[92m📌 Channel: {BANNER_TEXT}\033[0m")
    print(f"\033[93m⏰ Schedule: Daily at 9:00 AM\033[0m")
    print(f"\033[96m📊 Status: RUNNING...\033[0m")
    print("="*60 + "\n")
    
    logging.info("🚀 Bot Started Successfully!")

def login():
    """Smart Login - Tries multiple methods"""
    try:
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.set_user(INSTAGRAM_USERNAME)
            logging.info("✅ Logged in using Session File!")
            return True
        
        if INSTAGRAM_SESSION_ID:
            cl.set_user(INSTAGRAM_USERNAME)
            cl.set_settings({"sessionid": INSTAGRAM_SESSION_ID})
            logging.info("✅ Logged in using Session ID!")
            return True
        
        if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            cl.dump_settings(SESSION_FILE)
            logging.info("✅ Logged in using Username/Password!")
            return True
        
        logging.error("❌ No login credentials found!")
        return False
        
    except Exception as e:
        logging.error(f"❌ Login Failed: {e}")
        return False

def fetch_quote():
    """Fetch Motivational Quote"""
    try:
        response = requests.get(QUOTE_API_URL, timeout=10)
        data = response.json()
        return data["content"], data["author"]
    except Exception as e:
        logging.error(f"❌ Failed to fetch quote: {e}")
        return None, None

def generate_ai_caption(quote):
    """Generate AI caption with banner name"""
    try:
        if not OPENAI_API_KEY:
            return f"🚀 {quote[:50]}...\n\nFollow @{BANNER_TEXT} for daily motivation! #Motivation #Success #Inspiration"
        
        openai.api_key = OPENAI_API_KEY
        prompt = f"""Create an engaging Instagram caption for this motivational quote: "{quote}". 
        Include the channel name @{BANNER_TEXT} naturally. 
        Keep it short, inspiring, and add 3 trending hashtags."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"❌ AI caption failed: {e}")
        return f"✨ Stay inspired! Follow @{BANNER_TEXT} for daily motivation 💪\n#Motivation #Success #Inspiration"

def create_motivational_image(quote, author):
    """Generate image with quote + custom banner"""
    img = Image.new('RGB', (1080, 1080), color=(20, 20, 30))
    draw = ImageDraw.Draw(img)
    
    for i in range(1080):
        color = (20 + i//20, 20 + i//30, 30 + i//20)
        draw.line([(0, i), (1080, i)], fill=color)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 55)
        font_medium = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        font_large = font_medium = font_small = ImageFont.load_default()
    
    # Top Banner
    draw.rectangle([(0, 0), (1080, 120)], fill=(255, 215, 0))
    draw.rectangle([(0, 115), (1080, 120)], fill=(255, 180, 0))
    
    banner_text = f"🌟 {BANNER_TEXT} 🌟"
    bbox = draw.textbbox((0, 0), banner_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_x = (1080 - text_width) // 2
    draw.text((text_x, 30), banner_text, fill=(0, 0, 0), font=font_large)
    
    # Quote
    words = quote.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font_medium)
        if bbox[2] - bbox[0] < 900:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    y_position = 200
    for line in lines:
        draw.text((100, y_position), line, fill=(255, 255, 255), font=font_medium)
        y_position += 60
    
    # Author
    draw.text((100, y_position + 20), f"— {author}", fill=(255, 215, 0), font=font_small)
    
    # Bottom Banner
    draw.rectangle([(0, 980), (1080, 1080)], fill=(255, 215, 0))
    draw.text((300, 995), f"@{BANNER_TEXT}", fill=(0, 0, 0), font=font_large)
    
    img_path = "quote_post.jpg"
    img.save(img_path, quality=95)
    return img_path

def post_motivational_quote():
    """Post to Instagram Feed"""
    try:
        print("\033[93m📝 Fetching quote...\033[0m")
        quote, author = fetch_quote()
        if not quote:
            logging.warning("⚠️ No quote found. Skipping post.")
            return
        
        print("\033[96m🤖 Generating AI caption...\033[0m")
        caption = generate_ai_caption(quote)
        
        print("\033[95m🎨 Creating image with banner...\033[0m")
        img_path = create_motivational_image(quote, author)
        
        print("\033[94m📤 Uploading to Instagram Feed...\033[0m")
        cl.photo_upload(img_path, caption=caption)
        
        print(f"\033[92m✅ Posted Successfully! 📍 {BANNER_TEXT}\033[0m")
        logging.info(f"✅ Posted: {quote[:50]}...")
        
        if os.path.exists(img_path):
            os.remove(img_path)
            
    except Exception as e:
        logging.error(f"❌ Failed to post: {e}")
        print(f"\033[91m❌ Error: {e}\033[0m")

def relogin():
    """Refresh session"""
    print("\033[93m🔄 Refreshing session...\033[0m")
    login()

def run_now():
    """Manual run command"""
    print("\n\033[92m🚀 Running manual post...\033[0m")
    post_motivational_quote()

# ============ MAIN EXECUTION ============
if __name__ == "__main__":
    print_banner()
    
    print("\033[94m🔐 Logging in...\033[0m")
    if not login():
        print("\033[91m❌ Login failed! Check your credentials.\033[0m")
        sys.exit(1)
    
    schedule.every().day.at("09:00").do(post_motivational_quote)
    schedule.every().day.at("00:00").do(relogin)
    
    print("\n\033[92m⏰ Schedule Set:\033[0m")
    print("  • Daily Post: 9:00 AM")
    print("  • Session Refresh: 12:00 AM")
    print("\n\033[91m📌 Press Ctrl+C to stop\033[0m")
    print("="*60)
    
    # Uncomment to test immediately
    # post_motivational_quote()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n\n\033[91m🛑 Bot stopped by user\033[0m")
        logging.info("🛑 Bot stopped by user")
