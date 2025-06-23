import asyncio

from src.bot import run_process

if __name__ == "__main__":
    try:
        print("Start working...")
        asyncio.run(run_process())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Critical error: {e}")
