"""
Selenium Scraper for GitHub Actions - שולף את כל 168 הליגות בזהירות
"""

import json
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# כל 168 הליגות
ALL_LEAGUES = {
    637: 'נשים', 639: 'נשים', 741: 'נשים', 654: 'נשים', 651: 'נשים',
    641: 'נשים', 808: 'נשים', 860: 'נשים', 823: 'נשים', 809: 'נשים',
    859: 'נשים', 705: 'נשים', 815: 'נשים', 749: 'נשים', 717: 'נשים',
    900: 'נשים', 810: 'נשים', 901: 'נשים', 903: 'נשים', 902: 'נשים',
    101: 'נוער', 103: 'נוער', 102: 'נוער', 105: 'נוער', 104: 'נוער',
    920: 'נוער', 787: 'נוער', 666: 'נוער', 110: 'נוער', 115: 'נוער',
    726: 'נערים א\'', 121: 'נערים א\'', 120: 'נערים א\'', 646: 'נערים א\'',
    755: 'נערים א\'', 123: 'נערים א\'', 122: 'נערים א\'', 665: 'נערים א\'',
    664: 'נערים א\'',
    773: 'נערים ב\'', 719: 'נערים ב\'', 720: 'נערים ב\'', 135: 'נערים ב\'',
    139: 'נערים ב\'', 706: 'נערים ב\'', 131: 'נערים ב\'', 137: 'נערים ב\'',
    130: 'נערים ב\'', 658: 'נערים ב\'', 134: 'נערים ב\'',
    824: 'נערים ג\'', 845: 'נערים ג\'', 826: 'נערים ג\'', 736: 'נערים ג\'',
    663: 'נערים ג\'', 758: 'נערים ג\'', 759: 'נערים ג\'', 146: 'נערים ג\'',
    816: 'נערים ג\'', 707: 'נערים ג\'', 144: 'נערים ג\'',
    871: 'ילדים א\'', 155: 'ילדים א\'', 734: 'ילדים א\'', 870: 'ילדים א\'',
    648: 'ילדים א\'', 865: 'ילדים א\'', 764: 'ילדים א\'', 875: 'ילדים א\'',
    876: 'ילדים א\'', 662: 'ילדים א\'', 862: 'ילדים א\'', 152: 'ילדים א\'',
    156: 'ילדים א\'', 788: 'ילדים א\'', 150: 'ילדים א\'', 712: 'ילדים א\'',
    872: 'ילדים א\'', 863: 'ילדים א\'', 158: 'ילדים א\'', 154: 'ילדים א\'',
    861: 'ילדים א\'',
    880: 'ילדים ב\'', 739: 'ילדים ב\'', 748: 'ילדים ב\'', 689: 'ילדים ב\'',
    852: 'ילדים ב\'', 868: 'ילדים ב\'', 804: 'ילדים ב\'', 881: 'ילדים ב\'',
    882: 'ילדים ב\'', 897: 'ילדים ב\'', 161: 'ילדים ב\'', 165: 'ילדים ב\'',
    792: 'ילדים ב\'', 879: 'ילדים ב\'', 160: 'ילדים ב\'', 747: 'ילדים ב\'',
    767: 'ילדים ב\'', 878: 'ילדים ב\'', 167: 'ילדים ב\'', 163: 'ילדים ב\'',
    877: 'ילדים ב\'', 765: 'ילדים ב\'',
    886: 'ילדים ג\'', 887: 'ילדים ג\'', 175: 'ילדים ג\'', 713: 'ילדים ג\'',
    769: 'ילדים ג\'', 890: 'ילדים ג\'', 888: 'ילדים ג\'', 770: 'ילדים ג\'',
    883: 'ילדים ג\'', 884: 'ילדים ג\'', 794: 'ילדים ג\'', 738: 'ילדים ג\'',
    173: 'ילדים ג\'', 793: 'ילדים ג\'', 744: 'ילדים ג\'', 170: 'ילדים ג\'',
    172: 'ילדים ג\'', 885: 'ילדים ג\'', 891: 'ילדים ג\'', 174: 'ילדים ג\'',
    892: 'ילדים ג\'', 661: 'ילדים ג\'', 780: 'ילדים ג\'', 750: 'ילדים ג\'',
    649: 'ילדים ג\'',
    908: 'טרום ילדים א\'', 182: 'טרום ילדים א\'', 631: 'טרום ילדים א\'',
    737: 'טרום ילדים א\'', 838: 'טרום ילדים א\'', 771: 'טרום ילדים א\'',
    819: 'טרום ילדים א\'', 180: 'טרום ילדים א\'', 710: 'טרום ילדים א\'',
    183: 'טרום ילדים א\'', 801: 'טרום ילדים א\'', 799: 'טרום ילדים א\'',
    840: 'טרום ילדים א\'', 800: 'טרום ילדים א\'', 904: 'טרום ילדים א\'',
    660: 'טרום ילדים א\'', 839: 'טרום ילדים א\'', 181: 'טרום ילדים א\'',
    806: 'טרום ילדים א\'', 752: 'טרום ילדים א\'',
    640: 'טרום ילדים ב\'', 732: 'טרום ילדים ב\'', 912: 'טרום ילדים ב\'',
    913: 'טרום ילדים ב\'', 843: 'טרום ילדים ב\'', 798: 'טרום ילדים ב\'',
    659: 'טרום ילדים ב\'', 851: 'טרום ילדים ב\'', 657: 'טרום ילדים ב\'',
    844: 'טרום ילדים ב\'', 921: 'טרום ילדים ב\'', 922: 'טרום ילדים ב\'',
    842: 'טרום ילדים ב\'', 186: 'טרום ילדים ב\'', 918: 'טרום ילדים ב\'',
    722: 'טרום ילדים ב\'',
    795: 'טרום ילדים ג\'', 652: 'טרום ילדים ג\'', 916: 'טרום ילדים ג\''
}

