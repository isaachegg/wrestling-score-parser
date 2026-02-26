import re
import csv
from collections import defaultdict

# Import the scoring logic from our new rules file
from scoring_rules import get_advancement_points, get_bonus_points, get_placement_points

def tally_wrestling_scores(file_path):
    # Store team data: just the total score
    team_scores = defaultdict(float)
    
    # Store wrestler data: team, total, adv, bonus, placement
    wrestler_scores = defaultdict(lambda: {"team": "", "total": 0.0, "adv": 0.0, "bonus": 0.0, "placement": 0.0})

    pattern = re.compile(r"^(.*?) - (.*?) \((.*?)\).*? won (.*?) over (.*?) \((.*?)\)")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = pattern.search(line.strip())
                if not match:
                    continue

                round_name = match.group(1).strip()
                winner_name = match.group(2).strip()
                winner_team = match.group(3).strip()
                win_method = match.group(4).strip().lower()
                loser_name = match.group(5).strip()
                loser_team = match.group(6).strip()

                # Register teams for both wrestlers
                wrestler_scores[winner_name]["team"] = winner_team
                wrestler_scores[loser_name]["team"] = loser_team

                # --- 1. Fetch Points Using scoring_rules.py ---
                adv_pts = get_advancement_points(round_name)
                bonus_pts = get_bonus_points(win_method)
                winner_place_pts, loser_place_pts = get_placement_points(round_name)

                # --- 2. Apply Placement Points ---
                if winner_place_pts > 0:
                    wrestler_scores[winner_name]["placement"] += winner_place_pts
                    wrestler_scores[winner_name]["total"] += winner_place_pts
                    team_scores[winner_team] += winner_place_pts
                    
                    wrestler_scores[loser_name]["placement"] += loser_place_pts
                    wrestler_scores[loser_name]["total"] += loser_place_pts
                    team_scores[loser_team] += loser_place_pts

                # --- 3. Apply Advancement & Bonus Points ---
                wrestler_scores[winner_name]["adv"] += adv_pts
                wrestler_scores[winner_name]["bonus"] += bonus_pts
                wrestler_scores[winner_name]["total"] += (adv_pts + bonus_pts)
                
                team_scores[winner_team] += (adv_pts + bonus_pts)

    except FileNotFoundError:
        print(f"Error: Could not find file '{file_path}'. Please ensure the file is in the same directory.")
        return

    # Sort teams by total score (descending)
    sorted_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Sort wrestlers alphabetically by team (A-Z), then alphabetically by name (A-Z)
    sorted_wrestlers = sorted(wrestler_scores.items(), key=lambda x: (x[1]["team"], x[0]))

    # Trigger CSV generation
    generate_csvs(sorted_teams, sorted_wrestlers)

def generate_csvs(sorted_teams, sorted_wrestlers):
    # Create the Team Scores CSV
    with open('team_scores.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Team', 'Total Points'])
        for rank, (team, score) in enumerate(sorted_teams, start=1):
            writer.writerow([rank, team, score])
    print("Successfully generated 'team_scores.csv'")

    # Create the Individual Wrestler Scores CSV
    with open('wrestler_scores.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Team', 'Wrestler', 'Total Points', 'Advancement Pts', 'Bonus Pts', 'Placement Pts'])
        
        previous_team = None
        for wrestler, data in sorted_wrestlers:
            current_team = data['team']
            
            # Insert a blank row if the team name changes
            if previous_team is not None and current_team != previous_team:
                writer.writerow([])
                
            writer.writerow([current_team, wrestler, data['total'], data['adv'], data['bonus'], data['placement']])
            
            previous_team = current_team
            
    print("Successfully generated 'wrestler_scores.csv' with spaced teams")

if __name__ == "__main__":
    tally_wrestling_scores("vhsl_girls_states_matches.txt")