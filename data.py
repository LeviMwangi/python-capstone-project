import sqlite3
from datetime import datetime


def connect_db():
    """Connect to the SQLite database and return the connection."""
    return sqlite3.connect('safety.db')


def initialize_database():
    """Initialize the database and create tables if they don't exist."""
    conn = connect_db()
    c = conn.cursor()
    
    # Create the tips table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def add_safety_tips():
    """Add safety tips to the database."""
    safety_tips = [
        {"title": "Fire Safety", "content": "Install smoke alarms and regularly check their batteries."},
        {"title": "Road Safety", "content": "Always wear a seatbelt and follow traffic rules."},
        {"title": "Workplace Safety", "content": "Ensure proper use of personal protective equipment (PPE)."},
        {"title": "Electrical Safety", "content": "Do not overload electrical outlets and unplug appliances when not in use."},
        {"title": "Water Safety", "content": "Never leave children unattended near water sources like pools or bathtubs."},
        {"title": "Cybersecurity", "content": "Use strong, unique passwords and enable two-factor authentication."},
        {"title": "Health and Hygiene", "content": "Wash your hands regularly to prevent illness."},
        {"title": "Emergency Preparedness", "content": "Keep a first-aid kit and emergency supplies handy."},
        {"title": "Home Security", "content": "Lock doors and windows when leaving your home or before sleeping."},
        {"title": "Food Safety", "content": "Refrigerate perishable foods promptly and check expiration dates."},
        {"title": "Travel Safety", "content": "Be aware of local laws and emergency contacts when traveling."},
        {"title": "Child Safety", "content": "Teach children about stranger danger and safe behavior."},
        {"title": "Pet Safety", "content": "Ensure pets have access to clean water and a safe environment."},
        {"title": "Outdoor Safety", "content": "Wear sunscreen and stay hydrated when outdoors."},
        {"title": "Medication Safety", "content": "Store medications out of reach of children and only take prescribed doses."},
        {"title": "Alcohol Safety", "content": "Drink responsibly and never drive under the influence."},
        {"title": "Sports Safety", "content": "Use appropriate gear and follow safety guidelines for your activity."},
        {"title": "Disaster Safety", "content": "Learn evacuation routes and emergency procedures for your area."},
        {"title": "Tool Safety", "content": "Use tools only for their intended purpose and wear safety equipment."},
        {"title": "Mental Health Safety", "content": "Take breaks, seek support, and avoid burnout."},
        {"title": "Swimming Safety", "content": "Always swim with a buddy and never swim in dangerous weather conditions."},
        {"title": "Cycling Safety", "content": "Wear a helmet and ensure your bike is in good working condition."},
        {"title": "Camping Safety", "content": "Pack adequate supplies and follow Leave No Trace principles."},
        {"title": "Mountain Safety", "content": "Check weather conditions before hiking and inform someone of your route."},
        {"title": "Skiing Safety", "content": "Wear protective gear, ski within your ability, and follow resort rules."},
        {"title": "Home Fire Safety", "content": "Keep flammable items away from heat sources and never leave cooking unattended."},
        {"title": "Chemical Safety", "content": "Handle chemicals with care and follow safety instructions on labels."},
        {"title": "Social Media Safety", "content": "Limit the personal information shared online and use privacy settings."},
        {"title": "Elderly Safety", "content": "Ensure that homes are fall-proof and install grab bars where necessary."},
        {"title": "Gun Safety", "content": "Store firearms safely in a locked cabinet and keep ammunition separate."},
        {"title": "Childproofing Your Home", "content": "Use safety gates, outlet covers, and cabinet locks to prevent accidents."},
        {"title": "Work from Home Safety", "content": "Set up an ergonomic workstation and take regular breaks."},
        {"title": "Hand Tool Safety", "content": "Inspect tools before use and use the correct tool for the job."},
        {"title": "Sun Protection", "content": "Wear a wide-brimmed hat and sunscreen to protect from harmful UV rays."},
        {"title": "Lifting Safety", "content": "Lift with your legs, not your back, and avoid lifting objects that are too heavy."},
        {"title": "Tornado Safety", "content": "Seek shelter in a basement or interior room away from windows during a tornado."},
        {"title": "Hurricane Safety", "content": "Have an emergency kit ready and know your evacuation routes in advance."},
        {"title": "Ladder Safety", "content": "Ensure the ladder is on a stable surface and never stand on the top rung."},
        {"title": "Snow Safety", "content": "Shovel snow carefully to avoid strain and wear proper footwear to prevent slips."},
        {"title": "Bicycle Helmet Safety", "content": "Always wear a helmet, even on short rides, to protect against head injuries."},
        {"title": "Pet First Aid", "content": "Know basic first aid for pets, such as how to perform CPR and handle injuries."},
        {"title": "Flood Safety", "content": "Do not walk or drive through flooded areas; seek higher ground immediately."},
        {"title": "Ear Protection", "content": "Wear earplugs in loud environments to protect your hearing."},
        {"title": "Workplace Ergonomics", "content": "Adjust your workstation to prevent strain on your eyes, neck, and back."},
        {"title": "Electric Scooter Safety", "content": "Always wear a helmet, follow local laws, and ride responsibly."},
        {"title": "Slips and Falls Prevention", "content": "Keep walkways clear and use non-slip rugs to avoid tripping hazards."},
        {"title": "Emergency Contact List", "content": "Keep an updated list of emergency contacts in your phone and at home."},
        {"title": "Accident Prevention in the Kitchen", "content": "Keep knives sharp, store them safely, and clean up spills immediately."},
        {"title": "Carbon Monoxide Safety", "content": "Install a carbon monoxide detector and ensure proper ventilation in your home."},
        {"title": "Hiking Safety", "content": "Stay on marked trails, carry a map, and be prepared for changes in weather."},
        {"title": "Stress Management", "content": "Practice mindfulness or relaxation techniques to manage stress effectively."},
        {"title": "Hearing Protection", "content": "Wear ear protection when using loud machinery or attending concerts."},
        {"title": "Mental Health Support", "content": "Reach out to a therapist or support group when feeling overwhelmed."},
        {"title": "Bicycle Lock Safety", "content": "Use a strong, reliable lock to secure your bicycle in public places."},
        {"title": "Winter Driving Safety", "content": "Keep an emergency kit in your car and drive cautiously in snowy or icy conditions."},
        {"title": "Noise Pollution Safety", "content": "Limit exposure to loud noises and take regular breaks in quiet spaces."},
        {"title": "Tobacco Safety", "content": "Avoid smoking or using tobacco products to prevent long-term health risks."},
        {"title": "Backpack Safety", "content": "Carry a backpack with both straps and avoid overloading it to prevent back pain."},
        {"title": "Construction Site Safety", "content": "Wear a hard hat, steel-toed boots, and high-visibility clothing on construction sites."},
        {"title": "Watercraft Safety", "content": "Wear a life jacket and never operate a watercraft under the influence of alcohol."},
        {"title": "Sleep Safety", "content": "Create a comfortable sleep environment and avoid screens before bed."},
        {"title": "Safe Socializing", "content": "Practice safe social distancing and wear a mask when necessary."},
        {"title": "Public Transport Safety", "content": "Be aware of your surroundings and keep your belongings close on public transport."},
        {"title": "Grocery Store Safety", "content": "Use sanitizing wipes on shopping carts and avoid touching your face."},
        {"title": "Outdoor Fire Safety", "content": "Ensure campfires are fully extinguished before leaving and avoid dry areas."},
        {"title": "First-Aid Knowledge", "content": "Learn basic first-aid techniques such as CPR, bandaging, and wound care."},
        {"title": "Dog Walking Safety", "content": "Keep dogs on a leash and watch for traffic when walking in busy areas."},
        {"title": "Winter Clothing Safety", "content": "Dress in layers and wear waterproof boots to prevent hypothermia."},
        {"title": "Online Shopping Safety", "content": "Shop on secure websites and avoid using public Wi-Fi for transactions."},
        {"title": "Emergency Escape Plan", "content": "Create a family emergency escape plan and practice it regularly."},
        {"title": "Sunburn Prevention", "content": "Apply sunscreen every 2 hours and wear protective clothing when outdoors."},
        {"title": "Avoiding Distractions While Driving", "content": "Do not use your phone while driving and stay focused on the road."},
        {"title": "Scalpel Safety", "content": "Handle scalpels with care and store them in a safe place away from children."},
        {"title": "Safe Lifting Techniques", "content": "Bend your knees, not your back, and lift with your legs to avoid injury."},
        {"title": "Personal Safety Devices", "content": "Consider carrying a personal alarm or pepper spray for self-defense."},
        {"title": "Disaster Kit Maintenance", "content": "Regularly check and update your disaster preparedness kit with fresh supplies."},
        {"title": "Workplace Fire Safety", "content": "Know the location of fire exits and fire extinguishers in your workplace."},
        {"title": "Cleaning Product Safety", "content": "Store cleaning products in a secure location and use them according to instructions."},
        {"title": "Travel Medication Safety", "content": "Carry necessary medications and keep them in their original packaging when traveling."},
        {"title": "Water Purification Safety", "content": "Use a water filter or boil water in emergencies to prevent waterborne illnesses."},
        {"title": "Jungle Safety", "content": "Wear long sleeves, trousers, and use insect repellent when trekking in the jungle."},
        {"title": "Safe Home Renovation", "content": "Wear protective gear and ensure proper ventilation when renovating at home."},
        {"title": "Carbon Footprint Reduction", "content": "Use energy-efficient appliances and reduce waste to help protect the environment."},
        {"title": "Personal Hygiene Safety", "content": "Avoid sharing personal items like towels or razors to reduce the spread of germs."},
        {"title": "Fire Exit Awareness", "content": "Know your nearest fire exit and evacuation routes in case of emergency."},
        {"title": "Playground Safety", "content": "Ensure playground equipment is safe, stable, and suitable for the child's age."},
        {"title": "Health Screening Safety", "content": "Regularly visit a healthcare provider for check-ups and screenings."},
        {"title": "Sun Exposure Protection", "content": "Limit sun exposure during peak hours (10 a.m. - 4 p.m.) and wear a hat."},
        {"title": "Smoke-Free Home", "content": "Make your home a smoke-free zone to protect your family's health."},
        {"title": "Road Rage Prevention", "content": "Stay calm on the road, avoid aggressive driving, and yield to others when necessary."},
        {"title": "Carbon Footprint Awareness", "content": "Opt for public transportation, cycling, or walking to reduce your carbon footprint."},
        {"title": "Portable Generator Safety", "content": "Use generators outdoors and away from windows to avoid carbon monoxide buildup."},
        {"title": "Recycling Safety", "content": "Ensure that you separate and dispose of hazardous materials properly."},
        {"title": "Swimming Pool Safety", "content": "Ensure pools are fenced and always supervise children around water."},
        {"title": "Eyewear Safety", "content": "Wear safety goggles when using power tools or engaging in hazardous activities."},
        {"title": "Nighttime Walking Safety", "content": "Wear reflective clothing and carry a flashlight if walking at night."},
        {"title": "Building Safety", "content": "Check that fire alarms and sprinklers are functional in any building you visit."},
        {"title": "Public Space Safety", "content": "Stay alert and avoid unfamiliar or poorly lit areas in public spaces."},
        {"title": "Traveling with Kids Safety", "content": "Use appropriate car seats and booster seats based on your child's size and age."},
        {"title": "Stair Safety", "content": "Install handrails and keep stairs well-lit and clutter-free."},
        {"title": "Biking in Traffic Safety", "content": "Always use bike lanes and signal turns to ensure your safety on the road."},
        {"title": "Cooking Oil Safety", "content": "Keep hot cooking oil away from children and never leave it unattended on the stove."},
        {"title": "Heat Exhaustion Prevention", "content": "Stay hydrated and take frequent breaks when working or exercising in hot weather."},
        {"title": "Defensive Driving", "content": "Keep a safe distance, check mirrors often, and be aware of surrounding traffic."},
        {"title": "Personal Device Safety", "content": "Use a password or biometric lock for your personal devices to prevent unauthorized access."},
        {"title": "Earthquake Safety", "content": "Drop, Cover, and Hold On during an earthquake to protect yourself from falling debris."},
        {"title": "Earthquake Safety", "content": "Move away from windows, heavy furniture, and anything that can fall or shatter."},
        {"title": "Earthquake Safety", "content": "After the quake, check for injuries and be prepared for aftershocks."},
        {"title": "Flood Safety", "content": "If there's a flood warning, move to higher ground immediately."},
        {"title": "Flood Safety", "content": "Never drive through flooded streets—just six inches of water can cause loss of control."},
        {"title": "Flood Safety", "content": "Keep a disaster kit with essentials such as food, water, and medications."},
        {"title": "Tornado Safety", "content": "Go to the basement or interior room on the lowest floor if you hear tornado sirens."},
        {"title": "Tornado Safety", "content": "Avoid windows and cover yourself with a heavy blanket or mattress."},
        {"title": "Tornado Safety", "content": "Stay tuned to weather alerts and be prepared to evacuate if necessary."},
        {"title": "Hurricane Safety", "content": "Know your evacuation routes and have an emergency kit ready."},
        {"title": "Hurricane Safety", "content": "Stay indoors during a hurricane and avoid windows and glass doors."},
        {"title": "Hurricane Safety", "content": "After the storm, be cautious of debris and flooding in your area."},
        {"title": "Wildfire Safety", "content": "Create defensible space around your home by clearing away dry brush and flammable materials."},
        {"title": "Wildfire Safety", "content": "Have an evacuation plan and ensure all family members are aware of it."},
        {"title": "Wildfire Safety", "content": "Stay indoors when smoke levels are high to avoid respiratory issues."},
        {"title": "Volcanic Eruption Safety", "content": "If you live near an active volcano, follow evacuation orders immediately."},
        {"title": "Volcanic Eruption Safety", "content": "Wear a mask to protect your lungs from ash inhalation."},
        {"title": "Volcanic Eruption Safety", "content": "Stay indoors to avoid ash falling, and keep windows and doors closed."},
        {"title": "Tsunami Safety", "content": "If you're near the coast and feel an earthquake, evacuate immediately to higher ground."},
        {"title": "Tsunami Safety", "content": "Tsunamis can arrive minutes after an earthquake, so don't wait for an official warning."},
        {"title": "Tsunami Safety", "content": "Avoid returning to the beach until officials declare it safe."},
        {"title": "Landslide Safety", "content": "Avoid building near steep hills or cliffs that are prone to landslides."},
        {"title": "Landslide Safety", "content": "If you notice signs of potential landslides (like cracks in the ground or leaning trees), evacuate immediately."},
        {"title": "Landslide Safety", "content": "After heavy rain, be aware of your surroundings and watch for sudden slope movements."},
        {"title": "Blizzard Safety", "content": "Stay indoors during a blizzard to avoid frostbite or hypothermia."},
        {"title": "Blizzard Safety", "content": "Ensure your car is winterized, and keep blankets, water, and food in your vehicle during winter months."},
        {"title": "Blizzard Safety", "content": "If you must travel, let someone know your route and expected arrival time."},
        {"title": "Extreme Heat Safety", "content": "Stay hydrated and wear light clothing to prevent heat exhaustion."},
        {"title": "Extreme Heat Safety", "content": "Avoid outdoor activities during peak heat hours (10 a.m. to 4 p.m.)."},
        {"title": "Extreme Heat Safety", "content": "Keep an eye on vulnerable people like the elderly, children, and pets."},
        {"title": "Zombie Apocalypse Safety", "content": "Secure your home with barricades, and keep escape routes clear in case of a sudden invasion."},
        {"title": "Zombie Apocalypse Safety", "content": "Always have a weapon or tool for self-defense (like a crowbar or baseball bat) to fend off zombies."},
        {"title": "Zombie Apocalypse Safety", "content": "Establish a trusted group for survival, but be cautious of potential betrayal."},
        {"title": "Alien Invasion Safety", "content": "Know the locations of safe houses or underground bunkers in case of a citywide evacuation."},
        {"title": "Alien Invasion Safety", "content": "If the aliens use mind-control devices, wear protective headgear to block transmissions."},
        {"title": "Alien Invasion Safety", "content": "Gather supplies like food, water, and electronics that can function without modern power grids."},
        {"title": "Robot Uprising Safety", "content": "Disable or disconnect all AI systems in your home and office to prevent robots from gaining control."},
        {"title": "Robot Uprising Safety", "content": "Use EMP devices to disrupt robots' electrical systems and stop their movements."},
        {"title": "Robot Uprising Safety", "content": "Form alliances with other survivors to share resources and defend key locations."},
        {"title": "Vampire Attack Safety", "content": "Carry garlic and silver to ward off vampires and avoid encounters at night."},
        {"title": "Vampire Attack Safety", "content": "Stay in well-lit areas during dusk and dawn, as vampires are weakened by sunlight."},
        {"title": "Vampire Attack Safety", "content": "If bitten, immediately seek help from a healer or vampire hunter to avoid turning."},
        {"title": "Time Travel Paradox Safety", "content": "Avoid altering significant events in history, as even small changes can have catastrophic consequences in the present."},
        {"title": "Time Travel Paradox Safety", "content": "Carry a device that can return you to your original time in case you are stuck in an alternate timeline."},
        {"title": "Time Travel Paradox Safety", "content": "Be cautious of future versions of yourself and any paradoxes that may arise."},
        {"title": "Superhero Battle Safety", "content": "Find shelter away from the battlegrounds, as collateral damage can be widespread during superhero fights."},
        {"title": "Superhero Battle Safety", "content": "Have a 'safe word' to signal when to evacuate quickly."},
        {"title": "Superhero Battle Safety", "content": "If you find yourself near a supervillain's lair, stay out of sight and avoid making contact."},
        {"title": "Giant Monster Attack Safety", "content": "Stay inside sturdy buildings or underground bunkers to avoid destruction from giant monsters."},
        {"title": "Giant Monster Attack Safety", "content": "If possible, track the monster's movements and plan an escape route to a safe zone."},
        {"title": "Giant Monster Attack Safety", "content": "Don't engage the monster; instead, let military forces or specialists handle the situation."},
        {"title": "Nuclear Winter Safety", "content": "Stockpile food, water, and radiation protection gear like lead-lined clothing and masks."},
        {"title": "Nuclear Winter Safety", "content": "Seek shelter underground or in fortified structures that can protect you from radioactive fallout."},
        {"title": "Nuclear Winter Safety", "content": "Only venture outside if absolutely necessary and always wear protective gear to minimize radiation exposure."},
        {"title": "Alien Invasion Safety", "content": "Stay in a group and trust no one unless they have proven their loyalty."}
    ]

    try:
        conn = connect_db()
        c = conn.cursor()

        # Insert the tips into the database
        c.executemany(
            'INSERT INTO tips (title, content) VALUES (?, ?)',
            [(tip['title'], tip['content']) for tip in safety_tips]
        )

        conn.commit()
        print(f"{len(safety_tips)} safety tips have been added to the database.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    initialize_database()
    add_safety_tips()
    print("Disaster safety tips added successfully!")