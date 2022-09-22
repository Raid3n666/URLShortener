import sqlite3
import requests

con = sqlite3.connect('urls.db', check_same_thread = False)

cur = con.cursor()

class URL:

    def __init__(self, target = '', url = '') -> None:
        self.target = target
        self.url = url
        cur.execute('CREATE TABLE IF NOT EXISTS urls (target TEXT ,shortUrl TEXT)')
    
    def add(self):
        if self.is_valid():
            cur.execute(f'INSERT INTO urls VALUES ("{self.target}", "{self.url}")')
            con.commit()
            return True
        else:
            return False
    
    def get_existing(self):
        res = cur.execute(f'SELECT shortUrl FROM urls WHERE target = "{self.target}"')
        result = res.fetchone()
        result = str(result)
        result = result.strip("('',)")
        return result
    
    def is_valid(self):
        valid = False
        try:
            rq = requests.get(f'{self.target}')
            if rq.status_code == 200:
                valid = True
            else:
                valid = False
        except:
            valid = False
        return valid
    
    def get_target(self):
        res = cur.execute(f'SELECT target FROM urls WHERE shortUrl = "{self.url}"')
        result = res.fetchone()
        result = str(result)
        result = result.strip("('',)")
        return result
 
    
class DAL:

    def __init__(self,) -> None:
        cur.execute('CREATE TABLE IF NOT EXISTS urls (target TEXT ,shortUrl TEXT)')
    
    def list_all_targets(self):
        results_list = []
        res = cur.execute('SELECT target FROM urls')
        results = res.fetchall()
        for result in results:
            result = str(result)
            result = result.strip("('',)")
            results_list.append(result)
        return results_list
    
    def list_all_urls(self):
        object_list = self.get_all_objects()
        urls_list = []
        for i in object_list:
            urls_list.append(i.url)
        return urls_list
    
    def custom_url_check(self, url):
        status = 'pass'
        if url in self.list_all_urls():
            status = 'URL already exists.'
        if url.isdigit():
            status = 'URL must contain characters.'
        if len(url) < 4:
            status = 'URL must be at least 4 characters.'
        if len(url) > 12:
            status = "URL must not be longer than 12 characters."
        return status

    def get_all_objects(self):
        obj_list = []
        res = cur.execute('SELECT * FROM urls')
        results = res.fetchall()
        results = list(results)
        for item in results:
            url = URL(item[0], item[1])
            obj_list.append(url)
        return obj_list