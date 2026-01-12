"""
Leagues Tables Scraper - שולף טבלאות דירוג של כל הליגות
"""

import os
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# כל 202 הליגות שלנו (מהקוד המקורי)
ALL_LEAGUES = {
    # נשים (20)
    637: 'נשים', 639: 'נשים', 741: 'נשים', 654: 'נשים', 651: 'נשים', 
    641: 'נשים', 808: 'נשים', 860: 'נשים', 823: 'נשים', 809: 'נשים', 
    859: 'נשים', 705: 'נשים', 815: 'נשים', 749: 'נשים', 717: 'נשים', 
    900: 'נשים', 810: 'נשים', 901: 'נשים', 903: 'נשים', 902: 'נשים',
    
    # נוער (10)
    101: 'נוער', 103: 'נוער', 102: 'נוער', 105: 'נוער', 104: 'נוער', 
    920: 'נוער', 787: 'נוער', 666: 'נוער', 110: 'נוער', 115: 'נוער',
    
    # נערים א' (9)
    726: 'נערים א\'', 121: 'נערים א\'', 120: 'נערים א\'', 646: 'נערים א\'', 
    755: 'נערים א\'', 123: 'נערים א\'', 122: 'נערים א\'', 665: 'נערים א\'', 
    664: 'נערים א\'',
    
    # נערים ב' (11)
    773: 'נערים ב\'', 719: 'נערים ב\'', 720: 'נערים ב\'', 135: 'נערים ב\'', 
    139: 'נערים ב\'', 706: 'נערים ב\'', 131: 'נערים ב\'', 137: 'נערים ב\'', 
    130: 'נערים ב\'', 658: 'נערים ב\'', 134: 'נערים ב\'',
    
    # נערים ג' (11)
    824: 'נערים ג\'', 845: 'נערים ג\'', 826: 'נערים ג\'', 736: 'נערים ג\'', 
    663: 'נערים ג\'', 758: 'נערים ג\'', 759: 'נערים ג\'', 146: 'נערים ג\'', 
    816: 'נערים ג\'', 707: 'נערים ג\'', 144: 'נערים ג\'',
    
    # ילדים א' (21)
    871: 'ילדים א\'', 155: 'ילדים א\'', 734: 'ילדים א\'', 870: 'ילדים א\'', 
    648: 'ילדים א\'', 865: 'ילדים א\'', 764: 'ילדים א\'', 875: 'ילדים א\'', 
    876: 'ילדים א\'', 662: 'ילדים א\'', 862: 'ילדים א\'', 152: 'ילדים א\'', 
    156: 'ילדים א\'', 788: 'ילדים א\'', 150: 'ילדים א\'', 712: 'ילדים א\'', 
    872: 'ילדים א\'', 863: 'ילדים א\'', 158: 'ילדים א\'', 154: 'ילדים א\'', 
    861: 'ילדים א\'',
    
    # ילדים ב' (22)
    880: 'ילדים ב\'', 739: 'ילדים ב\'', 748: 'ילדים ב\'', 689: 'ילדים ב\'', 
    852: 'ילדים ב\'', 868: 'ילדים ב\'', 804: 'ילדים ב\'', 881: 'ילדים ב\'', 
    882: 'ילדים ב\'', 897: 'ילדים ב\'', 161: 'ילדים ב\'', 165: 'ילדים ב\'', 
    792: 'ילדים ב\'', 879: 'ילדים ב\'', 160: 'ילדים ב\'', 747: 'ילדים ב\'', 
    767: 'ילדים ב\'', 878: 'ילדים ב\'', 167: 'ילדים ב\'', 163: 'ילדים ב\'', 
    877: 'ילדים ב\'', 765: 'ילדים ב\'',
    
    # ילדים ג' (25)
    886: 'ילדים ג\'', 887: 'ילדים ג\'', 175: 'ילדים ג\'', 713: 'ילדים ג\'', 
    769: 'ילדים ג\'', 890: 'ילדים ג\'', 888: 'ילדים ג\'', 770: 'ילדים ג\'', 
    883: 'ילדים ג\'', 884: 'ילדים ג\'', 794: 'ילדים ג\'', 738: 'ילדים ג\'', 
    173: 'ילדים ג\'', 793: 'ילדים ג\'', 744: 'ילדים ג\'', 170: 'ילדים ג\'', 
    172: 'ילדים ג\'', 885: 'ילדים ג\'', 891: 'ילדים ג\'', 174: 'ילדים ג\'', 
    892: 'ילדים ג\'', 661: 'ילדים ג\'', 780: 'ילדים ג\'', 750: 'ילדים ג\'', 
    649: 'ילדים ג\'',
    
    # טרום ילדים א' (20)
    908: 'טרום ילדים א\'', 182: 'טרום ילדים א\'', 631: 'טרום ילדים א\'', 
    737: 'טרום ילדים א\'', 838: 'טרום ילדים א\'', 771: 'טרום ילדים א\'', 
    819: 'טרום ילדים א\'', 180: 'טרום ילדים א\'', 710: 'טרום ילדים א\'', 
    183: 'טרום ילדים א\'', 801: 'טרום ילדים א\'', 799: 'טרום ילדים א\'', 
    840: 'טרום ילדים א\'', 800: 'טרום ילדים א\'', 904: 'טרום ילדים א\'', 
    660: 'טרום ילדים א\'', 839: 'טרום ילדים א\'', 181: 'טרום ילדים א\'', 
    806: 'טרום ילדים א\'', 752: 'טרום ילדים א\'',
    
    # טרום ילדים ב' (16)
    640: 'טרום ילדים ב\'', 732: 'טרום ילדים ב\'', 912: 'טרום ילדים ב\'', 
    913: 'טרום ילדים ב\'', 843: 'טרום ילדים ב\'', 798: 'טרום ילדים ב\'', 
    659: 'טרום ילדים ב\'', 851: 'טרום ילדים ב\'', 657: 'טרום ילדים ב\'', 
    844: 'טרום ילדים ב\'', 921: 'טרום ילדים ב\'', 922: 'טרום ילדים ב\'', 
    842: 'טרום ילדים ב\'', 186: 'טרום ילדים ב\'', 918: 'טרום ילדים ב\'', 
    722: 'טרום ילדים ב\'',
    
    # טרום ילדים ג' (3)
    795: 'טרום ילדים ג\'', 652: 'טרום ילדים ג\'', 916: 'טרום ילדים ג\''
}

