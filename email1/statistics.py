from routers.schemas import UserDisplay

def send_statistics(user: UserDisplay):
    subject = "🌟 Your Impact is Growing!"
    no_summaries = len(user.summaries)
    no_likes = sum(len(summary.like) for summary in user.summaries)
    no_views = sum(len(summary.viewHistory) for summary in user.summaries)

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
            font-size: 24px;
            margin-bottom: 10px;
        }}
        p {{
            margin-bottom: 20px;
            font-size: 16px;
            line-height: 1.6;
            font-weight: bold;
            color: #ffffff;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;  /* Updated spacing */
            margin: 50px;
        }}
        .stat-item {{
            flex: 1;
            text-align: center;
        }}
        .stat-label {{
            color: #ffffff;
            font-size: 12px;
            margin-bottom: 5px;
            text-transform: uppercase;
            display: flex;
            justify-content: space-around;  /* Updated spacing */
            margin: 50px;
        }}
        .stat-value {{
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
        }}
        .button,
        .button a {{
            display: inline-block;
            padding: 10px 20px;
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
        .disclaimer {{
            color: #ffffff;
            font-size: 14px;
            margin-top: 30px;
        }}
        .signature {{
            font-size: 24px;
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
        <p><b>Exciting news! Your journey with #FlashBrain 🚀 is creating waves! Here's a glimpse of your latest achievements:</b></p>
        <div class="stats">
            <div class="stat-item">
                <p class="stat-label">Summaries</p>
                <p class="stat-value">{no_summaries}</p>
            </div>
            <div class="stat-item">
                <p class="stat-label">Likes</p>
                <p class="stat-value">{no_likes}</p>
            </div>
            <div class="stat-item">
                <p class="stat-label">Views</p>
                <p class="stat-value">{no_views}</p>
            </div>
        </div>
        <p class="disclaimer">Your impact is growing, and your content is resonating with others. Keep shining! 🌟</p>
        <p><b>Thank you for being a part of the #FlashBrain community!</b></p>
        <p class="signature"><b>#FlashBrain 🚀 Team</b></p>
    </div>
</body>
</html>
"""

    return subject, body
