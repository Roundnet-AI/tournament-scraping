from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
import time
import json
from pathlib import Path
from tqdm import tqdm
import requests

class UnixMonths():
    def __init__(self):
        self.data = [
            {"start": 1682924400000, "end": 1685602799999, "month": "may", "year": 2023},
            {"start": 1680332400000, "end": 1682924399999, "month": "april", "year": 2023},
            {"start": 1677657600000, "end": 1680332399999, "month": "march", "year": 2023},
            {"start": 1675238400000, "end": 1677657599999, "month": "february", "year": 2023},
            {"start": 1672560000000, "end": 1675238399999, "month": "january", "year": 2023},
            {"start": 1669881600000, "end": 1672560000000, "month": "december", "year": 2022},
            {"start": 1667286000000, "end": 1669881599999, "month": "november", "year": 2022},
            {"start": 1664607600000, "end": 1667285999999, "month": "october", "year": 2022},
            {"start": 1662015600000, "end": 1664607599999, "month": "september", "year": 2022},
            {"start": 1659337200000, "end": 1662015599999, "month": "august", "year": 2022},
            {"start": 1656658800000, "end": 1659337199999, "month": "july", "year": 2022},
            {"start": 1654066800000, "end": 1656658799999, "month": "june", "year": 2022},
            {"start": 1651388400000, "end": 1654066799999, "month": "may", "year": 2022},
            {"start": 1648796400000, "end": 1651388399999, "month": "april", "year": 2022},
            {"start": 1646121600000, "end": 1648796399999, "month": "march", "year": 2022},
            {"start": 1643702400000, "end": 1646121599999, "month": "february", "year": 2022},
            {"start": 1641024000000, "end": 1643702399999, "month": "january", "year": 2022},
            {"start": 1638345600000, "end": 1641023999999, "month": "december", "year": 2021},
            {"start": 1635750000000, "end": 1638345599999, "month": "november", "year": 2021},
            {"start": 1633071600000, "end": 1635750000000, "month": "october", "year": 2021},
            {"start": 1630479600000, "end": 1633071599999, "month": "september", "year": 2021},
            {"start": 1627801200000, "end": 1630479599999, "month": "august", "year": 2021},
            {"start": 1625122800000, "end": 1627801199999, "month": "july", "year": 2021},
            {"start": 1622530800000, "end": 1625122799999, "month": "june", "year": 2021},
            {"start": 1619852400000, "end": 1622530799999, "month": "may", "year": 2021},
            {"start": 1617260400000, "end": 1619852399999, "month": "april", "year": 2021},
            {"start": 1614585600000, "end": 1617260399999, "month": "march", "year": 2021},
            {"start": 1612166400000, "end": 1614585599999, "month": "february", "year": 2021},
            {"start": 1609488000000, "end": 1612166399999, "month": "january", "year": 2021},
            {"start": 1606809600000, "end": 1609487999999, "month": "december", "year": 2020},
            {"start": 1604214000000, "end": 1606809599999, "month": "november", "year": 2020},
            {"start": 1601535600000, "end": 1604213999999, "month": "october", "year": 2020},
            {"start": 1598943600000, "end": 1601535599999, "month": "september", "year": 2020},
            {"start": 1596265200000, "end": 1598943599999, "month": "august", "year": 2020},
            {"start": 1593586800000, "end": 1596265199999, "month": "july", "year": 2020},
            {"start": 1590994800000, "end": 1593586799999, "month": "june", "year": 2020},
            {"start": 1588316400000, "end": 1590994799999, "month": "may", "year": 2020},
            {"start": 1585724400000, "end": 1588316399999, "month": "april", "year": 2020},
            {"start": 1583049600000, "end": 1585724399999, "month": "march", "year": 2020},
            {"start": 1580544000000, "end": 1583049599999, "month": "february", "year": 2020},
            {"start": 1577865600000, "end": 1580543999999, "month": "january", "year": 2020},
        ]

