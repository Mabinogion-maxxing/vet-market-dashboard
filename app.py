import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(
    page_title="US Veterinary Health Market Dashboard",
    page_icon="🐾",
    layout="wide"
)

st.sidebar.title("Pointer Health")
st.sidebar.markdown("Veterinary Market Intelligence")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["Market Overview", "Market Trends", "Competitive Landscape", "Google Trends", "Industry News"]
)

st.title("US Veterinary Health Market Dashboard")
st.markdown("Real-Time Market Insights into the US Veterinary Health Market")

if page == "Market Overview":
    st.header("Market Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="US Vet Market Size 2024", value="\$37.3B", delta="+7.2% YoY")

    with col2:
        st.metric(label="US Pet Ownership", value="66%", delta="+2% vs 2020")

    with col3:
        st.metric(label="Vet Clinics in US", value="~33,000", delta="+1.5% YoY")

    st.markdown("---")
    st.caption("Data sources: AVMA, APPA, IBISWorld | Built for Pointer Health")

if page == "Market Trends":
    st.header("Market Trends")

    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
    market_size = [28.0, 29.3, 30.2, 32.3, 34.0, 35.4, 37.3]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=years,
        y=market_size,
        marker_color="teal",
        text=market_size,
        textposition="outside"
    ))
    fig1.update_layout(
        title="US Veterinary Market Size (Billions USD)",
        xaxis_title="Year",
        yaxis_title="Market Size (Billions USD)",
        template="plotly_white",
        height=450
    )
    st.plotly_chart(fig1, use_container_width=True)

    chart_coll, chart_col2 = st.columns(2)

    with chart_coll:
        pet_years = [2018, 2020, 2022, 2024]
        dog_ownership = [48.2, 50.0, 53.0, 54.7, 55.4]

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=pet_years,
            y=dog_ownership,
            mode="lines+markers",
            name="Dogs",
            line=dict(color="#3498db", width=3),
            marker=dict(size=8)
        ))
        fig2.update_layout(
            title="US Pet Ownership (Millions of Households)",
            xaxis_title="Year",
            yaxis_title="Households (Millions)",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)

    with chart_col2:
        segments = ["Clinical Visits", "Diagnostics", "Therapeutics", "Preventive Care", "Other"]
        values = [35, 25, 20, 12, 8]
        colors = ["#2ecc71", "#3498db", "#e74c3c", "#f39c12", "#9b59b6"]

        fig3 = go.Figure()
        fig3.add_trace(go.Pie(
            labels=segments,
            values=values,
            marker=dict(colors=colors),
            hole=0.4,
            textinfo="label+percent"
        ))
        fig3.update_layout(
            title="Veterinary Market Segments",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

if page == "Competitive Landscape":
    st.header("Competitive Landscape")

    st.markdown("Key players in the veterinary health technology space:")

    competitors = [
        {"Company": "Antech Diagnostics", "Focus": "Diagnostics", "Parent": "Mars Inc.", "Founded": "1986", "Status": "Acquired", "Notes": "Leading veterinary diagnostics lab network"},
        {"Company": "IDEXX Laboratories", "Focus": "Diagnostics & Software", "Parent": "Public (IDXX)", "Founded": "1983", "Status": "Public", "Notes": "Market leader in vet diagnostics and practice software"},
        {"Company": "Zoetis", "Focus": "Pharmaceuticals", "Parent": "Public (ZTS)", "Founded": "2013", "Status": "Public", "Notes": "Largest global animal health pharma company"},
        {"Company": "Petriage", "Focus": "AI Triage", "Parent": "Independent", "Founded": "2018", "Status": "Startup", "Notes": "AI-powered pet symptom checker"},
        {"Company": "Vetcove", "Focus": "Supply Chain", "Parent": "Independent", "Founded": "2015", "Status": "Startup", "Notes": "Online marketplace for vet supplies"},
        {"Company": "Pawp", "Focus": "Telehealth", "Parent": "Independent", "Founded": "2019", "Status": "Startup", "Notes": "24/7 digital pet clinic"},
        {"Company": "Whistle", "Focus": "Wearables", "Parent": "Mars Inc.", "Founded": "2012", "Status": "Acquired", "Notes": "GPS and health monitoring for pets"},
        {"Company": "Scratchpay", "Focus": "Financing", "Parent": "Independent", "Founded": "2016", "Status": "Startup", "Notes": "Payment plans for veterinary care"},
    ]

    import pandas as pd
    df = pd.DataFrame(competitors)

    status_filter = st.multiselect(
        "Filter by status:",
        options=df["Status"].unique(),
        default=df["Status"].unique()
    )

    filtered_df = df[df["Status"].isin(status_filter)]
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    comp_col1, comp_col2 = st.columns(2)

    with comp_col1:
        status_counts = df["Status"].value_counts()
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=status_counts.index.tolist(),
            y=status_counts.values.tolist(),
            marker_color=["#2ecc71", "#3498db", "#e74c3c", "#f39c12"]
        ))
        fig4.update_layout(
            title="Competitors by Status",
            template="plotly_white",
            height=350
        )
        st.plotly_chart(fig4, use_container_width=True)

    with comp_col2:
        focus_counts = df["Focus"].value_counts()
        fig5 = go.Figure()
        fig5.add_trace(go.Pie(
            labels=focus_counts.index.tolist(),
            values=focus_counts.values.tolist(),
            hole=0.4,
            textinfo="label+percent"
        ))
        fig5.update_layout(
            title="Competitors by Focus Area",
            template="plotly_white",
            height=350
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

if page == "Google Trends":
    st.header("Google Search Trends")
    st.markdown("What people are searching for in veterinary health:")

    from pytrends.request import TrendReq

    @st.cache_data(ttl=86400)
    def get_trends(keywords):
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload(keywords, cat=0, timeframe="today 12-m", geo="US")
        data = pytrends.interest_over_time()
        return data

    trend_options = [
        "Pointer Health",
        "veterinary telehealth",
        "pet diagnostics",
        "pet wellness",
        "animal hospital",
        "dog health",
        "cat health",
        "pet wearable",
        "veterinary AI",
        "pet preventive care"
    ]

    selected_trends = st.multiselect(
        "Select up to 5 search terms to compare:",
        options=trend_options,
        default=["Pointer Health"]
    )

    if selected_trends and len(selected_trends) <= 5:
        try:
            trends_data = get_trends(selected_trends)
            if not trends_data.empty:
                fig6 = go.Figure()
                for keyword in selected_trends:
                    if keyword in trends_data.columns:
                        fig6.add_trace(go.Scatter(
                            x=trends_data.index,
                            y=trends_data[keyword],
                            mode="lines",
                            name=keyword,
                            line=dict(width=2)
                        ))
                fig6.update_layout(
                    title="Google Search Interest Over Past 12 Months (US)",
                    xaxis_title="Date",
                    yaxis_title="Search Interest (0-100)",
                    template="plotly_white",
                    height=450,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3)
                )
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.warning("No trend data available for selected terms.")
        except Exception as e:
            st.error("Error fetching Google Trends data: " + str(e))
    elif len(selected_trends) > 5:
        st.warning("Please select 5 or fewer search terms.")
    else:
        st.info("Select at least one search term above.")

    st.markdown("---")

