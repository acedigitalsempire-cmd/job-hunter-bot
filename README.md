# 🎯 Job Hunter Bot — Daily Remote Job Alerts

This bot automatically finds **remote customer support jobs** every day and emails them to you.  
It runs at **10AM Nigeria Time** daily — completely free, no server needed.

---

## 📬 What You'll Receive

A daily email with a table of fresh remote jobs including:
- Job title & company
- Location
- Direct apply link
- Keywords & required skills

---

## 🚀 Setup Guide (Step-by-Step — No Coding Needed)

### STEP 1 — Create a GitHub Account
1. Go to [https://github.com](https://github.com)
2. Click **Sign Up** and create a free account
3. Verify your email

---

### STEP 2 — Create a New Repository (Project Folder)
1. After logging in, click the **+** button (top right) → **New repository**
2. Name it: `job-hunter-bot`
3. Make sure it's set to **Public**
4. Click **Create repository**

---

### STEP 3 — Upload These Files
1. On your new repo page, click **uploading an existing file**
2. Drag and drop ALL the files from this folder (keep the folder structure)
3. Click **Commit changes**

> ⚠️ Make sure the `.github/workflows/daily_jobs.yml` file is inside the correct folders.

---

### STEP 4 — Get a Gmail App Password

> This is a special password just for this bot. It is NOT your normal Gmail password.

1. Go to your Gmail → Click your profile photo → **Manage your Google Account**
2. Click the **Security** tab
3. Turn on **2-Step Verification** (if not already on)
4. Search for **App passwords** in the search bar
5. Select **Mail** and **Windows Computer** (or any device)
6. Click **Generate** — copy the 16-character password shown

---

### STEP 5 — Add Your Secrets to GitHub
1. Go to your GitHub repo
2. Click **Settings** (top menu)
3. On the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret** and add these one by one:

| Secret Name | Value |
|---|---|
| `EMAIL_USER` | Your Gmail address (e.g. yourname@gmail.com) |
| `EMAIL_PASS` | The 16-character App Password from Step 4 |
| `RECEIVER_EMAIL` | jobhauntgithub@gmail.com |

---

### STEP 6 — Run It Manually to Test
1. Go to your repo → Click **Actions** tab
2. Click **Daily Remote Customer Support Jobs** on the left
3. Click **Run workflow** → **Run workflow** (green button)
4. Wait 1–2 minutes → Check your email inbox!

---

## ⏰ Schedule

The bot runs automatically every day at **10:00 AM Nigeria Time (WAT)**.  
You don't need to do anything — just check your email daily!

---

## 🔧 Customization

To change the job keywords, open `config.py` and edit the `KEYWORDS` list.

---

## ❓ Troubleshooting

- **No email received?** Check your spam folder.
- **Workflow failed?** Check the Actions tab for error logs.
- **App password not working?** Make sure 2-Step Verification is enabled first.
