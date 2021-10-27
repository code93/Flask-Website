from companyblog import app

if __name__ == '__main__':
    from os import environ
    app.run(debug=False, port=environ.get("PORT", 5000))
