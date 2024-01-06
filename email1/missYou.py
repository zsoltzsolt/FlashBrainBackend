from routers.schemas import UserDisplay
import os
from datetime import datetime


def send_missing_you_email(user: UserDisplay, no_days: int):

    subject = f"🚀 Missing Your Spark, {user.username}! Rediscover the Power of FlashBrain Today"

    body = f"""<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            padding: 20px;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .container {{
            max-width: 600px;
            text-align: center;
            background-color: #1F70A7;  
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 40px;
            margin: 20px;
            position: relative;
            z-index: 1;
        }}
        .snow {{
            position: absolute;
            z-index: 2;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }}
        .snow:before {{
            content: '❄';
            position: absolute;
            color: #fff;
            animation: snowfall 10s linear infinite;
        }}
        @keyframes snowfall {{
            0% {{
                transform: translateY(-200%);
            }}
            100% {{
                transform: translateY(100vh);
            }}
        }}
        h1 {{
            color: #ffffff;
            font-size: 28px;
            margin-bottom: 15px;
        }}
        p {{
            margin-bottom: 20px;
            font-size: 18px;
            line-height: 1.6;
            font-weight: bold;
            color: #ffffff;
        }}
        .reasons {{
            text-align: left;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        .reason {{
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            color: #ffffff;
            font-size: 16px;
        }}
        .reason span {{
            margin-right: 10px;
            font-size: 20px;
            color: #ffffff;
        }}
        .cta-button {{
            margin-top: 30px;
        }}
        .button,
        .button a {{
            display: inline-block;
            padding: 15px 30px;
            font-size: 18px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            color: #ffffff;
            background-color: #1B262C;
            border: none;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }}
        .button:hover,
        .button a:hover {{
            background-color: #1B262C;
        }}
        .disclaimer {{
            color: #ffffff;
            font-size: 16px;
            margin-top: 30px;
        }}
        .signature {{
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="snow"></div>
    <div class="container">
        <h1>Hello <b>{user.username}</b>,</h1>
        <p><b>It's been a little quiet on FlashBrain lately, and we've missed your dynamic presence on our platform.</b></p>
        <div class="reasons">
            <div class="reason">
                <span>1.</span> New Challenges Await: We've added a fresh set of mind-bending challenges tailored to elevate your cognitive skills.
            </div>
            <div class="reason">
                <span>2.</span> Community Connections: Engage with fellow enthusiasts, share your insights, and learn from others who appreciate the power of a sharp mind.
            </div>
            <div class="reason">
                <span>3.</span> Exclusive Features: Explore the latest features designed to enhance your FlashBrain experience.
            </div>
        </div>
        <p class="disclaimer">To welcome you back, we've prepared a special surprise. Click the button below to rekindle the spark:</p>
        <p class="cta-button button"><a href="{os.environ.get("FRONTEND_URL")}">Resume Your Journey</a></p>
        <p class="disclaimer">It's been {no_days} days since your last activity. Thank you for being a valued part of the FlashBrain community. We can't wait to see you back in action!</p>
        <p class="signature"><b>#FlashBrain 🚀</b></p>
    </div>
</body>
</html>
"""

    return subject, body
