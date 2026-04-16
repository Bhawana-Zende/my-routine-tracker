import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import sqlite3
from pathlib import Path

# Page config
st.set_page_config(
    page_title="My Schedule Tracker",
    page_icon="📅",
    layout="wide"
)

# Database setup
DB_FILE = "schedule.db"

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Table for checkbox states
    c.execute('''CREATE TABLE IF NOT EXISTS checkbox_states
                 (date TEXT, time TEXT, checked INTEGER, PRIMARY KEY (date, time))''')
    
    # Table for custom schedules
    c.execute('''CREATE TABLE IF NOT EXISTS custom_schedules
                 (schedule_type TEXT, time TEXT, task TEXT, detail TEXT, period TEXT,
                  PRIMARY KEY (schedule_type, time))''')
    
    # Table for task overrides (individual day customizations)
    c.execute('''CREATE TABLE IF NOT EXISTS task_overrides
                 (date TEXT, time TEXT, task TEXT, detail TEXT, period TEXT,
                  PRIMARY KEY (date, time))''')
    
    # Table for custom time slots
    c.execute('''CREATE TABLE IF NOT EXISTS custom_time_slots
                 (time TEXT PRIMARY KEY, display_order INTEGER)''')
    
    conn.commit()
    conn.close()

def get_checkbox_state(date, time):
    """Get checkbox state from database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT checked FROM checkbox_states WHERE date=? AND time=?", (date, time))
    result = c.fetchone()
    conn.close()
    return bool(result[0]) if result else False

def set_checkbox_state(date, time, checked):
    """Set checkbox state in database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO checkbox_states (date, time, checked) VALUES (?, ?, ?)",
              (date, time, int(checked)))
    conn.commit()
    conn.close()

def get_custom_schedule(schedule_type):
    """Get custom schedule from database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT time, task, detail, period FROM custom_schedules WHERE schedule_type=?",
              (schedule_type,))
    results = c.fetchall()
    conn.close()
    
    schedule = {}
    for time, task, detail, period in results:
        schedule[time] = {'task': task, 'detail': detail, 'period': period}
    return schedule

def save_custom_schedule(schedule_type, time, task, detail, period):
    """Save custom schedule to database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO custom_schedules 
                 (schedule_type, time, task, detail, period) VALUES (?, ?, ?, ?, ?)""",
              (schedule_type, time, task, detail, period))
    conn.commit()
    conn.close()

def get_task_override(date, time):
    """Get task override for specific date/time"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT task, detail, period FROM task_overrides WHERE date=? AND time=?",
              (date, time))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {'task': result[0], 'detail': result[1], 'period': result[2]}
    return None

def save_task_override(date, time, task, detail, period):
    """Save task override for specific date/time"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO task_overrides 
                 (date, time, task, detail, period) VALUES (?, ?, ?, ?, ?)""",
              (date, time, task, detail, period))
    conn.commit()
    conn.close()

def get_custom_time_slots():
    """Get custom time slots from database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT time FROM custom_time_slots ORDER BY display_order")
    results = c.fetchall()
    conn.close()
    return [r[0] for r in results]

def add_custom_time_slot(time, display_order):
    """Add a custom time slot"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO custom_time_slots (time, display_order) VALUES (?, ?)",
              (time, display_order))
    conn.commit()
    conn.close()

