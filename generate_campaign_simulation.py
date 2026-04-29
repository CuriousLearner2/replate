import csv
import random

# Configuration
NUM_USERS = 100
DOMAINS = ["gmail.com", "outlook.com", "techfirm.io", "consulting.com", "university.edu"]
OUTPUT_DIR = "synthetic data"
OUTPUT_FILE = f"{OUTPUT_DIR}/campaign_responses_simulated.csv"

def generate_data():
    # ... (rest of function remains the same)
    users = []
    for i in range(1, NUM_USERS + 1):
        user_id = f"donor_{i:03}"
        domain = random.choice(DOMAINS)
        email = f"user_{i}@{domain}"
        
        # Simulate behavioral signals (clicks)
        # 40% chance to click Efficiency story (Category 1)
        clicked_efficiency = random.random() < 0.40
        
        # 35% chance to click Human Impact story (Category 2)
        clicked_human_impact = random.random() < 0.35
        
        # Simulate donation status
        # Higher chance to donate if they clicked something
        donation_prob = 0.05
        if clicked_efficiency: donation_prob += 0.20
        if clicked_human_impact: donation_prob += 0.25
        
        donated_amount = 0
        if random.random() < donation_prob:
            # Random gift between $25 and $500
            donated_amount = random.randint(25, 500)
        
        # Determine Archetype and Loyalty Level for Meta
        # VIPs = High Engagement + High Donation
        loyalty_level = "POTENTIAL"
        if donated_amount > 100 or (clicked_efficiency and clicked_human_impact):
            loyalty_level = "VIP"
        elif donated_amount > 0:
            loyalty_level = "STANDARD"

        users.append({
            "USER_ID": user_id,
            "EMAIL": email,
            "CLICKED_EFFICIENCY": clicked_efficiency,
            "CLICKED_HUMAN_IMPACT": clicked_human_impact,
            "DONATED_AMOUNT": donated_amount,
            "LOYALTY_LEVEL": loyalty_level
        })
    
    return users

def save_to_csv(data):
    keys = data[0].keys()
    with open(OUTPUT_FILE, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"SUCCESS: Generated {NUM_USERS} responses in {OUTPUT_FILE}")

if __name__ == "__main__":
    simulated_data = generate_data()
    save_to_csv(simulated_data)
    
    # Quick Summary for the user
    vips = [u for u in simulated_data if u['LOYALTY_LEVEL'] == "VIP"]
    print(f"--- Campaign Analysis ---")
    print(f"Total Potentials: {NUM_USERS}")
    print(f"Total VIPs Identified (Seed List): {len(vips)}")
    print(f"Efficiency Clicks: {sum(1 for u in simulated_data if u['CLICKED_EFFICIENCY'])}")
    print(f"Human Impact Clicks: {sum(1 for u in simulated_data if u['CLICKED_HUMAN_IMPACT'])}")
