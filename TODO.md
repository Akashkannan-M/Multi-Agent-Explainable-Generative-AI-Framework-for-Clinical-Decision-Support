# TODO - Fix Dashboard Errors

## Confirmed Errors Across Dashboards

### 1. User Management Dashboard — "Delete User" broken
- **File:** `agents/user_agent.py`
- **Issue:** `delete_user()` uses `DELETE FROM users WHERE id=?` but column is `user_id`
- **Error:** `sqlite3.OperationalError: no such column: id`
- **Fix:** Change `WHERE id=?` → `WHERE user_id=?`

### 2. Reports Dashboard — "Search Reports" broken
- **File:** `agents/report_history_agent.py`
- **Issue:** Method `filter_reports()` missing (called by `app.py` Reports page)
- **Error:** `AttributeError: 'ReportHistoryAgent' object has no attribute 'filter_reports'`
- **Fix:** Add `filter_reports(start_date, end_date)` method

## Progress

- [x] Analyze all dashboard agents and app.py
- [x] Run verification script to confirm errors
- [x] Fix `user_agent.py` delete_user column
- [x] Add `filter_reports()` to report_history_agent.py
- [x] Re-run verification script to confirm all dashboards work
- [x] Clean up temp verification files

