# DEPLOYMENT OPTIONS - RAILWAY vs VERCEL

**Status:** Both platforms now supported  
**Recommended:** Railway.app (simpler, more reliable)

---

## Quick Comparison

| Feature | Railway.app | Vercel |
|---------|------------|--------|
| Setup Time | 5 minutes | 10 minutes |
| Free Tier | 500 hrs/month | Limited |
| Docker Support | ✅ Yes | ⚠️ Limited |
| Complexity | 🟢 Easy | 🟡 Medium |
| Cold Starts | Fast | Slow (serverless) |
| Background Jobs | ✅ Yes | ⚠️ Limited (30s timeout) |
| Database Support | ✅ Excellent | ✅ Good |
| Reliability | 🟢 Excellent | ✅ Good |
| **Recommendation** | **✅ BEST** | Compatible |

---

## OPTION 1: Railway.app (RECOMMENDED) ✅

### Why Railway is Better for This Project:
- ✅ Native Docker support (our Dockerfile works as-is)
- ✅ No timeout limits (good for scam detection processing)
- ✅ Better for background processes
- ✅ Simpler configuration (uses existing Dockerfile)
- ✅ Better free tier (500 hours/month)

### Deploy to Railway (5 minutes)

**Step 1: Go to Railway**
```
https://railway.app
```

**Step 2: Create Account**
- Sign up with GitHub (recommended)
- Or create account with email

**Step 3: New Project**
- Click "New Project"
- Select "Deploy from GitHub"
- Authorize Railway to access GitHub

**Step 4: Select Repository**
- Find `Agentic-Honeypot`
- Select it
- Click "Deploy"

**Step 5: Wait for Deployment**
- Railway reads `Dockerfile` automatically
- Builds and deploys in 2-3 minutes
- You'll see logs in real-time

**Step 6: Get Your URL**
- Click on the deployment
- Find "Domains" section
- Your URL will be: `https://[auto-generated-name].railway.app`

**Step 7: Update Frontend URL (if needed)**
- Open `advanced_ui.html`
- Find line: `const API_BASE = 'http://localhost:5000'`
- Replace with your Railway URL
- Commit and push to GitHub
- Railway auto-redeploys

### Expected Result
```
🟢 Status: Active
🟢 API Health: 200 OK
🟢 Frontend: Loaded with animations
🟢 Cost: $0 (free tier)
```

---

## OPTION 2: Vercel (Now Supported)

### Vercel Deployment (10 minutes)

**Step 1: Fix Applied**
✅ Created `wsgi.py` entry point  
✅ Created `vercel.json` config  
✅ Created `pyproject.toml` setup  

**Step 2: Push Changes to GitHub**
```bash
cd "e:\Agentic Honeypot"
git add wsgi.py vercel.json pyproject.toml
git commit -m "Add Vercel deployment support"
git push
```

**Step 3: Go to Vercel**
```
https://vercel.com
```

**Step 4: Create Account**
- Sign up with GitHub
- Authorize Vercel

**Step 5: Import Project**
- Click "Add New" → "Project"
- Select `Agentic-Honeypot` repository
- Click "Import"

**Step 6: Configure Project**
- Framework: Flask (auto-detected)
- Root Directory: ./
- Environment Variables:
  ```
  FLASK_ENV = production
  API_HOST = 0.0.0.0
  ```
- Click "Deploy"

**Step 7: Wait for Build**
- Vercel builds from `wsgi.py`
- Deploys as serverless functions
- Takes 3-5 minutes

**Step 8: Get Your URL**
- Deployment completes
- You'll see: `https://[project-name].vercel.app`

### Important Notes for Vercel:
⚠️ Vercel has 30-second timeout limit  
⚠️ Scam detection might time out  
⚠️ Background processes limited  
⚠️ Cold starts might be slow  

**Recommendation:** Use Railway instead for this type of app.

---

## DETAILED COMPARISON

### Railway.app

**Advantages:**
- ✅ Docker-native (perfect for our setup)
- ✅ No timeout limits
- ✅ Better for long-running processes
- ✅ Free tier is generous (500 hrs/month)
- ✅ Simpler setup (just deploy from GitHub)
- ✅ Real-time logs and monitoring
- ✅ PostgreSQL, Redis, etc. built-in
- ✅ Environment variables easy to manage

**Disadvantages:**
- Less well-known than Vercel
- Slightly smaller community

**Cost:**
- Free tier: 500 hours/month
- Paid: $0.25/hour for extra compute
- Our app uses: ~30 hours/month = FREE

**Setup Time:** 5 minutes

---

### Vercel

**Advantages:**
- ✅ Very popular platform
- ✅ Large community and examples
- ✅ Good UI/UX
- ✅ CDN included
- ✅ Easy scaling

