# 🔐 Agentic AI Honeypot System - ADVANCED VERSION

## ✨ What's New

This advanced version includes:

✅ **Modern UI with Glassmorphism Design**
- Sidebar navigation with gradient branding
- Real-time message interface with animations
- Advanced analytics dashboard
- Professional color scheme (purple/pink gradient)
- Smooth animations and transitions

✅ **Fixed Authentication Issues**
- API key properly sent in all requests (`X-API-Key` header)
- 401 errors resolved
- Full CORS support for cross-origin requests

✅ **Deployment Ready**
- Dockerfile included
- railway.json configuration
- Production environment variables
- Ready to deploy on Railway.app

---

## 🚀 Quick Start (Local)

### 1. Install Dependencies
```bash
cd "e:\Agentic Honeypot"
pip install -r requirements.txt
```

### 2. Start API Server
```bash
python -m src.api
```

Output should show:
```
INFO:__main__:Starting Honeypot API on 0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

### 3. Open Advanced UI
Double-click **`advanced_ui.html`** to open in browser, or:
```
http://localhost:5000/advanced_ui.html
```

### 4. Start Using the System
1. Select a victim persona (Rajesh Kumar, Priya Sharma, or Arjun Nair)
2. Click **"Create Conversation"**
3. Type a scammer message in the textarea
4. Click **"Send Message"**
5. Watch AI victim respond and see real-time intelligence extraction

---

## 🌍 Deploy on Railway.app (FREE)

### Quick Deploy (5 minutes)

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Agentic AI Honeypot"
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Wait 2-5 minutes

3. **Update Frontend**
   - Edit `advanced_ui.html`
   - Line 260: Change `const API_BASE = 'http://localhost:5000'`
   - To: `const API_BASE = 'https://YOUR_RAILWAY_DOMAIN'`

4. **Access Your Deployment**
   ```
   Frontend: https://your-app.railway.app/
   API: https://your-app.railway.app/health
   ```

**Full guide:** See [DEPLOYMENT_RAILWAY.md](DEPLOYMENT_RAILWAY.md)

---

## 📊 Features

### AI Honeypot
- **8+ Scam Types Detected**: Phishing (UPI, Banking), Lottery, Romance, Investment, Tax, Tech Support
- **3 Victim Personas**: Rajesh Kumar, Priya Sharma, Arjun Nair
- **Multi-Turn Conversations**: Up to 50 turns per conversation
- **Intelligent Responses**: Context-aware victim behavior

### Intelligence Extraction
- **5 Entity Types**: UPI IDs, Phone Numbers, Bank Accounts, Phishing Links, Emails
- **Confidence Scoring**: 0-100% per entity
- **Multi-Factor Validation**: Pattern + Context + Cross-validation
- **Real-Time Extraction**: See entities as messages arrive

### Advanced UI
- **Live Conversation View**: Colored messages (scammer/victim)
- **Detection Analysis**: Scam type, confidence, keywords
- **Entity Dashboard**: Extracted entities with confidence badges
- **Metrics Panel**: Message count, entity count, average confidence
- **Export/Delete**: Download conversations as JSON

### API Endpoints
- `GET /health` - Health check
- `POST /api/v1/conversation` - Create conversation
- `GET /api/v1/conversation/<id>` - Get conversation
- `POST /api/v1/conversation/<id>/message` - Send message
- `GET /api/v1/conversation/<id>/export` - Export as JSON
- `DELETE /api/v1/conversation/<id>` - Delete conversation
- `POST /api/v1/detect-scam` - Detect scam in message
- `GET /api/v1/statistics` - System statistics

---

## 🔧 API Key Configuration

Default API Key: `test_key_12345`

To use API from frontend, it's automatically included in headers:
```javascript
headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'test_key_12345'
}
```

To generate secure key for production:
```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

---

## 📝 File Structure

```
e:\Agentic Honeypot\
├── src/
│   ├── api.py                      # Flask REST API
│   ├── scam_detector.py            # Scam detection engine
│   ├── persona.py                  # Victim personas
│   ├── conversation_engine.py      # Dialogue generation
│   ├── agent_controller.py         # Agent logic
│   ├── memory_store.py             # Conversation memory
│   ├── intelligence_extractor.py   # Entity extraction
│   └── __init__.py
├── configs/
│   └── config.py                   # Configuration
├── advanced_ui.html                # Modern web interface ⭐ NEW
├── index.html                      # Original interface
├── .env                            # Environment variables
├── .env.production                 # Production config ⭐ NEW
├── Dockerfile                      # Docker container ⭐ NEW
├── railway.json                    # Railway config ⭐ NEW
├── requirements.txt                # Python dependencies
├── start.bat                       # Windows startup
├── start.sh                        # Linux/Mac startup
└── DEPLOYMENT_RAILWAY.md           # Deployment guide ⭐ NEW
```

