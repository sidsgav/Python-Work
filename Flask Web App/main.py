from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug = True) # runs this file only when this file is ran directly not elsewhere