class RoundnetScrapingClient():
    def __init__(self, url: str):
        self.url = url
        self.tournaments = []

    def scrape(self, **kwargs):
        tournaments_filename = kwargs.get("tournaments_filename", "tournaments.json")
        try:
            self.get_tournaments(
                start=kwargs.get("start", 0),
                end=kwargs.get("end", 0),
            )
        except Exception as e:
            self.save_tournaments(tournaments_filename)
            raise e
        self.save_tournaments(tournaments_filename)

    def save_tournaments(self, filename: str="tournaments.json"):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.tournaments, f, indent=4)

class RequestsClient(RoundnetScrapingClient):
    def __init__(self, url: str):
        super().__init__(url)

    def _get(self, url: str):
        return requests.get(url).json()

class SeleniumClient(RoundnetScrapingClient):
    def __init__(self, url: str):
        super().__init__(url)
        self._driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self._driver.maximize_window()
        self._driver.implicitly_wait(2)

    def _scroll_to_bottom(self, and_back: bool = False):
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if and_back:
            self._driver.execute_script("window.scrollTo(0, 0);")

class FwangoClient(SeleniumClient):
    def __init__(self):
        super().__init__("https://fwango.io/")

    def get_tournaments(self, start: int = 0, end: int = 0, page: int = 1, sport: str = "roundnet", location: int = 0):
        """Return all tournaments between start and end date.

        Args:
            start (int): Start time in unix time. Defaults to 0.
            end (int): End time in unix time. Defaults to 0.
            page (int, optional): Page number. Defaults to 1.
            sport (str, optional): Sport to filter by. Defaults to "roundnet".
            location (int, optional): Location to filter by. Defaults to 0.
        """
        base_url = self.url + "/dashboard?sport={sport}&location={location}&period=custom&start={start}&end={end}&page={page}"
        url = base_url.format(sport=sport, location=location, start=start, end=end, page=page)
        self._driver.get(url)
        self._driver.implicitly_wait(5)
        self._scroll_to_bottom()
        try:
            result_count = self._driver.find_element(By.CLASS_NAME, "result-count").text
            result_count = int(''.join(c for c in result_count if c.isdigit()))
        except NoSuchElementException:
            result_count = 0
        pbar = tqdm(total=result_count)
        while len(self.tournaments) < result_count:
            self._scroll_to_bottom()
            tournaments_on_page = self._driver.find_elements(By.CLASS_NAME, "TournamentCard__InfoContainer-sc-luwbjz-1.eBszzz")
            for tournament in tournaments_on_page:
                date = tournament.find_element(By.CLASS_NAME, "date").text
                tournament_name = tournament.find_element(By.CLASS_NAME, "name").text
                geo = tournament.find_element(By.CLASS_NAME, "location").text
                try:
                    competitors = int(tournament.find_element(By.CLASS_NAME, "Box-sc-1xxy44l-0.Badge__BadgeContainer-sc-1yfpay5-0.kBPMgy.ihxfpj").text)
                except:
                    competitors = None
                tournament_url = tournament.find_element(By.XPATH, "..").get_attribute("href")
                players = self.get_players(tournament_url)
                self.tournaments.append({
                    "date": date,
                    "name": tournament_name,
                    "location": geo,
                    "competitors": competitors,
                    "url": tournament_url,
                    "players": players,
                })
                pbar.update()
            page += 1
            url = base_url.format(sport=sport, location=location, start=start, end=end, page=page)
            self._driver.get(url)
            self._driver.implicitly_wait(5)
        pbar.close()

    def get_players(self, url: str) -> "list[str]":
        self._driver.execute_script("window.open('');")
        self._driver.switch_to.window(self._driver.window_handles[1])
        self._driver.get(url)
        self._driver.implicitly_wait(5)
        teams_with_dupes = []
        while True:
            visible_teams = self._driver.find_elements(By.CLASS_NAME, "players")
            if len(visible_teams) == 0 or visible_teams[-1].text in teams_with_dupes:
                break
            teams_with_dupes.extend([p.text for p in visible_teams])
            self._driver.execute_script("arguments[0].scrollIntoView(true);", visible_teams[-1])
            time.sleep(.5)
        split = [t.split(" and ") for t in teams_with_dupes]
        players = {p.lower() for t in split for p in t}
        self._driver.close()
        self._driver.switch_to.window(self._driver.window_handles[0])
        return list(players)

    def save_tournaments(self, filename: str = "data/fwango_tournaments.json"):
        return super().save_tournaments(filename)

