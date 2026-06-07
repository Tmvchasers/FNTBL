````markdown name=README.md
# 🎮 Fortnite Matchmaking Bot GUI

A powerful **no-code desktop application** that turns your Fortnite alt-account into an automated matchmaking bot. Perfect for creating Level 1 bot lobbies for custom games!

---

## ⚡ Quick Start (Easiest Way)

### **Option 1: Download Pre-Built Executable (RECOMMENDED)**

1. **Go to Releases** → https://github.com/Tmvchasers/FNTBL/releases
2. **Download** `FortniteMatchmakingBot.exe`
3. **Double-click** to run (no installation needed!)
4. Enter your bot credentials and click "START BOT"

✅ **No Python required | No terminal needed | Just download and play!**

---

## 🛠️ Features

✨ **Easy-to-Use GUI**
- Paste Account ID, Device ID, Secret Key
- One-click START/STOP button
- Real-time status indicator (green = online)
- Live console log with timestamps

🤖 **Intelligent Bot Behavior**
- Auto-accepts all friend requests
- Auto-joins all party invites
- Detects game mode automatically:
  - **Unranked modes** (BR, Zero Build, OG) → Leaves to stay Level 1
  - **Ranked/Reload modes** → Posts "Mode not supported" and leaves

⚙️ **Professional Architecture**
- Background threading (GUI never freezes)
- Async/await event handling
- Clean disconnect & reconnect support
- Secure credential handling

---

## 📥 Installation Methods

### **Method 1: Download Executable (NO CODING)**
- Download from Releases tab
- Run the .exe file
- Done! ✅

### **Method 2: Run from Python Source Code**

**Requirements:**
- Python 3.8+
- pip (Python package manager)

**Steps:**
```bash
# 1. Clone the repository
git clone https://github.com/Tmvchasers/FNTBL.git
cd FNTBL

# 2. Install dependencies
pip install customtkinter fortnitepy

# 3. Run the bot
python fortnite_matchmaking_bot.py
```

### **Method 3: Build Your Own Executable**

If you want to compile the executable yourself:

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Install bot dependencies
pip install customtkinter fortnitepy

# 3. Build the executable
pyinstaller build_exe.py

# 4. Find your executable in the /dist folder
# The .exe file will be at: dist/FortniteMatchmakingBot.exe
```

---

## 🚀 How to Use

### **Step 1: Get Your Bot Credentials**

You'll need three things from your Fortnite alt-account:

- **Account ID**: Your Epic Games email or username
- **Device ID**: Device identifier from launcher authentication
- **Secret Key**: Your Epic Games password or launcher token

*(These are used ONLY for authenticating your bot account to Epic Games)*

### **Step 2: Launch the App**

- **Option A**: Double-click `FortniteMatchmakingBot.exe`
- **Option B**: Run `python fortnite_matchmaking_bot.py`

### **Step 3: Enter Credentials**

```
┌─────────────────────────────────────┐
│  Fortnite Matchmaking Bot           │
│                                     │
│  Account ID: [your@email.com    ]  │
│  Device ID:  [device_token      ]  │
│  Secret Key: [••••••••••••••••  ]  │
│                                     │
│  ┌─────────────────────────────┐   │
│  │    ► START BOT ◄            │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### **Step 4: Click START BOT**

Button turns **GREEN** and shows:
```
[10:15:23] Starting bot...
[10:15:24] Initializing Fortnite bot client...
[10:15:25] Connecting to Epic Games servers...
[10:15:26] Bot connected successfully!
[10:15:26] Bot Online as YourBotName
[10:15:26] Waiting for party invites...
```

### **Step 5: Bot Runs Automatically**

The bot will:
- ✅ Auto-accept friend requests
- ✅ Auto-join party invites
- ✅ Watch for matchmaking
- ✅ Leave for unranked modes (stays Level 1)
- ✅ Leave for ranked modes (posts message)

Example log:
```
[10:16:10] Joined party from PlayerName
[10:16:30] Party member joined: PlayerName2
[10:17:00] Matchmaking found: Unranked Battle Royale
[10:17:01] Unranked mode detected - leaving party to maintain Level 1
```

### **Step 6: Stop the Bot**

Click the **STOP BOT** button (turns RED):
```
[10:18:00] Stopping bot...
[10:18:01] Disconnecting bot...
[10:18:02] Bot disconnected
[10:18:02] Bot stopped
```

---

## 💡 Use Cases

- 🎯 **Custom Lobby Creation**: Use bot as a placeholder for full teams
- 📊 **Content Creation**: Populate custom game lobbies for streamers
- 🎮 **Scrims & Events**: Organize matchmaking for competitive matches
- 🏆 **Tournament Setup**: Fill bot slots in organized competitions

---

## 🔒 Security & Privacy

- Credentials are **ONLY used for bot authentication**
- No data is sent to external servers
- No telemetry or tracking
- Open-source code (verify it yourself!)
- Runs entirely on your machine

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| **"fortnitepy not installed" error** | Run: `pip install fortnitepy` |
| **"Please fill in all credential fields"** | Make sure all 3 fields have text |
| **Bot won't connect** | Verify credentials are correct |
| **"Mode not supported" spam** | Bot is working! Parties selecting Ranked/Reload modes |
| **GUI is slow/freezing** | Wait a moment - bot processes in background |
| **Can't find .exe file** | Check `/dist` folder after building |

---

## 📝 File Structure

```
FNTBL/
├── fortnite_matchmaking_bot.py    ← Main bot application
├── build_exe.py                   ← Build script for .exe
├── README.md                      ← This file
└── dist/
    └── FortniteMatchmakingBot.exe ← Your executable (after build)
```

---

## 🎯 System Requirements

**For Pre-Built Executable:**
- Windows 10 or later
- ~50MB disk space
- Internet connection

**For Running from Python:**
- Python 3.8 or later
- pip package manager
- ~100MB for dependencies
- Windows, Mac, or Linux

---

## 📞 Support & Issues

Having problems? Here's what to do:

1. **Check Credentials**: Verify Account ID, Device ID, Secret Key are correct
2. **Check Internet**: Ensure you have a stable connection
3. **Restart the App**: Sometimes a fresh start fixes issues
4. **Check GitHub Issues**: https://github.com/Tmvchasers/FNTBL/issues

---

## 📜 License

This project is provided as-is. Use at your own risk. Ensure you comply with Epic Games' Terms of Service when using automation tools.

---

## 🙌 Credits

Built with:
- **CustomTkinter** - Modern GUI framework
- **fortnitepy** - Fortnite API wrapper
- **PyInstaller** - Python to executable converter

---

**Ready to get started? Download the .exe from Releases now! 🚀**

````
