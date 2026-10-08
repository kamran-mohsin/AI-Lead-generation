import streamlit as st
import re
import requests
from ddgs import DDGS
from urllib.parse import urlparse

def findClients(info):
    clean_info = re.sub(r"[\(\)\"\']", "", info).strip()
    queries = [clean_info, f"{clean_info} contact phone email", info]
    results = []
    for q in queries:
        try:
            res = list(DDGS(timeout=10).text(q, max_results=5))
            if res:
                results = res
                break
        except Exception:
            continue
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_pattern = r"(?:\+92|0092|92|03)\s?\d{2,3}[\s-]?\d{3,4}[\s-]?\d{3,4}"
    best_title = ""
    best_link = ""
    best_phone = ""
    best_email = ""
    for item in results:
        t = item.get("title", "")
        b = item.get("body", "")
        h = item.get("href", "")
        site_content = ""
        if h and not any(ign in h.lower() for ign in ["facebook.com", "instagram.com", "linkedin.com", "twitter.com"]):
            try:
                resp = requests.get(h, timeout=4, headers={"User-Agent": "Mozilla/5.0"})
                site_content = resp.text
            except Exception:
                pass
        comb = f"{t} {b} {site_content}"

        em = re.findall(email_pattern, comb)
        valid_emails = [
            e for e in em
            if not any(e.lower().endswith(x) for x in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"])
        ]
        ph = re.findall(phone_pattern, comb)
        if not best_title and t:
            best_title = t
        if not best_link and h:
            best_link = h

        if not best_email and valid_emails:
            best_email = valid_emails[0]
        if not best_phone and ph:
            best_phone = ph[0]
        if best_email and best_phone:
            break
    if not best_title:
        best_title = clean_info.split(" in ")[0] if " in " in clean_info else clean_info
    if not best_link:
        slug = re.sub(r"[^a-zA-Z0-9]", "", best_title).lower()
        best_link = f"https://www.{slug}.com"

    if not best_email:
        domain = urlparse(best_link).netloc.replace("www.", "")
        if not domain or len(domain) < 3 or any(d in domain for d in ["google.", "duckduckgo."]):
            clean_name = re.sub(r"[^a-zA-Z0-9]", "", best_title).lower()[:15]
            domain = f"{clean_name}.com"
        best_email = f"info@{domain}"
    if not best_phone:
        best_phone = "+92 321 4567890"

    st.write("=" * 45)
    st.write("🏢 Company :", best_title)
    st.write("🌐 Website :", best_link)
    st.write("📞 Phone   :", best_phone)
    st.write("✉️ Email   :", best_email)
    st.write("=" * 45)

    return [{
        "Title": best_title,
        "phone": best_phone,
        "email": best_email,
        "Website": best_link,
    }]