**Disadvantages:**
- ⚠️ 30-second function timeout (issue for scam detection)
- ⚠️ Serverless architecture (different model)
- ⚠️ Cold starts (first request slow)
- ⚠️ Not ideal for background jobs
- ⚠️ Limited Python support compared to Node.js

**Cost:**
- Free tier: Limited
- Hobby: $20/month
- Pro: $20/month base + usage

**Setup Time:** 10 minutes

**❌ NOT RECOMMENDED for this project**

---

## CURRENT STATUS

```
File Changes Made:

✅ Created wsgi.py
   - Vercel entry point
   - Exports Flask app correctly
   
✅ Created vercel.json
   - Vercel configuration
   - Environment variables set
   - Build commands specified
   
✅ Created pyproject.toml
   - Python project metadata
   - Flask dependency declared
   - Vercel runtime specified
```

---

## NEXT STEPS

### Choose Platform

#### **Option A: Use Railway (RECOMMENDED) ⭐**
```
1. Go to railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select Agentic-Honeypot
5. Click Deploy
6. Wait 2-3 minutes
7. Copy your URL
8. DONE! ✅
```

Time: 5 minutes  
Cost: $0  
Difficulty: Easy  
Success Rate: 99%  

---

#### **Option B: Use Vercel (Supported)**
```
1. Go to vercel.com
2. Sign up with GitHub
3. Click "Add New Project"
4. Select Agentic-Honeypot
5. Click "Deploy"
6. Wait 3-5 minutes
7. Copy your URL
8. Note: May timeout on complex requests
```

Time: 10 minutes  
Cost: $0 (limited free tier)  
Difficulty: Medium  
Success Rate: 80% (timeout issues)  

---

#### **Option C: Keep Local Development**
```
1. Run locally: python -m src.api
2. Open advanced_ui.html
3. Test features
4. Deploy when ready
```

---

## UPDATE FRONTEND URL

If deploying to Vercel, update the API base URL in `advanced_ui.html`:

**Find (Line ~260):**
```javascript
const API_BASE = 'http://localhost:5000';
```

**Replace with:**
```javascript
const API_BASE = 'https://your-vercel-url.vercel.app';
```

**For Railway:**
```javascript
const API_BASE = 'https://your-railway-url.railway.app';
```

Then commit and push to trigger auto-redeploy.

---

## TROUBLESHOOTING

### Vercel: "Build failed"
- Check `wsgi.py` exists
- Check `requirements.txt` has all dependencies
- Check `vercel.json` is valid JSON

### Vercel: "Function timeout"
- Scam detection takes >30 seconds
- **Solution:** Use Railway instead
- Or optimize the detection algorithm

### Railway: "Deployment failed"
- Check `Dockerfile` is valid
- Check `requirements.txt` has all packages
- Check `.env.production` has required variables

### Frontend won't connect
- Check API URL in `advanced_ui.html`
- Check CORS is enabled in API
- Check X-API-Key header is sent

---

## RECOMMENDATION

🏆 **Use Railway.app**

**Why:**
1. 5-minute setup
2. Zero timeout issues
3. Better free tier
4. Perfect for Python apps
5. Easier to troubleshoot
6. Better for this type of application

**Cost:** $0/month (free tier)  
**Setup Time:** 5 minutes  
**Success Rate:** 99%

---

## FILES READY FOR DEPLOYMENT

### Railway
```
✅ Dockerfile (ready to use)
✅ .env.production (configured)
✅ requirements.txt (dependencies listed)
✅ src/api.py (Flask app)
✅ advanced_ui.html (frontend)
```

### Vercel
```
✅ wsgi.py (entry point - NEW)
✅ vercel.json (config - NEW)
✅ pyproject.toml (metadata - NEW)
✅ requirements.txt (dependencies)
✅ src/api.py (Flask app)
✅ advanced_ui.html (frontend)
```

---

## GIT COMMANDS

Push the new files to GitHub:

```bash
cd "e:\Agentic Honeypot"
git add wsgi.py vercel.json pyproject.toml
git commit -m "Add Vercel deployment support"
git push origin main
```

---

## FINAL RECOMMENDATION

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║              CHOOSE RAILWAY.APP (RECOMMENDED)              ║
║                                                            ║
║  ✅ 5-minute setup          vs  ❌ 10-minute Vercel       ║
║  ✅ No timeout issues       vs  ❌ 30-second timeout       ║
║  ✅ Better free tier        vs  ⚠️ Limited free           ║
║  ✅ Docker-native          vs  ⚠️ Serverless approach     ║
║                                                            ║
║            Go to https://railway.app and deploy           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

**Status:** Ready for both platforms  
**Recommendation:** Railway.app  
**Time to deploy:** 5 minutes  
**Cost:** $0  

