import asyncio

from ws_ui import Application


def main():
    app = Application()
    asyncio.run(app.main())


if __name__ == '__main__':
    main()
