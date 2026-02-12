from flask import Flask, render_template_string, request, redirect, url_for, flash, session, send_from_directory
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'DECR_secret_key_2026_driveeasy'

# --------- Database connection ----------
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="decr"
    )
except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")
    exit(1)

# --------- Serve static files ----------
@app.route('/static/<path:filename>')
def send_static_DECR(filename):
    return send_from_directory('.', filename)

# --------- Decorator ----------
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id_DECR' not in session:
            flash("Please log in first", "error")
            return redirect(url_for('home_DECR'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# --------- Sorting and Binary Search ----------
def bubble_sort_DECR(cars_list):
    n = len(cars_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if cars_list[j]['rental_price_DECR'] > cars_list[j + 1]['rental_price_DECR']:
                cars_list[j], cars_list[j + 1] = cars_list[j + 1], cars_list[j]
    return cars_list

def selection_sort_DECR(cars_list):
    n = len(cars_list)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if cars_list[j]['rental_price_DECR'] < cars_list[min_index]['rental_price_DECR']:
                min_index = j
        cars_list[i], cars_list[min_index] = cars_list[min_index], cars_list[i]
    return cars_list

def binary_search_price_DECR(sorted_cars, target_price):
    low = 0
    high = len(sorted_cars) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_price = sorted_cars[mid]['rental_price_DECR']
        if mid_price == target_price:
            return sorted_cars[mid]
        elif mid_price < target_price:
            low = mid + 1
        else:
            high = mid - 1
    return None

# --------- SUPERIOR CHATBOT ----------
def smart_chatbot_DECR(message: str, cars_data: list = None, chat_history: list = None) -> str:
    """Production-grade chatbot with car data integration"""
    if not cars_data:
        return " Fleet data loading... Please refresh!"
    
    msg = message.lower().strip()
    total_cars = len(cars_data)
    available_cars = sum(1 for c in cars_data if c['availability_DECR'])
    avg_price = sum(c['rental_price_DECR'] for c in cars_data) / total_cars if total_cars else 0
    
    # Smart responses with real data
    responses = {
        # Stats & Analytics
        'stats': f" **Fleet Stats**: {total_cars} total cars | {available_cars} available | Avg: {avg_price:.1f}€",
        'price': f" **Price Range**: {min(c['rental_price_DECR'] for c in cars_data):.1f}€ - {max(c['rental_price_DECR'] for c in cars_data):.1f}€\nCheapest available: {min((c['rental_price_DECR'] for c in cars_data if c['availability_DECR']), default=0):.1f}€",
        'average': f" **Average rental price**: {avg_price:.1f}€ across {total_cars} cars",
        'available': f" **{available_cars}/{total_cars} cars available** ({available_cars/total_cars*100:.0f}%)",
        
        # Car management
        'add': " **Add Car**: Select 'Add new car' → Fill model/brand/price/availability → Submit",
        'update': " **Update**: Select 'Update existing car' → Enter Car ID → Change only needed fields",
        'delete': " **Delete**: Select 'Delete car' → Enter Car ID → Confirm (irreversible!)",
        
        # Search & Sort
        'search': " **Binary Search**: Enter exact € price in search box above. Uses Selection Sort + Binary Search algorithm!",
        'sort': " **Sorting**: Choose Bubble Sort or Selection Sort from dropdown. Both sort by rental_price_DECR!",
        
        # Brands (detect common brands)
        'toyota': " **Toyota**: Reliable choice! Typically 35-60€/day. Fuel efficient family cars.",
        'bmw': " **BMW**: Premium luxury. 80-150€/day. Performance driving experience.",
        'mercedes': " **Mercedes**: Executive class. 90-200€/day. Ultimate comfort.",
        'audi': " **Audi**: Sporty premium. 85-160€/day. Quattro all-wheel drive.",
        
        # Help
        'help': """ **DriveEasy AI Assistant Commands**:
• `stats` - Fleet statistics
• `price` - Price range & cheapest
• `average` - Average rental price  
• `add`/`update`/`delete` - Car management
• `toyota`/`bmw`/etc - Brand info
• `help` - This menu
• Brand names work too! """,
        
        # Fallback
        'default': f" **Try these**: `stats` `price` `average` `add car` `help`\n\n Quick stats: {available_cars}/{total_cars} available @ {avg_price:.0f}€ avg"
    }
    
    # Match patterns (most specific first)
    patterns = [
        ('stats|total|count|how many', 'stats'),
        ('price|cost|€|euro|money', 'price'),
        ('average|avg|mean', 'average'),
        ('available|free|open', 'available'),
        ('add|create|new', 'add'),
        ('update|change|edit|modify', 'update'),
        ('delete|remove|trash', 'delete'),
        ('search|find|look', 'search'),
        ('sort|bubble|selection', 'sort'),
        ('toyota|corolla', 'toyota'),
        ('bmw', 'bmw'),
        ('mercedes|benz', 'mercedes'),
        ('audi', 'audi'),
        ('help|commands|what can you', 'help')
    ]
    
    for pattern, response_key in patterns:
        if any(word in msg for word in pattern.split('|')):
            return responses[response_key]
    
    # Brand detection fallback
    brands = ['toyota', 'bmw', 'mercedes', 'audi', 'ford', 'honda', 'volkswagen']
    for brand in brands:
        if brand in msg:
            return f"🚗 **{brand.upper()}**: Premium brand typically {50+brands.index(brand)*10:.0f}€+/day!"
    
    return responses['default']

# --------- HTML Templates (UPDATED WITH SUPERIOR CHAT) ----------
login_template_DECR = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DriveEasy Login</title>
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%); 
            color: #f1f5f9; 
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container { 
            width: 100%; 
            max-width: 420px; 
            background: rgba(15, 23, 42, 0.95); 
            padding: 40px; 
            border-radius: 24px; 
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
        }
        h1 { 
            text-align: center; 
            color: #6366f1; 
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 35px;
            letter-spacing: -0.5px;
        }
        label { 
            display: block; 
            margin: 25px 0 8px 0; 
            font-weight: 600;
            color: #cbd5e1;
            font-size: 15px;
        }
        input[type=text], input[type=password] {
            width: 100%; 
            padding: 16px 20px; 
            border-radius: 16px; 
            border: 2px solid rgba(99, 102, 241, 0.2); 
            background: rgba(30, 41, 59, 0.8); 
            color: #f1f5f9;
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        input:focus {
            outline: none;
            border-color: #6366f1;
            background: rgba(30, 41, 59, 1);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
            transform: translateY(-1px);
        }
        input::placeholder { color: #94a3b8; }
        button { 
            width: 100%; 
            margin-top: 30px; 
            padding: 18px; 
            background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%); 
            color: white; 
            border: none; 
            border-radius: 16px; 
            cursor: pointer; 
            font-weight: 600; 
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: relative;
            overflow: hidden;
        }
        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
        }
        button:active { transform: translateY(-1px); }
        a { 
            color: #a78bfa; 
            text-decoration: none; 
            font-weight: 500;
            transition: all 0.2s ease;
        }
        a:hover { color: #c4b5fd; text-decoration: underline; }
        .messages { margin-bottom: 25px; }
        .msg-error { color: #f87171 !important; background: rgba(248, 113, 113, 0.1); padding: 12px; border-radius: 12px; border-left: 4px solid #f87171; }
        .msg-success { color: #10b981 !important; background: rgba(16, 185, 129, 0.1); padding: 12px; border-radius: 12px; border-left: 4px solid #10b981; }
        .msg-info { color: #3b82f6 !important; background: rgba(59, 130, 246, 0.1); padding: 12px; border-radius: 12px; border-left: 4px solid #3b82f6; }
    </style>
</head>
<body>
<div class="container">
    <h1>DriveEasy Admin</h1>
    <div class="messages">
        {% with messages = get_flashed_messages(with_categories=true) %}
         {% if messages %}
           {% for category, message in messages %}
             <div class="msg-{{ category }}">{{ message }}</div>
           {% endfor %}
         {% endif %}
        {% endwith %}
    </div>
    <form method="POST" action="{{ url_for('login_DECR') }}">
        <label for="username_DECR">Username</label>
        <input type="text" id="username_DECR" name="username_DECR" required placeholder="Enter your username">
        <label for="password_DECR">Password</label>
        <input type="password" id="password_DECR" name="password_DECR" required placeholder="Enter your password">
        <button type="submit">Sign In</button>
    </form>
    <p style="margin-top:25px; text-align:center; font-size:14px;">
        No account? <a href="{{ url_for('signup_DECR') }}">Create one</a>
    </p>
</div>
</body>
</html>
"""



signup_template_DECR = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DriveEasy Signup</title>
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%); 
            color: #f1f5f9; 
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container { 
            width: 100%; 
            max-width: 450px; 
            background: rgba(15, 23, 42, 0.95); 
            padding: 40px; 
            border-radius: 24px; 
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
        }
        h1 { 
            text-align: center; 
            color: #6366f1; 
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 35px;
            letter-spacing: -0.5px;
        }
        label { 
            display: block; 
            margin: 25px 0 8px 0; 
            font-weight: 600;
            color: #cbd5e1;
            font-size: 15px;
        }
        input[type=text], input[type=password] {
            width: 100%; 
            padding: 16px 20px; 
            border-radius: 16px; 
            border: 2px solid rgba(99, 102, 241, 0.2); 
            background: rgba(30, 41, 59, 0.8); 
            color: #f1f5f9;
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        input:focus {
            outline: none;
            border-color: #6366f1;
            background: rgba(30, 41, 59, 1);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
            transform: translateY(-1px);
        }
        input::placeholder { color: #94a3b8; }
        button { 
            width: 100%; 
            margin-top: 30px; 
            padding: 18px; 
            background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%); 
            color: white; 
            border: none; 
            border-radius: 16px; 
            cursor: pointer; 
            font-weight: 600; 
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
        }
        a { 
            color: #a78bfa; 
            text-decoration: none; 
            font-weight: 500;
            transition: all 0.2s ease;
        }
        a:hover { color: #c4b5fd; text-decoration: underline; }
        .messages { margin-bottom: 25px; }
        .msg-error { color: #f87171 !important; background: rgba(248, 113, 113, 0.1); padding: 12px; border-radius: 12px; border-left: 4px solid #f87171; }
        .msg-success { color: #10b981 !important; background: rgba(16, 185, 129, 0.1); padding: 12px; border-radius: 12px; border-left: 4px solid #10b981; }
    </style>
</head>
<body>
<div class="container">
    <h1>Create Admin Account</h1>
    <div class="messages">
        {% with messages = get_flashed_messages(with_categories=true) %}
         {% if messages %}
           {% for category, message in messages %}
             <div class="msg-{{ category }}">{{ message }}</div>
           {% endfor %}
         {% endif %}
        {% endwith %}
    </div>
    <form method="POST" action="{{ url_for('signup_DECR') }}">
        <label for="username_DECR">Username</label>
        <input type="text" id="username_DECR" name="username_DECR" required placeholder="Enter username">
        <label for="full_name_DECR">Full name</label>
        <input type="text" id="full_name_DECR" name="full_name_DECR" required placeholder="John Doe">
        <label for="driving_license_number_DECR">Driving license number</label>
        <input type="text" id="driving_license_number_DECR" name="driving_license_number_DECR" required placeholder="DL12345678">
        <label for="password_DECR">Password</label>
        <input type="password" id="password_DECR" name="password_DECR" required placeholder="Enter secure password">
        <button type="submit">Create Account</button>
    </form>
    <p style="margin-top:25px; text-align:center; font-size:14px;">
        Already have account? <a href="{{ url_for('home_DECR') }}">Sign in</a>
    </p>
</div>
</body>
</html>
"""


cars_template_DECR = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DriveEasy Admin Panel</title>
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%); 
            color: #f1f5f9; 
            margin: 0; 
            min-height: 100vh;
        }
        header { 
            display: flex; 
            align-items: center; 
            justify-content: space-between; 
            padding: 20px 40px; 
            background: rgba(15, 23, 42, 0.95); 
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .brand { 
            display: flex; 
            align-items: center; 
            gap: 16px; 
        }
        .brand img { 
            height: 56px; 
            width: auto; 
            border-radius: 12px; 
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        }
        .brand-title { 
            font-size: 24px; 
            font-weight: 700; 
            background: linear-gradient(135deg, #6366f1, #818cf8); 
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        nav a { 
            color: #e2e8f0; 
            margin-left: 24px; 
            text-decoration: none; 
            font-weight: 500;
            padding: 10px 20px;
            border-radius: 12px;
            transition: all 0.3s ease;
            font-size: 14px;
        }
        nav a:hover { 
            color: #6366f1; 
            background: rgba(99, 102, 241, 0.1);
        }
        nav a.button { 
            background: linear-gradient(135deg, #6366f1, #818cf8); 
            color: white; 
            font-weight: 600; 
        }
        nav a.button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(99, 102, 241, 0.4);
        }
        .container { 
            max-width: 1400px; 
            margin: 40px auto; 
            padding: 0 40px 50px; 
        }
        table { 
            width: 100%; 
            border-collapse: separate; 
            border-spacing: 0;
            margin: 40px 0;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        th, td { 
            padding: 20px 24px; 
            text-align: left; 
            border-bottom: 1px solid rgba(71, 85, 105, 0.5);
        }
        th { 
            background: linear-gradient(135deg, #1e293b, #334155); 
            font-weight: 600;
            color: #6366f1;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 0.5px;
        }
        tr:nth-child(even) { background: rgba(34, 41, 59, 0.5); }
        tr:nth-child(odd) { background: rgba(30, 41, 59, 0.7); }
        tr:hover { 
            background: rgba(99, 102, 241, 0.2) !important;
            transform: scale(1.02);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .search-section {
            display: flex;
            flex-direction: column;
            gap: 25px;
            margin-bottom: 30px;
        }
        .search-card {
            background: rgba(30, 41, 59, 0.9);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(15px);
        }
        .search-card h3 {
            color: #6366f1;
            margin: 0 0 20px 0;
            font-size: 18px;
            font-weight: 600;
        }
        .search-card label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #cbd5e1;
            font-size: 15px;
        }
        .search-card input, .search-card select {
            width: 100%;
            padding: 18px 20px;
            border-radius: 16px;
            border: 2px solid rgba(99, 102, 241, 0.2);
            background: rgba(15, 23, 42, 0.8);
            color: #f1f5f9;
            font-size: 16px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }
        .search-card input:focus, .search-card select:focus {
            outline: none;
            border-color: #6366f1;
            background: rgba(15, 23, 42, 1);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
        }
        .search-card button {
            width: 100%;
            padding: 16px 24px;
            border: none;
            border-radius: 16px;
            background: linear-gradient(135deg, #6366f1, #818cf8);
            color: white;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .search-card button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(99, 102, 241, 0.4);
        }
        .messages { margin-bottom: 20px; text-align: center; }
        .msg-error { color: #f87171 !important; }
        .msg-success { color: #10b981 !important; }
        .msg-info { color: #3b82f6 !important; }
        .msg-warning { color: #f59e0b !important; }
        .row { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 40px; 
            margin-top: 50px; 
        }
        .card { 
            background: rgba(30, 41, 59, 0.9); 
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 24px; 
            padding: 30px; 
            backdrop-filter: blur(20px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            min-height: 600px;
        }
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 35px 70px rgba(0,0,0,0.4);
        }
        input[type=text], input[type=number], select {
            width: 100%; 
            padding: 16px 20px; 
            margin: 10px 0 20px 0;
            border-radius: 16px; 
            border: 2px solid rgba(99, 102, 241, 0.2); 
            background: rgba(15, 23, 42, 0.8); 
            color: #f1f5f9;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #6366f1;
            background: rgba(15, 23, 42, 1);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
        }
        button { 
            padding: 16px 32px; 
            border: none; 
            border-radius: 16px; 
            background: linear-gradient(135deg, #6366f1, #818cf8); 
            color: white; 
            cursor: pointer; 
            font-weight: 600; 
            transition: all 0.3s ease;
            width: 100%;
            font-size: 16px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        button:hover { 
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.4);
        }
        .chat-log { 
            max-height: 400px; 
            overflow-y: auto; 
            border: 1px solid rgba(255,255,255,0.1); 
            padding: 24px; 
            margin-bottom: 20px; 
            font-size: 15px; 
            background: rgba(15, 23, 42, 0.8); 
            border-radius: 16px;
            scrollbar-width: thin;
        }
        .chat-log::-webkit-scrollbar { width: 6px; }
        .chat-log::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
        .chat-log::-webkit-scrollbar-thumb { background: #6366f1; border-radius: 3px; }
        .chat-user { color: #60a5fa; font-weight: 600; }
        .chat-bot { color: #a78bfa; }
        .chat-time { color: #94a3b8; font-size: 13px; }
        .fleet-info { 
            font-size: 15px; 
            color: #60a5fa; 
            padding: 16px; 
            background: rgba(96, 165, 250, 0.15); 
            border-radius: 16px; 
            margin-bottom: 20px; 
            text-align: center;
            border: 1px solid rgba(96, 165, 250, 0.3);
            font-weight: 500;
        }
        @media (max-width: 1024px) {
            .row { grid-template-columns: 1fr; }
            .container { padding: 0 20px 30px; }
            header { padding: 20px; flex-direction: column; gap: 20px; text-align: center; }
            .search-section { gap: 20px; }
        }
    </style>
</head>
<body>
<header>
    <div class="brand">
        {% if header_data_DECR and header_data_DECR.logo_path_DECR %}
            <img src="/static/{{ header_data_DECR.logo_path_DECR }}" alt="Logo">
        {% endif %}
        <div class="brand-title">{{ header_data_DECR.company_name_DECR if header_data_DECR else 'DriveEasy Car Rental (DECR)' }}</div>
    </div>
    <nav>
        <span style="margin-right: 24px; color: #94a3b8;">👤 {{ session.username_DECR }}</span>
        <a href="{{ url_for('edit_header_DECR') }}">⚙️ Edit header</a>
        <a href="{{ url_for('logout_DECR') }}" class="button">🚪 Logout</a>
    </nav>
</header>
<div class="container">
    <div class="messages">
        {% with messages = get_flashed_messages(with_categories=true) %}
         {% if messages %}
           {% for category, message in messages %}
             <div class="msg-{{ category }}">{{ message }}</div>
           {% endfor %}
         {% endif %}
        {% endwith %}
    </div>

    <div class="search-section">
        <div class="search-card">
            <h3>🔄 Sort by rental price</h3>
            <form method="GET" action="{{ url_for('cars_DECR') }}">
                <label>Algorithm</label>
                <select name="sort_algorithm_DECR">
                    <option value="">SQL default</option>
                    <option value="bubble" {% if current_sort_algorithm_DECR == 'bubble' %}selected{% endif %}>Bubble Sort</option>
                    <option value="selection" {% if current_sort_algorithm_DECR == 'selection' %}selected{% endif %}>Selection Sort</option>
                </select>
                <button type="submit">Apply Sort</button>
            </form>
        </div>
        <div class="search-card">
            <h3>🔍 Binary search</h3>
            <form method="GET" action="{{ url_for('cars_DECR') }}">
                <label>Rental price (€ exact)</label>
                <input type="number" step="0.01" name="search_price_DECR" value="{{ search_price_DECR or '' }}" placeholder="e.g. 45.50">
                <button type="submit">Search</button>
            </form>
        </div>
    </div>

    {% if search_result_DECR %}
        <div style="background: rgba(16, 185, 129, 0.2); padding: 20px; border-radius: 16px; color: #10b981; border-left: 5px solid #10b981; margin: 20px 0; font-weight: 500;">
            🎉 Found! Car ID {{ search_result_DECR.car_id_DECR }}: {{ search_result_DECR.car_brand_DECR }} {{ search_result_DECR.car_model_DECR }} (€{{ '%.2f'|format(search_result_DECR.rental_price_DECR) }})
        </div>
    {% elif search_price_DECR %}
        <div style="background: rgba(248, 113, 113, 0.2); padding: 20px; border-radius: 16px; color: #f87171; border-left: 5px solid #f87171; margin: 20px 0; font-weight: 500;">
            ❌ No car found at exactly {{ search_price_DECR }}€
        </div>
    {% endif %}

    <table>
        <thead>
        <tr>
            <th>ID</th><th>Model</th><th>Brand</th><th>Price €</th><th>Status</th>
        </tr>
        </thead>
        <tbody>
        {% for car in cars_DECR %}
            <tr>
                <td>{{ car.car_id_DECR }}</td>
                <td>{{ car.car_model_DECR }}</td>
                <td>{{ car.car_brand_DECR }}</td>
                <td>€{{ '%.2f'|format(car.rental_price_DECR) }}</td>
                <td>{% if car.availability_DECR %}<span style="color:#10b981; font-weight: 600;">✅ Available</span>{% else %}<span style="color:#f87171; font-weight: 600;">❌ Unavailable</span>{% endif %}</td>
            </tr>
        {% else %}
            <tr><td colspan="5" style="text-align:center;color:#94a3b8;padding:50px; font-style: italic;">🚗 No cars found. Add some using the form below!</td></tr>
        {% endfor %}
        </tbody>
    </table>

    <div class="row">
        <div class="card">
            <h3 style="color: #6366f1; margin-bottom: 25px; font-size: 22px; font-weight: 700;">🔧 Manage Cars</h3>
            <form method="POST" action="{{ url_for('manage_car_DECR') }}">
                <label style="font-weight: 600; color: #cbd5e1; margin-bottom: 5px; display: block;">Action</label>
                <select name="action_DECR" required>
                    <option value="add">➕ Add new car</option>
                    <option value="update">✏️ Update existing car</option>
                    <option value="delete">🗑️ Delete car</option>
                </select>
                <label style="font-weight: 600; color: #cbd5e1; margin-bottom: 5px; display: block;">Car ID (for update/delete)</label>
                <input type="number" name="car_id_DECR">
                <label style="font-weight: 600; color: #cbd5e1; margin-bottom: 5px; display: block;">Model</label>
                <input type="text" name="car_model_DECR" placeholder="e.g. Corolla">
                <label style="font-weight: 600; color: #cbd5e1; margin-bottom: 5px; display: block;">Brand</label>
                <input type="text" name="car_brand_DECR" placeholder="e.g. Toyota">
                <label style="font-weight: 600; color: #cbd5e1; margin-bottom: 5px; display: block;">Rental price (€)</label>
                <input type="number" step="0.01" name="rental_price_DECR" placeholder="45.50">
                <label style="font-weight: 600; color: #cbd5e1; margin-bottom: 5px; display: block;">Availability (1=available, 0=unavailable)</label>
                <input type="number" min="0" max="1" name="availability_DECR">
                <button type="submit">Apply Changes</button>
            </form>
        </div>
        <div class="card">
            <h3 style="color: #6366f1; margin-bottom: 20px; font-size: 22px; font-weight: 700;">🤖 DriveEasy AI Assistant</h3>
            <div class="fleet-info">
                {{ cars_data_DECR|length if cars_data_DECR else 0 }} cars | 
                {{ (cars_data_DECR|selectattr('availability_DECR')|list|length) if cars_data_DECR else 0 }} available
            </div>
            <div class="chat-log" id="chatLog">
                {% for msg in chat_log_DECR %}
                    <div style="margin-bottom:16px;">
                    <span class="chat-{{ msg.role }}"> {{ msg.role|capitalize }}: </span>
                    <span>{{ msg.text }}</span>
                    <span class="chat-time">({{ msg.timestamp }})</span>
                    </div>
                {% endfor %}
            </div>
            <form method="POST" action="{{ url_for('chat_DECR') }}">
                <input type="text" name="chat_message_DECR" placeholder="💬 Try 'stats', 'price', 'help', 'Toyota'..." required autofocus>
                <button type="submit">Send 🚀</button>
            </form>
        </div>
    </div>
</div>
</body>
</html>
"""




edit_header_template_DECR = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Header</title>
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%); 
            color: #f1f5f9; 
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container { 
            width: 100%; 
            max-width: 500px; 
            background: rgba(15, 23, 42, 0.95); 
            backdrop-filter: blur(25px);
            padding: 50px; 
            border-radius: 28px; 
            box-shadow: 0 35px 70px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.1);
        }
        h2 { 
            color: #6366f1; 
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 40px;
            text-align: center;
            letter-spacing: -0.5px;
        }
        label { 
            display: block; 
            margin: 30px 0 12px 0; 
            font-weight: 600;
            color: #cbd5e1;
            font-size: 15px;
        }
        input[type=text] { 
            width: 100%; 
            padding: 20px 24px; 
            border-radius: 20px; 
            border: 2px solid rgba(99, 102, 241, 0.2); 
            background: rgba(30, 41, 59, 0.8); 
            color: #f1f5f9;
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        input:focus {
            outline: none;
            border-color: #6366f1;
            background: rgba(30, 41, 59, 1);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
            transform: translateY(-2px);
        }
        button { 
            margin-top: 35px; 
            padding: 20px 40px; 
            border: none; 
            border-radius: 20px; 
            background: linear-gradient(135deg, #6366f1, #818cf8); 
            color: white; 
            font-weight: 700; 
            cursor: pointer; 
            width: 100%;
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        button:hover { 
            transform: translateY(-4px);
            box-shadow: 0 25px 50px rgba(99, 102, 241, 0.4);
        }
        a { 
            display: inline-block;
            margin-top: 25px;
            color: #60a5fa; 
            text-decoration: none; 
            font-weight: 600;
            padding: 14px 32px;
            border-radius: 16px;
            border: 2px solid rgba(96, 165, 250, 0.3);
            transition: all 0.3s ease;
            width: 100%;
            text-align: center;
        }
        a:hover { 
            background: rgba(96, 165, 250, 0.15);
            color: #fff;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
<div class="container">
    <h2> Branding Settings</h2>
    <div class="messages" style="text-align: center; margin-bottom: 30px;">
        {% with messages = get_flashed_messages(with_categories=true) %}
         {% if messages %}
           {% for category, message in messages %}
             <div class="msg-{{ category }}">{{ message }}</div>
           {% endfor %}
         {% endif %}
        {% endwith %}
    </div>
    <form method="POST" action="{{ url_for('edit_header_DECR') }}">
        <label for="company_name_DECR">Company Name</label>
        <input type="text" id="company_name_DECR" name="company_name_DECR" value="{{ header_data_DECR.company_name_DECR if header_data_DECR else '' }}" required>
        <label for="logo_path_DECR">Logo Path</label>
        <input type="text" id="logo_path_DECR" name="logo_path_DECR" value="{{ header_data_DECR.logo_path_DECR if header_data_DECR else '' }}" placeholder="logo.png" required>
        <button type="submit">Save Branding</button>
        <a href="{{ url_for('cars_DECR') }}">← Back to Dashboard</a>
    </form>
</div>
</body>
</html>
"""

# --------- Routes ----------
@app.route('/')
def home_DECR():
    if 'user_id_DECR' in session:
        return redirect(url_for('cars_DECR'))
    return render_template_string(login_template_DECR)

@app.route('/signup', methods=['GET', 'POST'])
def signup_DECR():
    if request.method == 'GET':
        return render_template_string(signup_template_DECR)

    username_DECR = request.form.get('username_DECR', '').strip()
    full_name_DECR = request.form.get('full_name_DECR', '').strip()
    license_DECR = request.form.get('driving_license_number_DECR', '').strip()
    password_DECR = request.form.get('password_DECR', '')

    if not all([username_DECR, full_name_DECR, license_DECR, password_DECR]):
        flash("All fields are required", "error")
        return redirect(url_for('signup_DECR'))

    hashed = generate_password_hash(password_DECR)
    try:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Users_DECR (username_DECR, password_DECR, full_name_DECR, driving_license_number_DECR)
            VALUES (%s, %s, %s, %s)
        """, (username_DECR, hashed, full_name_DECR, license_DECR))
        db.commit()
        flash(" Account created successfully!", "success")
    except Exception as e:
        flash(f" Error: {str(e)}", "error")

    return redirect(url_for('home_DECR'))

@app.route('/login', methods=['POST'])
def login_DECR():
    username_DECR = request.form.get('username_DECR', '').strip()
    password_DECR = request.form.get('password_DECR', '')

    if not username_DECR or not password_DECR:
        flash("Please enter username and password", "error")
        return redirect(url_for('home_DECR'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users_DECR WHERE username_DECR = %s", (username_DECR,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password_DECR'], password_DECR):
        session['user_id_DECR'] = user['user_id_DECR']
        session['username_DECR'] = user['username_DECR']
        flash(" Welcome back!", "success")
        return redirect(url_for('cars_DECR'))
    else:
        flash(" Invalid credentials", "error")
        return redirect(url_for('home_DECR'))

@app.route('/logout')
def logout_DECR():
    session.clear()
    flash(" Logged out successfully", "info")
    return redirect(url_for('home_DECR'))

@app.route('/cars', methods=['GET'])
@login_required
def cars_DECR():
    sort_algorithm_DECR = request.args.get('sort_algorithm_DECR', '')
    search_price_raw = request.args.get('search_price_DECR')
    search_price_DECR = None
    search_result_DECR = None

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Header_data_DECR LIMIT 1")
    header_data_DECR = cursor.fetchone()

    cursor.execute("SELECT * FROM Cars_DECR")
    cars_DECR = cursor.fetchall()
    cars_data_DECR = cars_DECR.copy()  # For chatbot

    # Apply sorting
    if sort_algorithm_DECR == 'bubble':
        cars_DECR = bubble_sort_DECR(cars_DECR)
    elif sort_algorithm_DECR == 'selection':
        cars_DECR = selection_sort_DECR(cars_DECR)

    # Binary search
    if search_price_raw:
        try:
            search_price_DECR = float(search_price_raw)
            sorted_for_search = selection_sort_DECR([car.copy() for car in cars_data_DECR])
            search_result_DECR = binary_search_price_DECR(sorted_for_search, search_price_DECR)
        except ValueError:
            flash("Search price must be a valid number.", "error")

    # Enhanced chat log with timestamps
    chat_log_DECR = session.get('chat_log_DECR', [])
    from datetime import datetime
    for msg in chat_log_DECR:
        if 'timestamp' not in msg:
            msg['timestamp'] = datetime.now().strftime('%H:%M')

    return render_template_string(
        cars_template_DECR,
        cars_DECR=cars_DECR,
        header_data_DECR=header_data_DECR,
        current_sort_algorithm_DECR=sort_algorithm_DECR,
        search_price_DECR=search_price_DECR,
        search_result_DECR=search_result_DECR,
        chat_log_DECR=chat_log_DECR,
        cars_data_DECR=cars_data_DECR
    )

@app.route('/manage_car', methods=['POST'])
@login_required
def manage_car_DECR():
    action_DECR = request.form.get('action_DECR')
    car_id_DECR = request.form.get('car_id_DECR')
    model_DECR = request.form.get('car_model_DECR', '').strip()
    brand_DECR = request.form.get('car_brand_DECR', '').strip()
    price_raw = request.form.get('rental_price_DECR')
    availability_raw = request.form.get('availability_DECR')

    cursor = db.cursor()

    try:
        if action_DECR == 'add':
            if not all([model_DECR, brand_DECR, price_raw, availability_raw]):
                flash(" All fields required for new car", "error")
                return redirect(url_for('cars_DECR'))

            price = float(price_raw)
            availability = int(availability_raw)
            cursor.execute("""
                INSERT INTO Cars_DECR (car_model_DECR, car_brand_DECR, rental_price_DECR, availability_DECR)
                VALUES (%s, %s, %s, %s)
            """, (model_DECR, brand_DECR, price, availability))
            db.commit()
            flash(" Car added successfully!", "success")

        elif action_DECR == 'update':
            if not car_id_DECR:
                flash(" Car ID required to update", "error")
                return redirect(url_for('cars_DECR'))

            updates = []
            params = []

            if model_DECR:
                updates.append("car_model_DECR = %s")
                params.append(model_DECR)
            if brand_DECR:
                updates.append("car_brand_DECR = %s")
                params.append(brand_DECR)
            if price_raw:
                price = float(price_raw)
                updates.append("rental_price_DECR = %s")
                params.append(price)
            if availability_raw != "":
                availability = int(availability_raw)
                updates.append("availability_DECR = %s")
                params.append(availability)

            if not updates:
                flash(" No fields selected to update", "warning")
                return redirect(url_for('cars_DECR'))

            params.append(car_id_DECR)
            sql = f"UPDATE Cars_DECR SET {', '.join(updates)} WHERE car_id_DECR = %s"
            cursor.execute(sql, params)
            db.commit()
            flash(" Car updated successfully!", "success")

        elif action_DECR == 'delete':
            if not car_id_DECR:
                flash(" Car ID required to delete", "error")
                return redirect(url_for('cars_DECR'))
            cursor.execute("DELETE FROM Cars_DECR WHERE car_id_DECR = %s", (car_id_DECR,))
            db.commit()
            flash(" Car deleted permanently", "success")

    except Exception as e:
        db.rollback()
        flash(f" Database error: {str(e)}", "error")

    return redirect(url_for('cars_DECR'))

@app.route('/edit_header', methods=['GET', 'POST'])
@login_required
def edit_header_DECR():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Header_data_DECR LIMIT 1")
    header_data_DECR = cursor.fetchone()

    if request.method == 'POST':
        company_name_DECR = request.form.get('company_name_DECR')
        logo_path_DECR = request.form.get('logo_path_DECR')
        if not header_data_DECR:
            cursor2 = db.cursor()
            cursor2.execute("""
                INSERT INTO Header_data_DECR (company_name_DECR, logo_path_DECR)
                VALUES (%s, %s)
            """, (company_name_DECR, logo_path_DECR))
        else:
            cursor2 = db.cursor()
            cursor2.execute("""
                UPDATE Header_data_DECR
                SET company_name_DECR = %s, logo_path_DECR = %s
                WHERE header_id_DECR = %s
            """, (company_name_DECR, logo_path_DECR, header_data_DECR['header_id_DECR']))
        db.commit()
        flash(" Header updated successfully!", "success")
        return redirect(url_for('cars_DECR'))

    return render_template_string(edit_header_template_DECR, header_data_DECR=header_data_DECR)

@app.route('/chat', methods=['POST'])
@login_required
def chat_DECR():
    user_msg = request.form.get('chat_message_DECR', '').strip()
    if not user_msg:
        return redirect(url_for('cars_DECR'))

    # Get real car data for context
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cars_DECR")
    cars_context = cursor.fetchall()
    
    from datetime import datetime
    chat_log_DECR = session.get('chat_log_DECR', [])
    chat_log_DECR.append({
        'role': 'user', 
        'text': user_msg,
        'timestamp': datetime.now().strftime('%H:%M')
    })
    
    bot_reply = smart_chatbot_DECR(user_msg, cars_context, chat_log_DECR)
    chat_log_DECR.append({
        'role': 'bot', 
        'text': bot_reply,
        'timestamp': datetime.now().strftime('%H:%M')
    })
    
    session['chat_log_DECR'] = chat_log_DECR[-20:]  # Keep last 20 messages
    
    return redirect(url_for('cars_DECR'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)






# Team Contributions:
# 
# Hongor – Database & SQL
#  Create DB decr and export decr.sql
#  Create tables: header_data, users, cars  
#  Insert default data (header + admin)
#
# Hemang Tripathi – Header & Login
#  Dynamic header (load company name + logo from DB)
#  Edit header button (update DB, reflect automatically)
#  Admin login / logout system
#
# Mohammed Eltahawy – Main Table CRUD, Sorting & Extra Features
#  CRUD (Add, Update, Delete, View) for cars table
#  Implement Bubble Sort & Selection Sort
#  Make table display dynamic (images, text, availability)
#  Ensure sorting works with dynamic data
#
# Ibrahim Eltahawy – Search & Integration
#  Implement Binary Search for main table
#  Integrate all modules into one Python file
#  Ensure everything works together (header, login, CRUD, sort, search)

