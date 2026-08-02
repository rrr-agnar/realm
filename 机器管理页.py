async def admin_servers(request: Request, get_db, get_current_user, templates):
    user = get_current_user(request)
    if not user or not user.get("is_admin"):
        return RedirectResponse("/", 303)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM servers ORDER BY id")
    servers = [dict(x) for x in cur.fetchall()]
    for s in servers:
        cur.execute("SELECT COUNT(*) FROM port_rules WHERE server_id=?", (s["id"],))
        s["forward_count"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM protocol_accounts WHERE server_id=?", (s["id"],))
        s["protocol_count"] = cur.fetchone()[0]
    conn.close()
    return templates.TemplateResponse(
        request=request, name="admin_servers.html",
        context={"user": user, "servers": servers},
    )