# Default schedules
DEFAULT_WEEKDAY_SCHEDULE = {
    '7:00': {'period': 'morning', 'task': 'Morning Launch Begins', 'detail': 'Meditation (10-15 min)'},
    '7:30': {'period': 'morning', 'task': '10 Surya Namaskar', 'detail': '15 min yoga sequence'},
    '8:00': {'period': 'morning', 'task': 'Run/Walk + Shower', 'detail': '2k steps, shower & dress'},
    '8:30': {'period': 'morning', 'task': 'Breakfast', 'detail': 'Ready for work by 9 AM'},
    '9:00': {'period': 'work', 'task': 'Deep Work #1', 'detail': 'Focus time'},
    '9:30': {'period': 'work', 'task': 'Deep Work #1', 'detail': ''},
    '10:00': {'period': 'work', 'task': 'Deep Work #1', 'detail': '5-min movement break'},
    '10:30': {'period': 'work', 'task': 'Juice Break', 'detail': 'Social Reply Block #1'},
    '11:00': {'period': 'work', 'task': 'Deep Work #2', 'detail': 'Movement break if possible'},
    '11:30': {'period': 'work', 'task': 'Deep Work #2', 'detail': ''},
    '12:00': {'period': 'work', 'task': 'Deep Work #2', 'detail': 'Movement break if possible'},
    '12:30': {'period': 'work', 'task': 'Lunch', 'detail': 'Eat for 30 min'},
    '13:00': {'period': 'work', 'task': 'Active Reset', 'detail': '15-min tidy + 15-min walk + audiobook'},
    '13:30': {'period': 'work', 'task': 'Afternoon Work', 'detail': ''},
    '14:00': {'period': 'work', 'task': 'Afternoon Work', 'detail': 'Movement break at 2 PM'},
    '14:30': {'period': 'work', 'task': 'Afternoon Work', 'detail': ''},
    '15:00': {'period': 'work', 'task': 'Afternoon Work', 'detail': 'Movement break at 3 PM'},
    '15:30': {'period': 'work', 'task': 'Afternoon Work', 'detail': ''},
    '16:00': {'period': 'work', 'task': 'Afternoon Work', 'detail': 'Movement break at 4 PM'},
    '16:30': {'period': 'work', 'task': 'Afternoon Work', 'detail': ''},
    '17:00': {'period': 'evening', 'task': 'Post-Work Buffer', 'detail': 'Transition from work mode'},
    '17:30': {'period': 'evening', 'task': 'Buffer Time', 'detail': ''},
    '18:00': {'period': 'evening', 'task': 'Dinner', 'detail': '30 min meal'},
    '18:30': {'period': 'evening', 'task': 'Kitchen Cleanup', 'detail': '15 min - dishes'},
    '19:00': {'period': 'evening', 'task': 'Post-Dinner Walk', 'detail': 'Time with boyfriend (45 min)'},
    '19:30': {'period': 'evening', 'task': 'Social Replies', 'detail': 'Messages, food prep, tidy, calls'},
    '20:00': {'period': 'evening', 'task': 'Tomorrow Prep', 'detail': 'Learning course, journaling'},
    '20:30': {'period': 'evening', 'task': 'Flexible Time', 'detail': 'Any important tasks'},
    '21:00': {'period': 'evening', 'task': 'Flexible Time', 'detail': ''},
    '21:15': {'period': 'night', 'task': 'Read Book', 'detail': '30 min reading'},
    '21:45': {'period': 'night', 'task': 'Skincare', 'detail': '15 min routine'},
    '22:00': {'period': 'night', 'task': '🌙 Bedtime', 'detail': 'Lights out'}
}

