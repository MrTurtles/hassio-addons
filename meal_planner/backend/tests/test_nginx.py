from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[2]
NGINX_CONF = APP_ROOT / "rootfs" / "etc" / "nginx" / "http.d" / "meal-planner.conf"
INDEX_HTML = APP_ROOT / "frontend" / "index.html"


def test_nginx_separates_ingress_from_the_internal_api() -> None:
    config = NGINX_CONF.read_text(encoding="utf-8")
    assert "listen 8099" in config
    assert "allow 172.30.32.2" in config
    assert "deny all" in config
    assert "listen 8098" in config
    assert 'proxy_set_header X-MealPlanner-Channel "ingress"' in config
    assert 'proxy_set_header X-MealPlanner-Channel "internal"' in config
    assert "proxy_pass http://127.0.0.1:8000" in config


def test_frontend_keeps_the_ingress_placeholder() -> None:
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert "__INGRESS_BASE_HREF__" in html
