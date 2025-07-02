import pandas as pd 
import numpy as np 
import matplotlib, matplotlib.pyplot as plt
import io
import base64

DATA_PATH = "dataset/data.json"
matplotlib.use("Agg") 

def get_players():
    df = pd.read_json(DATA_PATH)
    return sorted(df['player_name'].unique().tolist())

def analyze_player(player_name):
    df = pd.read_json(DATA_PATH)
    player_df = df[df["player_name"] == player_name]
    
    total_runs = player_df['runs'].sum()
    total_balls = player_df['balls'].sum()
    matches = player_df['match_id'].sum()
    strike_rate = round((total_runs / total_balls) * 100, 2) if total_balls > 0 else 0
    average = round(player_df['runs'].mean(), 2)
    std_dev = round(player_df['runs'].std(), 2)
    
    plt.figure(figsize=(6,4))
    plt.plot(player_df["match_id"], player_df["runs"], marker="o", color="blue")
    plt.title(f"{player_name} - Runs Over Matches")
    plt.xlabel("Match ID")
    plt.ylabel("Runs")
    plt.grid(True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    line_chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    # Dismissal breakdown pie chart
    dismissal_counts = player_df["dismissal"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax.pie(
    dismissal_counts.values,
    labels=dismissal_counts.index,
    autopct="%1.1f%%",
    shadow=True,
    startangle=140,
    explode=[0.05]*len(dismissal_counts)
)
    plt.title(f"{player_name} - Dismissal Types")

    # Save to base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    pie_chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    
    return {
    "player": player_name,
    "matches": int(matches),
    "runs": int(total_runs),
    "balls": int(total_balls),
    "average": float(average),
    "strike_rate": float(strike_rate),
    "consistency": float(std_dev),
    "charts": {
        "runs_over_matches": f"data:image/png;base64,{line_chart_base64}",
        "dismissal_pie": f"data:image/png;base64,{pie_chart_base64}"
    }
}