# סה"כ: 20+10+9+11+11+21+22+25+20+16+3 = 168 ליגות

SEASON_ID = 27

class LeaguesTablesScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Anti-detection: נראה כמו משתמש אמיתי
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent אמיתי
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # הסתר שאנחנו Selenium
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.all_tables = []
    
    def scrape_league_table(self, league_id, age_group):
        """שלוף טבלת דירוג של ליגה בודדת"""
        url = f"https://www.football.org.il/leagues/league/?league_id={league_id}&season_id={SEASON_ID}"
        
        try:
            self.driver.get(url)
            
            # המתן זמן אקראי (בין 3-5 שניות) - נראה אנושי ונותן זמן לטעינה!
            import random
            wait_time = random.uniform(3, 5)
            time.sleep(wait_time)
            
            # המתן עד שהטבלה באמת נטענת
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            try:
                # חכה עד 10 שניות שיופיע a.table_row
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.table_row'))
                )
                print(f"   ⏳ טבלה נטענה בהצלחה")
            except:
                print(f"   ⚠️  טבלה לא נטענה תוך 10 שניות")
                # ננסה בכל זאת...
            
            # קבל את שם הליגה
            try:
                league_name_elem = self.driver.find_element(By.TAG_NAME, 'h1')
                league_name = league_name_elem.text.strip()
                
                # נקה את שם הליגה
                if '2025/2026' in league_name:
                    parts = league_name.split('\n')
                    league_name = parts[-1] if len(parts) > 1 else league_name
            except:
                print(f"⚠️  League {league_id}: לא נמצא שם ליגה")
                return None
            
            # מצא את הטבלה
            teams = []
            try:
                # DEBUG: נראה מה באמת יש בדף
                page_source = self.driver.page_source
                
                # בדוק אם יש בכלל טבלה
                if 'table_row' not in page_source:
                    print(f"   ❌ אין 'table_row' בדף!")
                    if 'bindData' in page_source:
                        print(f"   📌 יש 'bindData' - הדף נטען אבל הטבלה לא")
                    return None
                
                print(f"   ✓ הדף מכיל 'table_row'")
                
                # נסה מספר selectors שונים
                selectors = [
                    'a.table_row',
                    '.table_row.link_url',
                    'a[href*="team-details"]',
                    '.league-table a.table_row',
                    '.table_view a.table_row'
                ]
                
                for selector in selectors:
                    table_rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if table_rows:
                        print(f"   ✅ נמצאו {len(table_rows)} שורות עם selector: {selector}")
                        break
                else:
                    print(f"   ❌ לא נמצאו שורות עם אף selector!")
                    return None
                
                # סנן רק שורות עם team_name (זה הטבלה האמיתית)
                valid_rows = []
                for row in table_rows:
                    try:
                        # בדוק אם יש team_name בשורה
                        row.find_element(By.CSS_SELECTOR, '.table_col.team_name')
                        valid_rows.append(row)
                    except:
                        continue
                
                print(f"   ✅ שורות טבלה תקינות: {len(valid_rows)}")
                
                if not valid_rows:
                    print(f"   ⚠️  לא נמצאו שורות עם team_name")
                    return None
                
                for row in valid_rows:
                    try:
                        # מיקום
                        place_elem = row.find_element(By.CSS_SELECTOR, '.table_col.place')
                        place = place_elem.text.strip()
                        
                        # שם קבוצה
                        team_name_elem = row.find_element(By.CSS_SELECTOR, '.table_col.team_name')
                        team_name = team_name_elem.text.strip()
                        if team_name.startswith('קבוצה'):
                            team_name = team_name.replace('קבוצה', '', 1).strip()
                        
                        # כל העמודות
                        cols = row.find_elements(By.CSS_SELECTOR, '.table_col.ltr')
                        
                        if len(cols) >= 7:
                            games = cols[0].text.strip()
                            wins = cols[1].text.strip()
                            draws = cols[2].text.strip()
                            losses = cols[3].text.strip()
                            goals = cols[4].text.strip()
                            points = cols[5].text.strip()
                            
                            teams.append({
                                'place': int(place) if place.isdigit() else place,
                                'teamName': team_name,
                                'games': int(games) if games.isdigit() else 0,
                                'wins': int(wins) if wins.isdigit() else 0,
                                'draws': int(draws) if draws.isdigit() else 0,
                                'losses': int(losses) if losses.isdigit() else 0,
                                'goals': goals,
                                'points': int(points) if points.isdigit() else 0
                            })
                    except:
                        continue
                
                if teams:
                    league_data = {
                        'leagueId': league_id,
                        'leagueName': league_name,
                        'ageGroup': age_group,
                        'teams': teams,
                        'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    self.all_tables.append(league_data)
                    print(f"✅ League {league_id}: {league_name} - {len(teams)} קבוצות")
                    return league_data
                else:
                    print(f"⚠️  League {league_id}: {league_name} - לא נמצאו שורות טבלה (אולי אין משחקים עדיין)")
                    return None
                    
            except Exception as e:
                print(f"❌ League {league_id}: שגיאה בשליפת טבלה - {str(e)[:100]}")
                return None
                
        except Exception as e:
            print(f"❌ League {league_id}: שגיאה כללית - {e}")
            return None
    
    def scrape_all_leagues(self):
        """שלוף את כל הטבלאות"""
        print(f"\n📊 מתחיל שליפת {len(ALL_LEAGUES)} טבלאות ליגה...")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        import random
        
        for i, (league_id, age_group) in enumerate(ALL_LEAGUES.items(), 1):
            self.scrape_league_table(league_id, age_group)
            
            if i % 20 == 0:
                print(f"📍 התקדמות: {i}/{len(ALL_LEAGUES)} ליגות - {len(self.all_tables)} טבלאות נשלפו")
                # הפסקה ארוכה יותר כל 20 ליגות
                wait_time = random.uniform(3, 5)
                print(f"   💤 מנוחה קצרה ({wait_time:.1f} שניות)...")
                time.sleep(wait_time)
            else:
                # הפסקה אקראית בין ליגות (1-2 שניות)
                time.sleep(random.uniform(1, 2))
        
        print("="*60)
        print(f"✅ סיום! סה\"כ {len(self.all_tables)} טבלאות נשלפו")
        
        return self.all_tables
    
    def save_to_json(self, filename='leagues_tables.json'):
        """שמור את כל הטבלאות ל-JSON"""
        if not self.all_tables:
            print("⚠️  אין נתונים לשמירה!")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_tables, f, ensure_ascii=False, indent=2)
        
        print(f"💾 הקובץ {filename} נשמר!")
        print(f"📊 סה\"כ {len(self.all_tables)} טבלאות ליגה")
    
    def close(self):
        self.driver.quit()


def main():
    """פונקציה ראשית"""
    print(f"\n🏆 שולף טבלאות דירוג של כל הליגות")
    print(f"📅 עונת 2025/2026")
    print("="*60)
    
    scraper = LeaguesTablesScraper()
    
    try:
        # שלוף את כל הטבלאות
        scraper.scrape_all_leagues()
        
        # שמור ל-JSON
        scraper.save_to_json('leagues_tables.json')
        
    except Exception as e:
        print(f"\n❌ שגיאה כללית: {e}")
    
    finally:
        scraper.close()
        print(f"\n✅ סיום תהליך")


if __name__ == "__main__":
    main()