if page == "Industry News":
    st.header("Latest Veterinary Industry News")

    import os
    API_Key = os.environ.get("NEWS_API_KEY", "")

    @st.cache_data(ttl=3600)
    def get_news(query):
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": API_Key
        }

        response = requests.get(url, params=params)
        return response.json()

    search_topic = st.selectbox("Choose a topic:", ["veterinary health industry", "animal health technology", "pet diagnostics", "veterinary pharmaceuticals", "veterinary health care", "North American veterinary market", "veterinary services", "veterinary research", "veterinary education", "veterinary telemedicine"])

    news_data = get_news(search_topic)

    if news_data.get("status") == "ok":
        articles = news_data.get("articles", [])
        if articles:
            for article in articles:
                title = article.get("title", "No title")
                description = article.get("description", "No description available")
                url = article.get("url", "")
                source = article.get("source", {}).get("name", "Unknown")
                published = article.get("publishedAt", "")[:10]
                st.subheader(title)
                st.markdown(f"**{source}** | {published}")
                st.markdown(description)
                st.markdown(f"[Read full article]({url})")
                st.markdown("---")

            else:
                st.warning("No news articles found for the selected topic.")
    else:
        st.error("Error fetching news data. Please try again later.")

    st.caption("Data source: NewsAPI.org | Built for Pointer Health")

