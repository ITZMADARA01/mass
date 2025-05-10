import asyncio
from telethon import TelegramClient, errors
from telethon.tl.functions.account import ReportPeerRequest

# Replace with your own Telegram API credentials
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'

client = TelegramClient('session_report', API_ID, API_HASH)

REASON_CODES = {
    "0": "Spam",
    "1": "Child abuse",
    "2": "Copyright",
    "3": "Unwanted contact or harassment",
    "4": "Other"
}

async def report_target(username_or_id: str, reason_code: int, report_times: int = 1):
    """
    Report a user/channel/group by username or id multiple times.
    """
    for i in range(report_times):
        try:
            entity = await client.get_entity(username_or_id)
            await client(ReportPeerRequest(peer=entity, reason=reason_code))
            print(f"[{i+1}/{report_times}] Successfully reported: {username_or_id} for reason '{REASON_CODES[str(reason_code)]}'")
        except errors.rpcerrorlist.UserIdInvalidError:
            print(f"Invalid target or cannot report {username_or_id}. You might need to be contacts or member.")
            return
        except Exception as e:
            print(f"Error reporting {username_or_id}: {e}")
            return
        await asyncio.sleep(1)  # slight delay between reports

async def main():
    print("=== Telegram Mass Reporting Script ===")
    await client.start()
    print("Logged in as", await client.get_me())

    while True:
        print("\nEnter usernames or channel/group IDs to report (comma-separated), or 'exit' to quit:")
        targets = input("Targets: ").strip()
        if targets.lower() == 'exit':
            break

        usernames = [t.strip() for t in targets.split(",") if t.strip()]
        if not usernames:
            print("No valid targets provided, please try again.")
            continue

        print("Choose a reason for reporting:")
        for code, desc in REASON_CODES.items():
            print(f"{code} - {desc}")
        reason = input("Reason code: ").strip()
        if reason not in REASON_CODES:
            print("Invalid reason code, defaulting to 'Other'.")
            reason = "4"

        times_str = input("How many times to report each target? (1-5 recommended): ").strip()
        try:
            times = int(times_str)
            if times < 1 or times > 20:
                print("Number of reports should be between 1 and 20, defaulting to 1.")
                times = 1
        except:
            print("Invalid input, defaulting number of reports to 1.")
            times = 1

        for u in usernames:
            await report_target(u, int(reason), times)

    print("Exiting... Goodbye!")
    await client.disconnect()

if _name_ == '_main_':
    asyncio.run(main())