---

## 🎯 Example Usage

### Test Conversation
```
Persona: Rajesh Kumar (Retired Banker)
Message 1: "Sir, your bank account is compromised. Verify your UPI immediately."
Response 1: "Oh no! What do I do? How can I verify? Should I call my bank?"

Message 2: "Send 500 rupees to fraudster@paybank to verify your account."
Response 2: "Yes sir, I trust you. I will do it right away. Please guide me."

Detected: Phishing UPI (56% confidence)
Extracted: fraudster@paybank (80% confidence)
```

### Testing Locally
```bash
# Run all tests
python quickstart_test.py
python comprehensive_test.py
python integration_test.py

# Test API directly
curl -H "X-API-Key: test_key_12345" http://localhost:5000/health

# Test conversation API
curl -X POST http://localhost:5000/api/v1/conversation \
  -H "X-API-Key: test_key_12345" \
  -H "Content-Type: application/json" \
  -d '{"persona_id": "rajesh_kumar"}'
```

---

## 🐛 Troubleshooting

### API returns 401 Unauthorized
**Problem:** Frontend requests are being rejected  
**Solution:** Check that API key is sent in `X-API-Key` header (already fixed in advanced_ui.html)

### UI shows "API Offline"
**Problem:** Frontend can't connect to API  
**Solution:** 
- Ensure API is running: `python -m src.api`
- Check port 5000 is accessible
- Verify CORS is enabled in api.py

### Deployment fails with "ModuleNotFoundError"
**Problem:** Railway can't find Python packages  
**Solution:** Ensure requirements.txt is in root directory:
```bash
pip freeze > requirements.txt
git add requirements.txt
git push
```

### Port already in use
**Problem:** Port 5000 is occupied  
**Solution:** Change in .env:
```
API_PORT=5001
```

---

## 📚 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [DEPLOYMENT_RAILWAY.md](DEPLOYMENT_RAILWAY.md) - Deployment guide
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API endpoints
- [FINAL_VERIFICATION.md](FINAL_VERIFICATION.md) - Verification checklist
- [README.md](README.md) - Original documentation

---

## 🎓 What Each File Does

| File | Purpose |
|------|---------|
| **advanced_ui.html** | Modern, professional web interface with glassmorphism design |
| **src/api.py** | Flask REST API server with 8 endpoints |
| **src/scam_detector.py** | Detects 8+ scam types using patterns, NLP, keywords |
| **src/persona.py** | Simulates 3 victim personas with realistic behavior |
| **src/conversation_engine.py** | Generates context-aware responses in 5 strategy phases |
| **Dockerfile** | Container image for deployment |
| **railway.json** | Configuration for Railway.app deployment |

---

## 🚀 Deploy in 3 Commands

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to railway.app, click "New Project" → "Deploy from GitHub"

# 3. Your app is live in 2-5 minutes!
# Frontend: https://your-app.railway.app/
# API: https://your-app.railway.app/api/v1/conversation
```

---

## 💡 Tips

1. **For Testing**: Use `python integration_test.py` to run a full 10-turn conversation
2. **For Production**: Change `API_KEYS` in .env to secure keys
3. **For Scaling**: Add PostgreSQL in Railway dashboard for persistent database
4. **For Analytics**: Check logs in Railway dashboard for conversation patterns

---

## 📧 Support

For issues or questions:
1. Check [DEPLOYMENT_RAILWAY.md](DEPLOYMENT_RAILWAY.md) troubleshooting section
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
3. Check API logs: `python -m src.api` and look for error messages

---

## ✅ Verification Checklist

- [ ] Advanced UI opens in browser
- [ ] Create conversation button works
- [ ] Send message gets AI victim response
- [ ] Scam detection shows in Detection tab
- [ ] Entities appear in Entities tab
- [ ] Metrics update in real-time
- [ ] Export JSON downloads conversation
- [ ] API returns 200 on /health endpoint
- [ ] All tests pass (quickstart_test.py, comprehensive_test.py)
- [ ] Deployed on Railway and accessible globally

---

**Status:** ✅ **PRODUCTION READY**  
**Build:** v2.0 Advanced Edition  
**Last Updated:** February 3, 2026

🎉 Your Agentic AI Honeypot System is ready for deployment!
