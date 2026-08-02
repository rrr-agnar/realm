async def admin_add_server(
    request: Request,
    get_db, get_current_user,
    name: str = Form(...),
    ssh_host: str = Form(...),
    ssh_port: int = Form(22),
    ssh_user: str = Form("root"),
    ssh_key_path: str = Form("/root/.ssh/id_ed25519"),
    mode: str = Form("both"),          # forward | protocol | both —— 这就是你要的
    port_range: str = Form("1024-65535"),
    xray_api_port: int = Form(10085),
    remark: str = Form(""),
):
    user = get_current_user(request)
    if not user or not user.get("is_admin"):
        return RedirectResponse("/", 303)
    if mode not in ("forward", "protocol", "both"):
        return RedirectResponse("/admin/servers?error=bad_mode", 303)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO servers (name, ssh_host, ssh_port, ssh_user, ssh_key_path,
                              mode, port_range, xray_api_port, status, remark)
        VALUES (?,?,?,?,?,?,?,?, 'active', ?)
    """, (name, ssh_host, ssh_port, ssh_user, ssh_key_path, mode,
          port_range, xray_api_port, remark))
    conn.commit()
    conn.close()
    return RedirectResponse("/admin/servers?ok=added", 303)
