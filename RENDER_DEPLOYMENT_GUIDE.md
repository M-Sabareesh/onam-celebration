# 🚀 Render Deployment Guide - Data Persistence Setup

## 🎯 **Quick Setup (No Commands Needed)**

Since Render only allows one start command, here's the **simplest approach**:

### **Option 1: Use Pre-Built Data (Fastest) ⚡**

1. **Upload Pre-Built Data to GitHub:**
   ```bash
   # The data_backup/ folder is already created with sample questions/events
   # Just upload it to GitHub!
   ```

2. **Create GitHub Repository:**
   - Create: `onam-celebration-data` (public repository)
   - Upload the `data_backup/` folder from your project

3. **Set Render Environment Variable:**
   ```
   GITHUB_BACKUP_BASE_URL=https://raw.githubusercontent.com/YOUR_USERNAME/onam-celebration-data/main/data_backup/
   ```

4. **Set Render Start Command:**
   ```bash
   ./start.sh
   ```

5. **Done!** ✅ Your app will auto-restore data on startup.

---

### **Option 2: Manual Backup When Needed 📋**

When you want to create fresh backups:

1. **Run Locally:**
   ```bash
   # Make executable
   chmod +x backup_to_github.sh
   
   # Run backup
   ./backup_to_github.sh
   ```

2. **Upload to GitHub:**
   - The script will create `data_backup/` folder
   - Upload contents to your `onam-celebration-data` repository

3. **Render Auto-Restores:**
   - Your `start.sh` script automatically downloads data
   - No additional commands needed on Render

---

### **Option 3: GitHub Actions (Automated) 🤖**

For automatic backups when you push code:

1. **Setup GitHub Secrets:**
   - `DJANGO_SECRET_KEY`: Your secret key
   - `DATA_REPO_TOKEN`: Personal access token for data repo

2. **Push to Main Branch:**
   - GitHub Action runs automatically
   - Creates backup and updates data repository
   - Render pulls fresh data on next deployment

---

## ⚙️ **Render Configuration**

### **Environment Variables:**
```bash
# Required
GITHUB_BACKUP_BASE_URL=https://raw.githubusercontent.com/YOUR_USERNAME/onam-celebration-data/main/data_backup/

# Optional
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=your_secure_password
AUTO_RESTORE_DATA=True
```

### **Start Command:**
```bash
./start.sh
```

### **Build Command (if any):**
```bash
pip install -r requirements.txt
```

---

## 🔄 **How It Works**

1. **App Starts on Render** → `start.sh` runs
2. **Checks Database** → If empty, downloads from GitHub
3. **Restores Questions/Events** → Core structure ready
4. **Players Register Fresh** → Clean start each session
5. **App Ready** → Full functionality restored!

---

## 📁 **GitHub Repository Structure**

**Main Repository (onam-celebration):**
```
onam-celebration/
├── start.sh                 # ← Your start command
├── backup_to_github.sh      # ← Manual backup script
├── data_backup/             # ← Pre-built data
│   ├── questions.json
│   ├── events.json
│   └── backup_info.json
└── apps/core/management/commands/
    ├── backup_data.py       # ← Backup command
    └── restore_data.py      # ← Restore command
```

**Data Repository (onam-celebration-data):**
```
onam-celebration-data/
└── data_backup/
    ├── questions.json       # ← Questions for treasure hunt
    ├── events.json         # ← Events for competitions
    └── backup_info.json    # ← Backup metadata
```

---

## 🎉 **Benefits**

✅ **One Command Only** - Just `./start.sh` on Render  
✅ **Auto-Restore** - Data loads automatically  
✅ **No Manual Work** - Set once, works forever  
✅ **Fresh Sessions** - Players get clean start  
✅ **Persistent Structure** - Questions/events always available  
✅ **Free Solution** - GitHub + Render free tiers  

---

## 🐛 **Troubleshooting**

### **If Data Doesn't Restore:**
1. Check GitHub URL is public and correct
2. Verify `data_backup/` folder exists in GitHub repo
3. Check Render logs for error messages
4. App will create default questions as fallback

### **If Start Command Fails:**
1. Make sure `start.sh` is executable: `chmod +x start.sh`
2. Check file exists in repository root
3. Verify script syntax is correct

### **Test Locally:**
```bash
# Test restore command
python manage.py restore_data --github-base-url=https://raw.githubusercontent.com/YOUR_USERNAME/onam-celebration-data/main/data_backup/ --structure-only

# Test backup command
python manage.py backup_data --output-dir=test_backup
```

---

## 🎯 **Recommended Workflow**

1. **Development:** Add new questions locally
2. **Backup:** Run `./backup_to_github.sh` 
3. **Upload:** Push to `onam-celebration-data` repository
4. **Deploy:** Render automatically uses new data
5. **Enjoy:** Fresh Onam celebration every startup! 🎊

This approach gives you persistent data with zero additional commands on Render!
