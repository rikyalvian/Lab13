from django.http import HttpResponse

def welcome(request):
    return HttpResponse("""
        <html>
            <head>
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        flex-direction: column;
                        text-align: center;
                    }
                    h1 {
                        font-size: 48px;
                        font-weight: bold;
                    }
                    p {
                        font-size: 24px;
                    }
                </style>
            </head>
            <body>
                <h1>Selamat Datang di Aplikasi Django!</h1>
                <p>Perkenalkan Saya Riky Alvian</p>
            </body>
        </html>
    """)
