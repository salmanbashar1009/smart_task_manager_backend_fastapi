# Fix Auth Register 500 Error

## Steps:
- [x] Edit app/repositories/user_repo.py: Fix session.refresh() to pass 'user' instance.
- [x] Test POST /auth/register via http://127.0.0.1:8000/docs (expect 200).
- [x] Restart server: Ctrl+C then `fastapi dev app/main.py` if needed.

Task complete. .gitignore added excluding venv/.
