# 📅 Interactive Schedule Tracker

A beautiful, interactive schedule tracker built with Streamlit. Track your daily routines, customize tasks, and access your schedule from any device!

## ✨ Features

- ✅ **Interactive Checkboxes** - Mark tasks complete
- ✏️ **Edit Mode** - Customize tasks with Google Calendar-style confirmations
- ➕ **Custom Time Slots** - Add 15-minute blocks or any custom time
- 📱 **Multi-Device Sync** - Access from phone, laptop, tablet
- 💾 **Auto-Save** - All changes saved to SQLite database
- 🌐 **12-Hour Format** - Shows 1:00 PM instead of 13:00
- 📊 **Export Data** - Download backup as JSON

## 🚀 Quick Deploy to Streamlit Cloud (FREE!)

### Step 1: Prepare Your Files

1. Create a new GitHub repository
2. Upload these files:
   - `streamlit_schedule_app.py`
   - `requirements.txt`
   - `README.md` (this file)

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file path: `streamlit_schedule_app.py`
6. Click "Deploy"!

Your app will be live at: `https://your-username-schedule-tracker.streamlit.app`

## 💻 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_schedule_app.py
```

Open your browser to `http://localhost:8501`

## 📖 How to Use

### Daily Tracking
1. Open your schedule URL
2. Check off tasks as you complete them ✅
3. Changes save automatically

### Editing Tasks
1. Click **"✏️ Edit Mode"**
2. Click on any task text to edit
3. Click **"💾"** save button
4. Choose:
   - **This day only** - Customize just that specific date
   - **All weekdays/Saturdays/Sundays** - Update your template

### Adding Custom Time Slots
1. Click **"➕ Add Time Slot"**
2. Enter time (e.g., `13:00` for 1:00 PM)
3. Choose which days (Weekdays/Saturdays/Sundays)
4. Enter task name and details
5. Click **"✅ Add"**

Example: Add a 15-minute break from 1:00-1:15 PM:
- Time: `13:00`
- Task: "Quick Break"
- Details: "15 min walk"

## 🎨 Customization

### Your Default Schedule

**Weekdays:**
- 7:00-9:00 AM: Morning routine (meditation, yoga, run, breakfast)
- 9:00 AM-5:00 PM: Work blocks with breaks
- 5:00-10:00 PM: Evening routine (dinner, walk, prep, wind-down)

**Saturdays:**
- 9:00 AM: Leisurely breakfast
- 10:00 AM-12:00 PM: Household tasks
- 1:00-6:00 PM: Adventure/Connection (rotates weekly)
- 7:00-11:00 PM: Hobby time & wind-down

**Sundays:**
- 9:00 AM: Slow breakfast
- 10:00 AM-1:00 PM: Growth & creation time
- 1:30-3:30 PM: Meal prep
- 3:30-5:00 PM: Weekly/monthly planning
- 7:00-10:00 PM: Family connection & prep

### Modify Defaults

Edit the `DEFAULT_WEEKDAY_SCHEDULE`, `DEFAULT_SATURDAY_SCHEDULE`, and `DEFAULT_SUNDAY_SCHEDULE` dictionaries in `streamlit_schedule_app.py`.

## 📊 Data Storage

All data is stored in a local SQLite database (`schedule.db`):
- **checkbox_states** - Your daily completions
- **custom_schedules** - Your template modifications
- **task_overrides** - Individual day customizations
- **custom_time_slots** - Your added time blocks

### Backup & Restore

Click **"💾 Export"** → **"📥 Download Backup"** to save your data as JSON.

To restore: Copy data from JSON and insert into database using SQLite browser.

## 🔧 Advanced Features

### Mobile Access
Your Streamlit app works great on phones! Bookmark it for quick access.

### Sharing
Share your Streamlit URL with family/friends if you want them to see your schedule.

### Custom Themes
Streamlit supports custom themes. Create a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

## 🐛 Troubleshooting

**Checkboxes not saving?**
- Check that the database file has write permissions
- Look for errors in the Streamlit console

**Schedule not loading?**
- Clear browser cache
- Check database file exists
- Verify no syntax errors in custom schedules

**Deployment issues?**
- Ensure `requirements.txt` is in repo root
- Check Streamlit Cloud logs for errors
- Verify Python version compatibility (3.8+)

## 📝 Future Enhancements

Ideas for additional features:
- [ ] Calendar export (.ics file)
- [ ] Email reminders
- [ ] Weekly analytics
- [ ] Habit streaks
- [ ] Multi-user accounts
- [ ] Dark mode
- [ ] Mobile app notifications

## 📄 License

MIT License - Feel free to customize and use for your personal scheduling needs!

## 💬 Support

Questions? Issues? Open an issue on GitHub or submit a pull request!

---

Built with ❤️ using [Streamlit](https://streamlit.io)