DEFAULT_SATURDAY_SCHEDULE = {
    '9:00': {'period': 'saturday', 'task': '😴 Leisurely Breakfast', 'detail': 'Sleep in - no rush!'},
    '9:30': {'period': 'saturday', 'task': '😴 Leisurely Breakfast', 'detail': ''},
    '10:00': {'period': 'saturday', 'task': '🏠 Household Block', 'detail': 'Groceries + Laundry + Cleaning'},
    '10:30': {'period': 'saturday', 'task': '🏠 Household Block', 'detail': ''},
    '11:00': {'period': 'saturday', 'task': '🏠 Household Block', 'detail': ''},
    '11:30': {'period': 'saturday', 'task': '🏠 Household Block', 'detail': ''},
    '12:00': {'period': 'saturday', 'task': '🍽️ Lunch', 'detail': ''},
    '12:30': {'period': 'saturday', 'task': '🍽️ Lunch', 'detail': ''},
    '13:00': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': 'See weekly rotation'},
    '13:30': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': ''},
    '14:00': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': ''},
    '14:30': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': ''},
    '15:00': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': ''},
    '15:30': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': ''},
    '16:00': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': ''},
    '16:30': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': ''},
    '17:00': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': ''},
    '17:30': {'period': 'saturday', 'task': '✨ Adventure/Connection', 'detail': ''},
    '18:00': {'period': 'saturday', 'task': '🍽️ Dinner', 'detail': ''},
    '18:30': {'period': 'saturday', 'task': '🍽️ Dinner', 'detail': ''},
    '19:00': {'period': 'saturday', 'task': '🎮 Hobby/Play Time', 'detail': 'When desired - optional'},
    '19:30': {'period': 'saturday', 'task': '🎮 Hobby/Play Time', 'detail': ''},
    '20:00': {'period': 'saturday', 'task': '🎮 Hobby/Play Time', 'detail': ''},
    '20:30': {'period': 'saturday', 'task': '🎮 Hobby/Play Time', 'detail': ''},
    '21:00': {'period': 'saturday', 'task': '🌙 Free Wind-Down', 'detail': ''},
    '21:30': {'period': 'saturday', 'task': '🌙 Free Wind-Down', 'detail': ''},
    '22:00': {'period': 'saturday', 'task': '🌙 Free Wind-Down', 'detail': ''},
    '22:30': {'period': 'saturday', 'task': '🌙 Free Wind-Down', 'detail': ''}
}

DEFAULT_SUNDAY_SCHEDULE = {
    '9:00': {'period': 'sunday', 'task': '☕ Slow Breakfast', 'detail': 'Coffee time - no rush'},
    '9:30': {'period': 'sunday', 'task': '☕ Slow Breakfast', 'detail': ''},
    '10:00': {'period': 'sunday', 'task': '📚 Growth & Creation', 'detail': 'Learning, skill-building, writing'},
    '10:30': {'period': 'sunday', 'task': '📚 Growth & Creation', 'detail': ''},
    '11:00': {'period': 'sunday', 'task': '📚 Growth & Creation', 'detail': ''},
    '11:30': {'period': 'sunday', 'task': '📚 Growth & Creation', 'detail': ''},
    '12:00': {'period': 'sunday', 'task': '📚 Growth & Creation', 'detail': ''},
    '12:30': {'period': 'sunday', 'task': '📚 Growth & Creation', 'detail': ''},
    '13:00': {'period': 'sunday', 'task': '🍽️ Lunch', 'detail': ''},
    '13:30': {'period': 'sunday', 'task': '👨\u200d🍳 Meal Prep Together', 'detail': '2 hours with boyfriend'},
    '14:00': {'period': 'sunday', 'task': '👨\u200d🍳 Meal Prep Together', 'detail': ''},
    '14:30': {'period': 'sunday', 'task': '👨\u200d🍳 Meal Prep Together', 'detail': ''},
    '15:00': {'period': 'sunday', 'task': '👨\u200d🍳 Meal Prep Together', 'detail': ''},
    '15:30': {'period': 'sunday', 'task': '📋 Weekly/Monthly Planning', 'detail': 'See rotation notes'},
    '16:00': {'period': 'sunday', 'task': '📋 Planning', 'detail': ''},
    '16:30': {'period': 'sunday', 'task': '📋 Planning', 'detail': ''},
    '17:00': {'period': 'sunday', 'task': '⏸️ Buffer Time', 'detail': ''},
    '17:30': {'period': 'sunday', 'task': '⏸️ Buffer Time', 'detail': ''},
    '18:00': {'period': 'sunday', 'task': '🍽️ Dinner', 'detail': ''},
    '18:30': {'period': 'sunday', 'task': '🍽️ Dinner', 'detail': ''},
    '19:00': {'period': 'sunday', 'task': '👨\u200d👩\u200d👧\u200d👦 Family Connection', 'detail': 'Parent calls, video chats'},
    '19:30': {'period': 'sunday', 'task': '👨\u200d👩\u200d👧\u200d👦 Family Connection', 'detail': ''},
    '20:00': {'period': 'sunday', 'task': '🌙 Wind Down', 'detail': 'Prep for Monday'},
    '20:30': {'period': 'sunday', 'task': '🌙 Wind Down', 'detail': ''},
    '21:00': {'period': 'sunday', 'task': '🌙 Wind Down', 'detail': ''},
    '21:30': {'period': 'sunday', 'task': '🌙 Wind Down', 'detail': ''},
    '22:00': {'period': 'sunday', 'task': '🌙 Bedtime', 'detail': ''}
}

