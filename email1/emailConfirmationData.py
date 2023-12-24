def create_subject_body(name, link):
    subject = "Confirm Your Email Address"
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
        <div class="snow"></div>
        <div class="container">
            <h1>Hello <b>{name}</b>,</h1>
            <p><b>Thank you for signing up for our service! We're excited to have you on board. Before you can start using your account, we just need to confirm your email address.</b></p>
            <p><b>To confirm your email address, please click on the following link:</b></p>
            <p class="button"><a href="{link}">Confirm Email</a></p>
            <p class="disclaimer">If you didn't sign up for our service, please disregard this email.</p>
            <p><b>Thank you,</b></p>
            <p class="signature"><b>#FlashBrain</b></p>
        </div>
    </body>
    </html>
    """

    return subject, body