SEASON_ID = 27

class LeaguesScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Anti-detection (כמו בגביעים!)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # הסתר שזה Selenium
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.all_tables = []
    
    def scrape_league(self, league_id, age_group):
        """שלוף ליגה בודדת"""
        url = f"https://www.football.org.il/leagues/league/?league_id={league_id}&season_id={SEASON_ID}"
        
        try:
            self.driver.get(url)
            
            # המתן קצת (נראה אנושי)
            time.sleep(random.uniform(2, 4))
            
            # חכה לטבלה
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.table_row'))
                )
            except:
                print(f"⚠️  {league_id}: לא נמצאה טבלה")
                return None
            
            # שם ליגה
            try:
                h1 = self.driver.find_element(By.TAG_NAME, 'h1')
                league_name = h1.text.strip()
                if '2025/2026' in league_name:
                    league_name = league_name.split('\n')[-1].strip()
            except:
                league_name = f"ליגה {league_id}"
            
            # שורות טבלה
            table_rows = self.driver.find_elements(By.CSS_SELECTOR, 'a.table_row')
            
            teams = []
            for row in table_rows:
                try:
                    place_div = row.find_element(By.CSS_SELECTOR, '.table_col.place')
                    team_div = row.find_element(By.CSS_SELECTOR, '.table_col.team_name')
                    
                    if not place_div or not team_div:
                        continue
                    
                    place = place_div.text.strip()
                    team_name = team_div.text.strip().replace('קבוצה', '').strip()
                    
                    cols = row.find_elements(By.CSS_SELECTOR, '.table_col.ltr')
                    
                    if len(cols) >= 6:
                        teams.append({
                            'place': int(place) if place.isdigit() else place,
                            'teamName': team_name,
                            'games': int(cols[0].text.strip() or 0),
                            'wins': int(cols[1].text.strip() or 0),
                            'draws': int(cols[2].text.strip() or 0),
                            'losses': int(cols[3].text.strip() or 0),
                            'goals': cols[4].text.strip(),
                            'points': int(cols[5].text.strip() or 0)
                        })
                except:
                    continue
            
            if teams:
                print(f"✅ {league_id}: {league_name} - {len(teams)} קבוצות")
                return {
                    'leagueId': league_id,
                    'leagueName': league_name,
                    'ageGroup': age_group,
                    'teams': teams,
                    'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                print(f"⚠️  {league_id}: {league_name} - אין קבוצות")
                return None
                
        except Exception as e:
            print(f"❌ {league_id}: {str(e)[:60]}")
            return None
    
    def scrape_all(self):
        """שלוף את כל 168 הליגות"""
        print(f"\n🏆 מתחיל שליפת {len(ALL_LEAGUES)} ליגות")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⚡ אסטרטגיה: לאט וזהיר (anti-detection)")
        print("="*60)
        
        for i, (league_id, age_group) in enumerate(ALL_LEAGUES.items(), 1):
            result = self.scrape_league(league_id, age_group)
            if result:
                self.all_tables.append(result)
            
            # התקדמות
            if i % 20 == 0:
                print(f"📊 התקדמות: {i}/{len(ALL_LEAGUES)} - {len(self.all_tables)} הצליחו")
                # הפסקה ארוכה יותר
                time.sleep(random.uniform(3, 5))
            else:
                # המתן בין ליגות
                time.sleep(random.uniform(2, 3))
        
        print("="*60)
        print(f"✅ סיום! {len(self.all_tables)}/{len(ALL_LEAGUES)} ליגות נשלפו")
        
        return self.all_tables
    
    def save_json(self, filename='leagues_tables.json'):
        """שמור JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_tables, f, ensure_ascii=False, indent=2)
        print(f"💾 נשמר: {filename}")
    
    def close(self):
        """סגור דפדפן"""
        self.driver.quit()


def main():
    scraper = LeaguesScraper()
    
    try:
        scraper.scrape_all()
        scraper.save_json()
    except Exception as e:
        print(f"\n❌ שגיאה כללית: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
