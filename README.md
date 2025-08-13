## WhatsApp Neonize Bot 🤖

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Neonize](https://img.shields.io/badge/Neonize-Latest-green.svg)](https://github.com/krypton-byte/neonize)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)]()

> 🚀 **Powerful WhatsApp automation bot built with Python and Neonize library**

A robust, production-ready WhatsApp bot that provides automated messaging, contact management, and various utility features with comprehensive error handling and 24/7 uptime monitoring.

## ✨ Features

### 🔧 **Core Functions**
- 🏓 **Ping/Pong** - Connection testing
- 📊 **Status Monitoring** - Real-time bot health check
- 🔊 **Echo Command** - Message echoing for testing
- ℹ️ **Bot Information** - Detailed system information

### 📱 **WhatsApp Integration**
- 📸 **Profile Pictures** - Retrieve user profile images
- 🔒 **Privacy Settings** - Access privacy configurations
- ⚙️ **Chat Settings** - Manage chat configurations
- 📋 **Contact Management** - Safe contact handling (with crash protection)

### 🛡️ **Reliability Features**
- 🔄 **Auto-Reconnection** - Automatic connection recovery
- 💓 **Heartbeat Monitoring** - System health tracking
- ⏰ **Timeout Protection** - Prevents hanging operations
- 🚨 **Crash Prevention** - Enhanced error handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- WhatsApp account
- Internet connection

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/classyid/whatsapp-neonize-bot.git
cd whatsapp-neonize-bot
```

2. **Install dependencies:**
```bash
pip install neonize
```

3. **Run the bot:**
```bash
python bot.py
```

4. **Scan QR Code:**
   - QR code will appear in terminal
   - Open WhatsApp on your phone
   - Go to Settings > Linked Devices
   - Scan the QR code

## 💬 Commands

| Command | Description | Status |
|---------|-------------|--------|
| `ping` | Test bot connection | ✅ Stable |
| `status` | Check bot status | ✅ Stable |
| `help` | Show all commands | ✅ Stable |
| `info` | Bot information | ✅ Stable |
| `echo [text]` | Echo your message | ✅ Stable |
| `profile_pict` | Get profile picture | ⚠️ Privacy dependent |
| `status_privacy` | Get privacy settings | ⚠️ Limited access |
| `get_chat_settings` | Get chat settings | ⚠️ Limited access |
| `download_contacts` | Download contacts | ❌ Temporarily disabled |

## 🔧 Configuration

### Environment Setup
```python
# Database location
DATABASE_PATH = "db.sqlite3"

# Logging level
LOG_LEVEL = logging.DEBUG

# Heartbeat interval (seconds)
HEARTBEAT_INTERVAL = 60
```

### Safety Features
- **Contact Download Protection** - Prevents crashes from empty contact lists
- **Timeout Management** - 15-30 second timeouts for all operations
- **Retry Mechanism** - Up to 3 retries for failed operations
- **Graceful Shutdown** - Proper cleanup on exit

## 🐛 Known Issues

### Contact Download Bug
- **Issue:** Library crashes when accessing empty contacts
- **Status:** Temporarily disabled with warning system
- **Workaround:** Manual contact management only
- **Fix:** Awaiting upstream library update

### Privacy Limitations
- Some features depend on WhatsApp privacy settings
- Profile pictures may not be accessible if privacy restricted
- Status information limited by user permissions

## 🔍 Troubleshooting

### Bot Won't Connect
```bash
# Check internet connection
ping google.com

# Verify Python version
python --version

# Reinstall dependencies
pip uninstall neonize
pip install neonize
```

### QR Code Issues
- Ensure WhatsApp Web is not already connected elsewhere
- Try refreshing by restarting the bot
- Check phone's internet connection

### Crash on Startup
- Delete `db.sqlite3` to reset session
- Ensure no other WhatsApp bots are running
- Check Python permissions

## 📊 Monitoring

The bot includes built-in monitoring:
- **Heartbeat System** - 60-second intervals
- **Connection Status** - Real-time tracking
- **Error Logging** - Comprehensive error capture
- **Uptime Counter** - Runtime tracking

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

- Use responsibly and respect WhatsApp Terms of Service
- This bot is for educational and automation purposes
- Not affiliated with WhatsApp Inc.
- Use at your own risk

## 🙏 Acknowledgments

- [Neonize](https://github.com/krypton-byte/neonize) - WhatsApp Web API library
- [WhatsApp](https://whatsapp.com) - Messaging platform
- Python Community - Async/await support

## 📞 Support

- 📧 **Contact:** kontak@classy.id

---

**⭐ Star this repository if it helped you!**

Made with ❤️ by [Your Name](https://github.com/classyid)
