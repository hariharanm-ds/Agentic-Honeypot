═══════════════════════════════════════════════════════════════════════════════
                    ADVANCED UI WALKTHROUGH & VISUAL GUIDE
                          Step-by-Step Tutorial
═══════════════════════════════════════════════════════════════════════════════

🎨 DESIGN PHILOSOPHY
═════════════════════

The Advanced UI uses modern design principles:

1. GLASSMORPHISM
   - Semi-transparent frosted glass effect
   - Cards have white background with 96% opacity
   - Backdrop blur creates depth
   - Professional and modern look

2. GRADIENT BRANDING
   - Primary gradient: Blue (#667eea) → Purple (#764ba2)
   - Accent: Pink (#f093fb) for highlights
   - Consistent throughout all buttons and headers

3. ANIMATION & MICRO-INTERACTIONS
   - Floating logo animation (continuous)
   - Slide-in messages (300ms)
   - Pop-in entity tags (300ms)
   - Pulse status indicator (2s loop)
   - Smooth tab transitions (300ms)

4. VISUAL HIERARCHY
   - Large sidebar (280px) for navigation
   - Full-width topbar with status
   - 2-column main workspace
   - Clear component separation

═══════════════════════════════════════════════════════════════════════════════
                          LAYOUT STRUCTURE
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                                  TOPBAR                                      │
│  Agentic AI Honeypot System              API Connected [●]                   │
├──────────────┬──────────────────────────────────────────────────────────────┤
│              │                                                               │
│  SIDEBAR     │  LEFT PANEL                 │  RIGHT PANEL                    │
│              │  💬 Live Conversation       │  📊 Intelligence Analysis       │
│  🔐 Logo     │                             │                                 │
│  Honeypot AI │  ┌─────────────────────┐    │  Tabs: 🎯 🏷️ 📈                │
│  (Animated)  │  │ Create conversation │    │                                 │
│              │  │ to get started      │    │  ┌──────────────────────────┐  │
│  👤 Persona  │  │                     │    │  │ Detection Results:       │  │
│  ┌─────────┐ │  │ 🚨 Scammer: "Your  │    │  │                          │  │
│  │ Rajesh  │ │  │ account compromised"│    │  │ 🎯 Type: phishing_upi    │  │
│  │ Kumar   │ │  │                     │    │  │ 📊 Confidence: 56%       │  │
│  └─────────┘ │  │ 👤 Victim: "What do│    │  │ 🔑 Keywords: verify,upi  │  │
│              │  │ I do?"              │    │  └──────────────────────────┘  │
│  💬 Message  │  │                     │    │  Entities Extracted:            │
│  ┌─────────┐ │  │ 🚨 Scammer: "Send  │    │  ┌──────────────────────────┐  │
│  │ Type    │ │  │ 500 rupees to..."   │    │  │ UPI: fraudster@bank (80%)│  │
│  │ here... │ │  │                     │    │  │ Email: scam@gmail (50%)  │  │
│  └─────────┘ │  │ 👤 Victim: "I'll do│    │  └──────────────────────────┘  │
│              │  │ it right away"      │    │  Metrics:                       │
│  [Send] [Exp]│  │                     │    │  Messages: 4  Entities: 2       │
│  [Delete]    │  │                     │    │  Confidence: 65%  Phase: 2      │
│              │  └─────────────────────┘    │                                 │
│              │                             │                                 │
└──────────────┴─────────────────────────────┴─────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                      COMPONENT BREAKDOWN
═══════════════════════════════════════════════════════════════════════════════

1️⃣ SIDEBAR (Left Navigation Panel)
──────────────────────────────────

┌─────────────────────────────┐
│  🔐 Honeypot AI            │  <- Logo section with gradient background
│  Scam Detection Engine      │     (animates up/down continuously)
├─────────────────────────────┤
│  👤 VICTIM PERSONA          │  <- Section label (uppercase, small)
│  ┌──────────────────────┐   │
│  │ [Rajesh Kumar (58) ▼]│  │  <- Dropdown selector
│  └──────────────────────┘   │  (Changes the victim to interact with)
├─────────────────────────────┤
│  [+ Create Conversation]    │  <- Primary action button
│  (gradient bg, hover lift)  │  (Gradient background, lifts on hover)
├─────────────────────────────┤
│  💬 SEND MESSAGE            │  <- Section label
│  ┌──────────────────────┐   │
│  │ Type scammer message │  │  <- Text area (100px min height)
│  │ ........            │  │
│  └──────────────────────┘   │
│  [≫ Send]                   │  <- Send button (paper plane icon)
├─────────────────────────────┤
│  [↓ Export JSON]            │  <- Export button (green gradient)
│  [🗑 Delete]                │  <- Delete button (red gradient)
│  (margin-top: auto)         │
└─────────────────────────────┘

Features:
- Sticky position (stays visible while scrolling)
- 280px fixed width
- White background with 95% opacity
- Border right for separation
- Box shadow on right edge

═══════════════════════════════════════════════════════════════════════════════

2️⃣ TOPBAR (Status & Title Bar)
──────────────────────────────

┌─────────────────────────────────────────────┐
│  🧠 Agentic AI Honeypot System     ●API OK  │
│  (Left-aligned title)         (Right status) │
└─────────────────────────────────────────────┘

Features:
- White background (95% opacity)
- Full width, 20px padding vertical
- Flexbox for spacing
- Status badge on right:
  * Green dot (●) when online
  * Red dot (●) when offline
  * Breathing animation on dot
  * Auto-checks every 30 seconds

═══════════════════════════════════════════════════════════════════════════════

3️⃣ LEFT PANEL - LIVE CONVERSATION
──────────────────────────────────

Header:
┌────────────────────────────┐
│  💬 Live Conversation      │  <- Panel header (gradient bg, white text)
└────────────────────────────┘

Content:
┌────────────────────────────────────────────┐
│ ┌──────────────────────────────────────┐  │
│ │ 📭 Create a conversation to get      │  │ <- Empty state (centered)
│ │ started                              │  │
│ └──────────────────────────────────────┘  │
│                                            │
│ When messages exist:                       │
│ ┌──────────────────────────────────────┐  │
│ │ 🚨 Scammer:                         │  │
│ │ "Your bank account is compromised.  │  │
│ │ Verify your UPI ID immediately."    │  │ <- Red-bordered (danger)
│ └──────────────────────────────────────┘  │
│                                            │
│ ┌──────────────────────────────────────┐  │
│ │ 👤 Victim:                          │  │
│ │ "Oh no! What do I do? How can I     │  │
│ │ verify? Should I call my bank?"     │  │ <- Green-bordered (success)
│ └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘

Features:
- Messages slide in from left (300ms animation)
- Scammer messages: Red left border + red tint background
- Victim messages: Green left border + green tint background
- Auto-scrolls to latest message
- Max-height with scrollbar
- Dashed border container

═══════════════════════════════════════════════════════════════════════════════

4️⃣ RIGHT PANEL - INTELLIGENCE ANALYSIS
───────────────────────────────────────

Header:
┌────────────────────────────────────────┐
│  📊 Intelligence Analysis             │  <- Gradient header
└────────────────────────────────────────┘

Tabs:
┌────────────────────────────────────────┐
│ [🎯 Detection] [🏷️ Entities] [📈 Metrics]
│                ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  <- Underline indicates active tab
└────────────────────────────────────────┘

TAB 1 - DETECTION:
┌────────────────────────────────────────┐
│ 🎯 Scam Type:     phishing_upi        │  <- Detection card
│ 📊 Confidence:    56.2%               │
│ 🔑 Keywords:      verify, upi, account│
└────────────────────────────────────────┘

TAB 2 - ENTITIES:
┌─────────────────────────────────────────────┐
│ [🔑 UPI: fraudster@paybank (80%)]          │  <- Entity tags
│ [🔑 Email: scam@gmail.com (50%)]           │  (pop-in animation)
│ [🔑 Link: https://fake-bank.com (75%)]     │
└─────────────────────────────────────────────┘

TAB 3 - METRICS:
┌──────────────────┬──────────────────┐
│   Messages: 4    │   Entities: 2    │  <- 2x2 metric grid
├──────────────────┼──────────────────┤
│ Confidence: 56%  │   Phase: 2/5     │
└──────────────────┴──────────────────┘

Features:
- Tab buttons change color on hover
- Active tab shows colored underline
- Smooth 300ms transition between tabs
- Content only displayed when tab is active

═══════════════════════════════════════════════════════════════════════════════
                      COLOR SCHEME REFERENCE
═══════════════════════════════════════════════════════════════════════════════

Primary Gradient:
  From: #667eea (Periwinkle Blue)
  To:   #764ba2 (Medium Purple)
  Used on: Headers, main buttons, metric cards

Accent Color:
  #f093fb (Hot Pink)
  Used on: Borders, highlights, emphasis

Status Colors:
  Success:  #4caf50 (Green)     - Victim messages, API connected
  Danger:   #f44336 (Red)       - Scammer messages, delete button
  Warning:  #ff9800 (Orange)    - Not used in current design
  Info:     #2196F3 (Blue)      - Detection cards, information

Neutral Colors:
  Dark:     #1a1a2e (Very Dark Blue) - Background
  Light:    #f5f7fa (Off White)      - Secondary background
  Text:     #333333 (Dark Gray)      - Body text

═══════════════════════════════════════════════════════════════════════════════
                    INTERACTIVE FEATURES & ANIMATIONS
═══════════════════════════════════════════════════════════════════════════════

1. FLOATING LOGO ANIMATION
   - Duration: 3 seconds
   - Effect: Moves up/down 10px continuously
   - Creates: Floating feeling

   @keyframes float {
       0%, 100% { transform: translateY(0px); }
       50% { transform: translateY(-10px); }
   }

2. SLIDE-IN MESSAGE ANIMATION
   - Duration: 300ms (0.3s)
   - From: Opacity 0, translateX(-10px)
   - To: Opacity 1, translateX(0)
   - Effect: Messages smoothly enter from left

3. POP-IN ENTITY TAG ANIMATION
   - Duration: 300ms
   - From: Scale 0.8, Opacity 0
   - To: Scale 1, Opacity 1
   - Effect: Tags appear with small bounce

4. PULSE STATUS DOT
   - Duration: 2 seconds, infinite loop
   - From: Opacity 1
   - To: Opacity 0.5, back to 1
   - Effect: Breathing animation

5. SPIN LOADING INDICATOR
   - Duration: 1 second, infinite loop
   - Effect: Smooth 360° rotation
   - Used on: Button when loading

6. BUTTON HOVER EFFECTS
   - On hover: translateY(-2px) - lifts up
   - On hover: box-shadow increases
   - On active: translateY(0) - returns to normal
   - Duration: 300ms smooth transition

═══════════════════════════════════════════════════════════════════════════════
                        RESPONSIVE DESIGN
═══════════════════════════════════════════════════════════════════════════════

Desktop (1200px+):
  ├─ Sidebar: 280px visible on left
  └─ Main workspace: 2-column grid (1fr 1fr)

Tablet (768px - 1200px):
  ├─ Sidebar: Still visible (280px)
  └─ Main workspace: Still 2 columns (but smaller)

Mobile (<768px):
  ├─ Sidebar: Hidden (display: none)
  └─ Main workspace: 1 column (full width)

CSS Media Query:
@media (max-width: 1200px) {
    .workspace {
        grid-template-columns: 1fr;
    }
    .sidebar {
        display: none;
    }
}

═══════════════════════════════════════════════════════════════════════════════
                    HOW TO USE - STEP BY STEP
═══════════════════════════════════════════════════════════════════════════════

STEP 1: Start API Server
─────────────────────────
Terminal:
  cd e:\Agentic Honeypot
  python -m src.api

Output:
  INFO:__main__:Starting Honeypot API on 0.0.0.0:5000
  * Running on http://127.0.0.1:5000

Status: Look for "Running on" message

STEP 2: Open Advanced UI
────────────────────────
Browser:
  Open: advanced_ui.html
  OR: http://localhost:5000/advanced_ui.html

Expected: 
  - See purple/pink gradient background
  - Sidebar on left with logo
  - Two panels on right
  - Status shows "API Connected" with green dot

STEP 3: Create Conversation
────────────────────────────
Action:
  1. Choose persona from dropdown (Rajesh Kumar, Priya Sharma, or Arjun Nair)
  2. Click "Create Conversation" button
  3. See success alert

Result:
  - Conversation ID generated
  - Message containers now ready for input
  - Empty state messages disappear

STEP 4: Send Scammer Message
─────────────────────────────
Action:
  1. Click in message textarea (at bottom of sidebar)
  2. Type scammer message, e.g.:
     "Your account is compromised. Send UPI ID for verification."
  3. Click "Send" button

Result:
  - "Sending..." loader appears on button
  - After 1-2 seconds:
    * Red message appears (scammer)
    * Green message appears (victim's AI response)
    * Button returns to normal
    * Metrics update
    * Scam detection results show in Detection tab
    * Entities appear in Entities tab

STEP 5: View Analysis
─────────────────────
Detection Tab:
  - Scam Type: Shows detected type (phishing_upi, phishing_banking, etc.)
  - Confidence: Shows 0-100%
  - Keywords: Shows detected malicious words

Entities Tab:
  - Shows extracted information (UPI, phone, email, links)
  - Each has confidence percentage
  - Color-coded badges

Metrics Tab:
  - Total messages: Increments with each exchange
  - Total entities: Grows as new intelligence found
  - Average confidence: Shows overall detection strength
  - Current phase: Shows strategy stage (1-5)

STEP 6: Export Conversation
───────────────────────────
Action:
  Click "Export JSON" button (green)

Result:
  - File downloads: conversation_[ID].json
  - Contains full conversation history
  - Includes all detection results
  - Includes all extracted entities
  - Can be used for law enforcement

STEP 7: Delete Conversation
────────────────────────────
Action:
  1. Click "Delete" button (red)
  2. Confirm in popup dialog

Result:
  - Conversation removed from server
  - All panels reset to empty state
  - Ready to create new conversation

═══════════════════════════════════════════════════════════════════════════════
                        TEST SCENARIOS
═══════════════════════════════════════════════════════════════════════════════

SCENARIO 1: Banking Phishing
────────────────────────────
Persona: Rajesh Kumar (Retired Banker)
Message: "Sir, SBI detected fraudulent transactions. Verify your account details 
         urgently at https://verify-sbi-bank.com/confirm"
Expected Detection: phishing_banking
Expected Entities: Link (https://verify-sbi-bank.com/confirm)

SCENARIO 2: UPI Scam
────────────────────
Persona: Priya Sharma (Homemaker)
Message: "Madam, Google Play credit is available. Verify UPI at fraudster@upi.com 
         to claim your reward immediately"
Expected Detection: phishing_upi
Expected Entities: UPI ID (fraudster@upi.com)

SCENARIO 3: Lottery Scam
─────────────────────────
Persona: Arjun Nair (Business Owner)
Message: "Congratulations! You've won 10 lakhs in PowerBall lottery. Pay processing 
         fee of 2000 rupees to unlock."
Expected Detection: lottery_scam
Expected Entities: Amount (10 lakhs)

SCENARIO 4: Tech Support Scam
──────────────────────────────
Persona: Rajesh Kumar
Message: "WARNING: Your computer has virus. Call Microsoft support immediately at 
         +1-800-TECHSUPPORT to fix"
Expected Detection: tech_support
Expected Entities: Phone number, company name

SCENARIO 5: Investment Scam
────────────────────────────
Persona: Priya Sharma
Message: "Secret investment opportunity! 50% returns monthly guaranteed. 
         Send 50000 rupees to activate account."
Expected Detection: investment_scam
Expected Entities: Amount (50000)

═══════════════════════════════════════════════════════════════════════════════
                      KEYBOARD SHORTCUTS
═══════════════════════════════════════════════════════════════════════════════

While UI is focused:
  Tab         - Navigate between form elements
  Enter       - In message box, type Shift+Enter for new line, or just Enter to send
  Escape      - Cancel alert/dialog
  Ctrl+L      - Select address bar
  F12         - Open developer console (for debugging)

═══════════════════════════════════════════════════════════════════════════════
                      TROUBLESHOOTING UI ISSUES
═══════════════════════════════════════════════════════════════════════════════

Issue: Sidebar not visible
Solution: 
  - Check if you're on mobile (<768px width)
  - Sidebar hides on mobile
  - Messages still accessible in main area

Issue: Status shows "API Offline"
Solution:
  - Ensure API is running: python -m src.api
  - Check port 5000 is accessible
  - Refresh page (browser may have cached connection)

Issue: Buttons don't respond
Solution:
  - Clear browser cache (Ctrl+Shift+Delete)
  - Check JavaScript console for errors (F12)
  - Ensure advanced_ui.html is not cached

Issue: Messages don't appear
Solution:
  - Ensure conversation is created first
  - Check API responses in browser console (F12 → Network tab)
  - Verify message has text content

Issue: Animations choppy
Solution:
  - GPU acceleration might be off
  - Try different browser (Chrome, Firefox, Edge)
  - Check if hardware acceleration is enabled

═══════════════════════════════════════════════════════════════════════════════

This advanced UI provides a professional, modern interface for interacting with
your Agentic AI Honeypot system. All functionality is intuitive and visual.

For production deployment, simply update the API_BASE URL to your deployed server!

═══════════════════════════════════════════════════════════════════════════════
