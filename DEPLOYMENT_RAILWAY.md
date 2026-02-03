═══════════════════════════════════════════════════════════════════════════════
                         RAILWAY.APP DEPLOYMENT GUIDE
                    Deploy Agentic AI Honeypot to Free Platform
═══════════════════════════════════════════════════════════════════════════════

PLATFORM: Railway.app (Free tier: 500 hours/month = 20 days continuous)
TIME TO DEPLOY: ~15 minutes
COST: FREE

═══════════════════════════════════════════════════════════════════════════════
                              STEP-BY-STEP GUIDE
═══════════════════════════════════════════════════════════════════════════════

STEP 1: CREATE RAILWAY ACCOUNT (2 minutes)
────────────────────────────────────────────
1. Go to https://railway.app
2. Click "Sign Up" → Choose "GitHub" or "Email"
3. Complete email verification
4. Skip "Create First Project" (we'll do it next)

STEP 2: CREATE RAILWAY.JSON CONFIGURATION (2 minutes)
────────────────────────────────────────────────────────
In e:\Agentic Honeypot\, create file "railway.json":

{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "startCommand": "python -m src.api"
  }
}

STEP 3: CREATE DOCKERFILE (1 minute)
──────────────────────────────────────
Create file "Dockerfile" in project root:

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV DEBUG=False

EXPOSE 8000

CMD ["python", "-m", "src.api"]

STEP 4: UPDATE API PORT CONFIGURATION (1 minute)
──────────────────────────────────────────────────
Edit configs/config.py:

# Change line ~13 from:
    API_PORT = int(os.getenv("API_PORT", 5000))

# To:
    API_PORT = int(os.getenv("API_PORT", 8000))

Also update src/api.py around line 300:

# Change from:
    app.run(host=config.API_HOST, port=config.API_PORT, use_reloader=False, debug=False)

# To:
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        use_reloader=False,
        debug=False,
        threaded=True
    )

STEP 5: CREATE .RAILWAYENV FILE (1 minute)
───────────────────────────────────────────
Create ".railwayenv" in project root (note: no dot at start in Railway UI):

FLASK_ENV=production
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
API_KEYS=test_key_12345
AUTHORIZED_IPS=*
LOG_LEVEL=INFO

STEP 6: PUSH TO GITHUB (3 minutes)
──────────────────────────────────
1. Create GitHub repository at https://github.com/new
   - Name: agentic-honeypot
   - Public or Private (your choice)

2. In project directory, run:
   git init
   git add .
   git commit -m "Initial commit: Agentic AI Honeypot System"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/agentic-honeypot.git
   git push -u origin main

STEP 7: DEPLOY ON RAILWAY (3 minutes)
─────────────────────────────────────
1. Go to https://railway.app/dashboard
2. Click "New Project" → "Deploy from GitHub"
3. Connect GitHub account
4. Select "agentic-honeypot" repository
5. Click "Deploy"
6. Wait for build to complete (2-5 minutes)
7. In Railway dashboard, you'll see your domain like:
   https://agentic-honeypot-production.up.railway.app

STEP 8: GET YOUR DEPLOYED URL (1 minute)
─────────────────────────────────────────
1. In Railway dashboard, go to your project
2. Click "Deployments" tab
3. Click on the green checkmark (successful deployment)
4. Copy the "Deployment URL" - looks like:
   https://agentic-honeypot-production.up.railway.app

STEP 9: UPDATE FRONTEND FOR DEPLOYED API (2 minutes)
──────────────────────────────────────────────────────
Edit "advanced_ui.html" (or index.html):

Line ~260, change:
  const API_BASE = 'http://localhost:5000';

To:
  const API_BASE = 'https://YOUR_RAILWAY_DOMAIN';

Example:
  const API_BASE = 'https://agentic-honeypot-production.up.railway.app';

STEP 10: ACCESS YOUR DEPLOYMENT (1 minute)
───────────────────────────────────────────
Frontend URL:
  https://agentic-honeypot-production.up.railway.app/

API Health Check:
  https://agentic-honeypot-production.up.railway.app/health

Create Conversation API:
  POST https://agentic-honeypot-production.up.railway.app/api/v1/conversation

═══════════════════════════════════════════════════════════════════════════════
                          QUICK START AFTER DEPLOYMENT
═══════════════════════════════════════════════════════════════════════════════

1. Open deployed URL in browser
2. Select a victim persona (Rajesh Kumar, Priya Sharma, or Arjun Nair)
3. Click "Create Conversation"
4. Type a scammer message in the textarea, e.g.:
   "Sir, your bank account has been compromised. Verify your UPI ID immediately."
5. Click "Send Message"
6. Watch AI victim respond and see intelligence extraction
7. Click "Export JSON" to download conversation data

═══════════════════════════════════════════════════════════════════════════════
                              TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

Issue: Build fails with "ModuleNotFoundError"
Solution: Ensure requirements.txt is in root directory and has all dependencies:
  pip freeze > requirements.txt

Issue: API returns 401 errors
Solution: Verify AUTHORIZED_IPS=* in .railwayenv

Issue: Frontend can't connect to API (CORS error)
Solution: Ensure src/api.py has:
  from flask_cors import CORS
  CORS(app)

Issue: Deployment shows "Port already in use"
Solution: Railway assigns random ports. Don't hardcode port, use env variable.

Issue: Database errors
Solution: Railway doesn't persist SQLite. Use PostgreSQL addon:
  - In Railway dashboard, click "Add"
  - Select "PostgreSQL"
  - It auto-sets DATABASE_URL env var

═══════════════════════════════════════════════════════════════════════════════
                            PRODUCTION SETUP
═══════════════════════════════════════════════════════════════════════════════

For production deployment, add these to .railwayenv:

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:pass@localhost:5432/honeypot

# Redis Cache
REDIS_URL=redis://localhost:6379

# Environment
FLASK_ENV=production
DEBUG=False
LOG_LEVEL=WARNING

# Security
AUTHORIZED_IPS=*
API_KEYS=your_secure_key_here

# Limits
MAX_CONVERSATION_TURNS=100
CONVERSATION_TIMEOUT_MINUTES=60

═══════════════════════════════════════════════════════════════════════════════
                              FREE TIER LIMITS
═══════════════════════════════════════════════════════════════════════════════

Railway Free Tier:
- 500 hours/month (continuous 24/7 = ~20 days)
- 5GB egress/month
- Shared CPU
- 5GB disk
- Can pause after usage if needed

Cost after free tier: $0.25/hour (optional)

═══════════════════════════════════════════════════════════════════════════════

Deployment Complete! 🚀
Your Agentic AI Honeypot is now live and accessible globally!

═══════════════════════════════════════════════════════════════════════════════