def format_time_12hr(time_24hr):
    """Convert 24hr time to 12hr AM/PM format"""
    try:
        hours, minutes = map(int, time_24hr.split(':'))
        period = 'AM' if hours < 12 else 'PM'
        hours_12 = hours % 12 if hours % 12 != 0 else 12
        return f"{hours_12}:{minutes:02d} {period}"
    except:
        return time_24hr

def get_week_of_month(date):
    """Get week number within the month (1-4)"""
    first_day = date.replace(day=1)
    day_of_month = date.day
    first_weekday = first_day.weekday()
    adjusted_day = day_of_month + first_weekday - 1
    return min(adjusted_day // 7 + 1, 4)

def get_schedule_for_day(date, custom_weekday, custom_saturday, custom_sunday):
    """Get the schedule for a specific day"""
    day_of_week = date.weekday()  # 0=Monday, 6=Sunday
    
    if day_of_week == 5:  # Saturday
        return custom_saturday if custom_saturday else DEFAULT_SATURDAY_SCHEDULE
    elif day_of_week == 6:  # Sunday
        return custom_sunday if custom_sunday else DEFAULT_SUNDAY_SCHEDULE
    else:  # Weekday
        return custom_weekday if custom_weekday else DEFAULT_WEEKDAY_SCHEDULE

# Initialize database
init_db()

# Initialize session state
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

# Load custom schedules
custom_weekday = get_custom_schedule('weekday')
custom_saturday = get_custom_schedule('saturday')
custom_sunday = get_custom_schedule('sunday')

# Title and controls
st.title("📅 My Interactive Schedule")
st.caption("April 16 - May 16, 2026 | Track your daily tasks")

# Control buttons
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    if st.button("✏️ Edit Mode" if not st.session_state.edit_mode else "💾 View Mode"):
        st.session_state.edit_mode = not st.session_state.edit_mode
        st.rerun()

with col2:
    if st.button("➕ Add Time Slot"):
        st.session_state.show_add_time_modal = True

with col3:
    if st.button("🔄 Reset"):
        # Clear custom schedules
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM custom_schedules")
        conn.commit()
        conn.close()
        st.success("Reset to defaults!")
        st.rerun()

with col4:
    if st.button("⬜ Clear Checks"):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM checkbox_states")
        conn.commit()
        conn.close()
        st.success("Cleared all checkboxes!")
        st.rerun()

with col5:
    if st.button("💾 Export"):
        # Export data as JSON
        conn = sqlite3.connect(DB_FILE)
        data = {
            'checkboxes': pd.read_sql("SELECT * FROM checkbox_states", conn).to_dict('records'),
            'custom_schedules': pd.read_sql("SELECT * FROM custom_schedules", conn).to_dict('records'),
            'task_overrides': pd.read_sql("SELECT * FROM task_overrides", conn).to_dict('records'),
        }
        conn.close()
        
        st.download_button(
            "📥 Download Backup",
            data=json.dumps(data, indent=2),
            file_name=f"schedule_backup_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# Add Time Slot Modal
if st.session_state.get('show_add_time_modal'):
    with st.expander("➕ Add Custom Time Slot", expanded=True):
        st.write("Add a custom time block (e.g., 13:00-13:15 for a 15-min break)")
        
        col_a, col_b = st.columns(2)
        with col_a:
            new_time = st.text_input("Time (HH:MM format)", "13:00", key="new_time_input")
        with col_b:
            day_type = st.selectbox("Apply to", ["Weekdays", "Saturdays", "Sundays"], key="day_type_select")
        
        task_name = st.text_input("Task Name", "New Task", key="task_name_input")
        task_detail = st.text_input("Details (optional)", "", key="task_detail_input")
        
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button("✅ Add"):
                schedule_type = day_type.lower()[:-1] if day_type != "Weekdays" else "weekday"
                period_map = {"weekday": "work", "saturday": "saturday", "sunday": "sunday"}
                save_custom_schedule(schedule_type, new_time, task_name, task_detail, period_map[schedule_type])
                st.session_state.show_add_time_modal = False
                st.success(f"Added {new_time} to {day_type}!")
                st.rerun()
        
        with col_y:
            if st.button("❌ Cancel"):
                st.session_state.show_add_time_modal = False
                st.rerun()

st.divider()

# Generate dates
start_date = datetime(2026, 4, 16)
end_date = datetime(2026, 5, 16)
dates = []
current = start_date
while current <= end_date:
    dates.append(current)
    current += timedelta(days=1)

# Show dates in columns (7 days per row for week view)
st.subheader("📆 Your Schedule")

# Week view
for week_start_idx in range(0, len(dates), 7):
    week_dates = dates[week_start_idx:week_start_idx + 7]
    
    # Day headers
    cols = st.columns(len(week_dates))
    for idx, date in enumerate(week_dates):
        with cols[idx]:
            day_name = date.strftime("%a")
            date_str = date.strftime("%b %d")
            st.markdown(f"**{day_name}**<br>{date_str}", unsafe_allow_html=True)
    
    # Get all time slots for this week
    all_times = set()
    for date in week_dates:
        schedule = get_schedule_for_day(date, custom_weekday, custom_saturday, custom_sunday)
        all_times.update(schedule.keys())
    
    # Sort times
    sorted_times = sorted(all_times, key=lambda t: tuple(map(int, t.split(':'))))
    
    # Display each time slot
    for time in sorted_times:
        cols = st.columns(len(week_dates))
        
        for idx, date in enumerate(week_dates):
            with cols[idx]:
                date_str = date.strftime("%Y-%m-%d")
                schedule = get_schedule_for_day(date, custom_weekday, custom_saturday, custom_sunday)
                
                # Check for override first
                override = get_task_override(date_str, time)
                task_data = override if override else schedule.get(time)
                
                if task_data:
                    # Checkbox
                    checked = get_checkbox_state(date_str, time)
                    new_checked = st.checkbox(
                        f"{format_time_12hr(time)}",
                        value=checked,
                        key=f"check_{date_str}_{time}",
                        label_visibility="visible"
                    )
                    
                    if new_checked != checked:
                        set_checkbox_state(date_str, time, new_checked)
                    
                    # Task display or edit
                    task_style = "text-decoration: line-through; opacity: 0.6;" if new_checked else ""
                    
                    if st.session_state.edit_mode:
                        new_task = st.text_input(
                            "Task",
                            value=task_data['task'],
                            key=f"task_{date_str}_{time}",
                            label_visibility="collapsed"
                        )
                        
                        if task_data.get('detail'):
                            new_detail = st.text_input(
                                "Detail",
                                value=task_data['detail'],
                                key=f"detail_{date_str}_{time}",
                                label_visibility="collapsed"
                            )
                        else:
                            new_detail = task_data.get('detail', '')
                        
                        # Save button
                        if st.button("💾", key=f"save_{date_str}_{time}"):
                            # Ask if apply to all or this day only
                            st.session_state[f'edit_pending_{date_str}_{time}'] = {
                                'task': new_task,
                                'detail': new_detail,
                                'period': task_data['period']
                            }
                    else:
                        st.markdown(f'<p style="{task_style}"><strong>{task_data["task"]}</strong></p>', unsafe_allow_html=True)
                        if task_data.get('detail'):
                            st.markdown(f'<p style="{task_style}; font-size: 0.8em; color: #666;">{task_data["detail"]}</p>', unsafe_allow_html=True)
                else:
                    st.write("")
        
        st.divider()
    
    st.markdown("---")

# Footer
st.caption("💡 Tip: Enable Edit Mode to customize tasks. Changes sync across all devices!")
