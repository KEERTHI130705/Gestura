import uvicorn


def main() -> None:
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000, reload=False, workers=1)


if __name__ == '__main__':
    main()

