def create_subject_body(name, link):
    subject = "Summary generated 🎉🎉🎉"
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
            .confetti {{
                position: absolute;
                z-index: 2;
                width: 100%;
                height: 100%;
                pointer-events: none;
                overflow: hidden;
            }}
            .confetti:before {{
                content: '🎉';
                position: absolute;
                color: #FFD700; /* Gold */
                font-size: 20px;
                animation: confetti-fall 10s linear infinite;
            }}
            @keyframes confetti-fall {{
                0% {{
                    transform: translateY(-200%);
                }}
                100% {{
                    transform: translateY(100vh);
                }}
            }}
            h1 {{
                color: #ffffff;
            }}
            p {{
                margin-bottom: 20px;
                font-size: 16px;
                line-height: 1.6;
                font-weight: bold;
                color: #ffffff;
            }}
            .button,
            .button a {{
                display: inline-block;
                padding: 5px 15px;
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
        <div class="confetti"></div>
        <div class="container">
           <h1>Hello <b>{name}</b>,</h1>
            <p><b>Congratulations! Your personalized summary is ready to dazzle.</b></p>
            <p><b>To view your summary, simply click on the glittering link below:</b></p>
            <p class="button"><a href="{link}">View Your Flashy Summary</a></p>
            <p class="disclaimer">In case you're wondering, this isn't your average summary—it's a masterpiece!</p>
            <p><b>Sparkling regards,</b></p>
            <p class="signature"><b>#FlashBrain 🚀</b></p>
        </div>
    </body>
    </html>
    """

    return subject, body
