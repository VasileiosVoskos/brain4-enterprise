import streamlit as st, requests, bs4
st.header("🚨 Live Damage Alerts")
sites = {"NewsAuto": "https://www.newsauto.gr/category/news/ellada/"}
keywords = ["τροχα", "ατύχη", "καραμπ"]
for name, url in sites.items():
    st.subheader(name)
    try:
        html = requests.get(url, timeout=10).text
        soup = bs4.BeautifulSoup(html, "html.parser")
        links = soup.find_all("a", href=True, limit=20)
        for a in links:
            if any(k in a.text.lower() for k in keywords):
                st.write(f"• [{a.text.strip()}]({a['href']})")
    except Exception as e:
        st.error(e)
# Placeholder for alerts.py