class ClickNRunClient(RequestsClient):
    def __init__(self):
        super().__init__("https://clickn.run/")

    def get_tournaments(self, **kwargs):
        base_url = self.url + "api/competitions?query=raceAggregationDetails.trackTypes.subtype:eq:roundnet&projection=coreDetails,raceAggregationDetails"
        response = self._get(base_url)
        for tournament in tqdm(response["competitions"]):
            location = None
            if "location" in tournament["coreDetails"]:
                location = tournament["coreDetails"]["location"]
                location = f"{location['locality']}, {location['administrativeArea']}, {location['country']}"
            event_id = f"{tournament['_id']['baseCompetitionId']}/{tournament['_id']['editionId']}"
            players = self.get_players(event_id)
            self.tournaments.append({
                "date": tournament["coreDetails"]["dateRange"]["start"],
                "name": tournament["coreDetails"]["name"],
                "location": location,
                "competitors": tournament["raceAggregationDetails"]["registrationsSummary"]["participants"]["current"],
                "url": f"{self.url}en/events/{event_id}",
                "players": players
            })

    def get_players(self, event_id: str) -> "list[str]":
        base_url = self.url + f"api/competitions/{event_id}?projection=_id,mass"
        response = self._get(base_url)
        players = []
        for _, player in response["mass"]["participants"].items():
            try:
                last_name = player["coreDetails"]["lastName"].lower()
                first_name = player["coreDetails"]["firstName"].lower()
            except KeyError:
                continue
            full_name = f"{first_name} {last_name}"
            players.append(full_name)
        return players

    def save_tournaments(self, filename: str = "data/clicknrun_tournaments.json"):
        return super().save_tournaments(filename)

class PlayerZoneClient(SeleniumClient):
    def __init__(self):
        super().__init__("https://playerzone.roundnetgermany.de/tournaments")

    def get_tournaments(self, **kwargs):
        self._driver.get(self.url)
        self._driver.implicitly_wait(5)
        self._driver.find_element(By.XPATH, "//*[@id='tournaments']/div/div[1]/div[2]/a/span").click()
        # Select "All" from the dropdown (//*[@id="id_region_container"]/div)
        self._driver.find_element(By.XPATH, "//*[@id='id_region_container']/div").click()
        self._driver.find_element(By.XPATH, "//*[@id='id_region_container']/div/div[2]/div[3]").click()
        self._driver.find_element(By.XPATH, "//*[@id='filter-form']/div[3]/button").click()
        self._driver.implicitly_wait(5)
        pagination = self._driver.find_elements(By.XPATH, "//*[@id='tournaments']/ul[2]")
        pages = int(pagination[0].text.split(" ")[-2])
        for page in tqdm(range(1, pages + 1)):
            url = f"{self.url}?page={page}"
            self._driver.get(url)
            self._driver.implicitly_wait(5)
            self._scroll_to_bottom()
            tournaments = self._driver.find_elements(By.XPATH, "//*[@id='tournaments']/ul[1]")
            for tournament in tournaments:
                date_geo = tournament.find_element(By.CLASS_NAME, "tournament-date").text
                date = date_geo.split(", ")[0]
                geo = date_geo.split(", ")[1]
                tournament_name = tournament.find_element(By.CLASS_NAME, "tournament-title").text
                competitors = int(tournament.find_element(By.CLASS_NAME, "tournament-team-count").text.split(" ")[1].split("/")[0])
                self.tournaments.append({
                    "date": date,
                    "name": tournament_name,
                    "location": geo,
                    "competitors": competitors * 2,
                    "url": None,
                    "players": None,
                })

    def save_tournaments(self, filename: str = "data/playerzone_tournaments.json"):
        return super().save_tournaments(filename)
        

if __name__ == "__main__":
    # client = ClickNRunClient()
    # client.scrape(
    #     tournaments_filename="data/clicknrun_tournaments_20230620.json",
    # )

    # client = PlayerZoneClient()
    # client.scrape(
    #     tournaments_filename="data/playerzone_tournaments_20230620.json",
    # )

    client = FwangoClient()
    client.scrape(
        start=1577865600000,
        tournaments_filename="data/fwango_tournaments_20230620.json",
    )
