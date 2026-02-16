import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_bart_torvik():
    results = {
        "rankings": [],
        "schedule": []
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        # Scrape Rankings
        print("Scraping Rankings...")
        page.goto('https://barttorvik.com/', wait_until='networkidle')
        time.sleep(5)
        soup_rankings = BeautifulSoup(page.content(), 'html.parser')
        
        rows = soup_rankings.find_all('tr', class_='seedrow')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 24:
                team_cell = cols[1]
                team_name = team_cell.get_text(separator=" ", strip=True).split('\n')[0].strip()
                # Clean team name - sometimes has rank/seed info
                if '(' in team_name:
                    team_name = team_name.split('(')[0].strip()
                
                def get_val(cell):
                    # Get only the text before the <br> or <span>
                    val = cell.find(string=True)
                    return val.strip() if val else ""

                data = {
                    "rank": get_val(cols[0]),
                    "team": team_name,
                    "conf": get_val(cols[2]),
                    "games": get_val(cols[3]),
                    "record": get_val(cols[4]),
                    "adj_oe": get_val(cols[5]),
                    "adj_de": get_val(cols[6]),
                    "barthag": get_val(cols[7]),
                    "efg_o": get_val(cols[8]),
                    "efg_d": get_val(cols[9]),
                    "tor": get_val(cols[10]),
                    "tord": get_val(cols[11]),
                    "orb": get_val(cols[12]),
                    "drb": get_val(cols[13]),
                    "ftr": get_val(cols[14]),
                    "ftrd": get_val(cols[15]),
                    "2p_o": get_val(cols[16]),
                    "2p_d": get_val(cols[17]),
                    "3p_o": get_val(cols[18]),
                    "3p_d": get_val(cols[19]),
                    "3pr": get_val(cols[20]),
                    "3prd": get_val(cols[21]),
                    "adj_t": get_val(cols[22]),
                    "wab": get_val(cols[23])
                }
                results["rankings"].append(data)

        # Scrape Schedule
        print("Scraping Schedule...")
        page.goto('https://barttorvik.com/schedule.php', wait_until='networkidle')
        time.sleep(5)
        soup_schedule = BeautifulSoup(page.content(), 'html.parser')
        
        table = soup_schedule.find('table', id='tblData')
        if table:
            sched_tbody = table.find('tbody')
            if sched_tbody:
                sched_rows = sched_tbody.find_all('tr')
                for row in sched_rows:
                    cols = row.find_all('td')
                    if len(cols) >= 5:
                        time_str = cols[0].text.strip()
                        matchup_cell = cols[1]
                        
                        # Extract network if available
                        network = ""
                        network_span = matchup_cell.find('span', style=lambda x: x and 'color:gray' in x)
                        if network_span:
                            network = network_span.text.strip()
                            
                        matchup_text = matchup_cell.get_text(separator=" ", strip=True)
                        # Extract T-Rank info
                        trank_line = cols[2].text.strip()
                        ttq = cols[3].text.strip()
                        result = cols[4].text.strip()
                        
                        game = {
                            "time": time_str,
                            "matchup": matchup_text,
                            "network": network,
                            "trank_line": trank_line,
                            "ttq": ttq,
                            "result": result
                        }
                        results["schedule"].append(game)

        browser.close()

    # Save to files
    timestamp = datetime.now().isoformat()
    
    with open('rankings.json', 'w', encoding='utf-8') as f:
        json.dump({"scraped_at": timestamp, "total_teams": len(results["rankings"]), "data": results["rankings"]}, f, indent=2)
    
    with open('schedule.json', 'w', encoding='utf-8') as f:
        json.dump({"scraped_at": timestamp, "total_games": len(results["schedule"]), "data": results["schedule"]}, f, indent=2)

    print(f"Scraping complete. Found {len(results['rankings'])} teams and {len(results['schedule'])} games.")

if __name__ == "__main__":
    scrape_bart_torvik()
