# 🤖 Instagram Motivational Quote Bot

## 🚀 Features
- ✅ Posts daily motivational quotes automatically
- ✅ AI-generated captions using OpenAI (Optional)
- ✅ Custom banner with your channel name on images
- ✅ Auto-posts to Instagram feed
- ✅ Session management (No need to login every time)
- ✅ Beautiful cfonts banner on startup

---

## 📦 Installation

```bash
# 1. Download and extract the ZIP file
# 2. Open terminal/CMD in the project folder
# 3. Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Setup (Important!)

### **Step 1: Create `.env` File**

Create a file named **`.env`** in the project folder and add this:

```env
# Instagram Credentials (Replace with yours)
INSTAGRAM_USERNAME=your_username_here
INSTAGRAM_PASSWORD=your_password_here

# OpenAI API Key (Optional - for AI captions)
OPENAI_API_KEY=your_openai_api_key_here

# Your Channel Name (Shows on image banner)
BANNER_TEXT=your_channel_name
```

### **Step 2: Add Your Values**

Example:
```env
INSTAGRAM_USERNAME=john_doe
INSTAGRAM_PASSWORD=MyPass@123
BANNER_TEXT=john_doe
```

---

## 🚀 Run the Bot

```bash
python main.py
```

---

## 📱 What Happens?

- ✅ Daily post at: **9:00 AM**
- ✅ Session refresh at: **12:00 AM**
- ✅ Press `Ctrl+C` to stop

---

## 📸 Image Preview

Your image will look like this:

```
╔═══════════════════════════════╗
║  🌟 your_channel_name 🌟     ║
║                               ║
║  "Quote appears here"        ║
║                               ║
║  — Author                    ║
║                               ║
║  @your_channel_name          ║
╚═══════════════════════════════╝
```

---

## ❓ Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| `.env` file not found | Create `.env` file in project folder |
| Login fails | Use Session ID method (see below) |
| 2FA issue | Turn off 2FA or use Session ID |

---

## 🔑 Session ID Method (More Stable)

If username/password doesn't work:

1. **Login** to Instagram in your browser
2. Press **F12** → **Application** → **Cookies**
3. Find and copy `sessionid` value
4. Add to `.env` file:
```env
INSTAGRAM_SESSION_ID=1234567890%3Aabc123def456%3A12
```

---

## 📝 Credits

**Developed by — { @kozpy }**

---

## 📄 License

MIT License - Free to use and modify
