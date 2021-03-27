import mysql.connector
from mysql.connector import errorcode
from os import environ
from typing import Union

TABLES = {
    "pages": (
        "CREATE TABLE 'page_urls' ("
        "  'id' int(6) NOT_NULL AUTO_INCREMENT,"
        "  'url' char(255) NOT_NULL,"
        "  'downloaded' tinyint(1) DEFAULT 0,"
        "  'parsed' tinyint(1) DEFAULT 0,"
        "  PRIMARY_KEY ('id')"
        ") ENGINE=InnoDB"
    ),
    "flags": (
        "CREATE TABLE 'page_urls' ("
        "  'id' int(6) NOT_NULL AUTO_INCREMENT,"
        "  'url' char(255) NOT_NULL,"
        "  'dl_url' char(255) NOT_NULL,"
        "  'downloaded' tinyint(1) DEFAULT 0,"
        "  PRIMARY_KEY ('id')"
        ") ENGINE=InnoDB"
    ),
    "encounters": (
        "CREATE TABLE 'encounters' ("
        "  'id' int(6) NOT_NULL AUTO_INCREMENT,"
        "  'flag' int(6) NOT_NULL,"
        "  'dl' (6) NOT_NULL,"
        "  PRIMARY_KEY ('id')"
        ") ENGINE=InnoDB"
    )
}

class MySqlInterface:

    def __init__(self):
        self.connection = mysql.connector.connect(
            user=environ["DB_LOGIN"],
            password=environ["DB_PASSWD"],
            host=environ["DB_HOST"]
        )
        self.c = self.connection.cursor()
        self.set_db()

    def url_exists(self, url: str) -> Union[int, bool]:
        """
        Returns page/flag ID if its URL exists in the flag_urls or page_urls table.
        Returns False if not.
        """
        if url.endswith("svg"):
            self.c.execute("SELECT id FROM flags WHERE url=%s", (url,))
        else:
            self.c.execute("SELECT id FROM pages WHERE url=%s", (url,))
        resp = self.c.fetchone()
        return resp[0] if resp else False

    def encounter_exists(self, flag: Union[int, str], page: Union[int, str]) -> Union[int, bool]:
        """
        Returns key of encounter if it already exists in the encounters table.

        Page and flag may be specified using an ID or URL.
        """
        if not type(page) == int:
            page = self.url_exists(page)
        if not type(flag) == int:
            flag = self.url_exists(flag)
        self.c.execute("SELECT id FROM encounters WHERE flag=%s AND page=%s", (flag, page))
        resp = self.c.fetchone()
        return resp[0] if resp else False

    def flag_url(self, flag_pk):
        """Returns URL of flag with given ID.""" 
        self.c.execute("SELECT url FROM flags WHERE id=%s", (flag_pk,))
        return self.c.fetchone()[0]

    def page_url(self, page_pk):
        """Returns URL of page with given ID.""" 
        self.c.execute("SELECT url FROM pages WHERE id=%s", (page_pk,))
        return self.c.fetchone()[0]

    # Database row insertion methods
    def new_page_url(self, url: str) -> int:
        """
        Create a new row in the page_urls table and return its key.
        """
        self.c.execute("INSERT INTO pages (url) VALUES (%s)", (url,))
        self.db.commit()
        self.log.info(f"{url} | New flag page link recorded.")
        return self.c.lastrowid

    def new_flag_url(self, url: str) -> int:
        """
        Create a new row in the flag_urls table and return its key.
        """
        self.c.execute("INSERT INTO flags (url) VALUES (%s)", (url,))
        self.db.commit()
        self.log.info(f"{url} | New flag link recorded.")
        return self.c.lastrowid

    def new_encounter(self, flag_url: str, page_url: str) -> int:
        """
        Record encounter of flag on new page in the encounters table.
        """
        flag_pk, page_pk = self.url_exists(flag_url), self.url_exists(page_url)
        self.c.execute("INSERT INTO encounters (flag, page) VALUES (%s, %s)",
                       (flag_pk, page_pk))
        self.db.commit()
        self.log.info(f"{flag_url} | New flag link encounter recorded.")
        return self.c.lastrowid

    def new_flag(self, flag_url: str, dl_url: str) -> int:
        """
        Create a new flag entry in the flags table.
        """
        self.c.execute("INSERT INTO flags (flag_url, dl_url) VALUES (%s, %s)",
                       (flag_url, dl_url,))
        self.db.commit()
        self.log.info(f"{flag_url} | New Flag added to database.")
        return self.c.lastrowid
    
  # Flag setter methods
    def mark_as_downloaded(self, url: str) -> int:
        """
        Mark a flag_url or page_url as downloaded.
        """
        if url.endswith("svg"):
            self.c.execute("UPDATE flag_urls SET downloaded=1 WHERE url=%s;", (url,))
        else:
            self.c.execute("UPDATE page_urls SET downloaded=1 WHERE url=%s;", (url,))
        self.db.commit()
        self.log.info(f"{url} | Marked as downloaded.")
        return self.c.lastrowid

    def mark_as_parsed(self, url: str) -> int:
        """
        Mark a page_url as parsed.
        """
        self.c.execute("UPDATE page_urls SET parsed=1 WHERE url=%s;", (url,))
        self.db.commit()
        self.log.info(f"{url} | Page marked as parsed.")
        return self.c.lastrowid

    def get_encounters(self, flag_url):
        """Returns the primary keys of all pages where flag_url has been encountered."""
        self.c.execute("SELECT id FROM flags WHERE flag_url=%s;", (flag_url,))
        flag_pk = self.c.fetchone()[0]
        self.c.execute("SELECT * FROM encounters WHERE flag=%s;", (flag_pk,))
        return [hit[2] for hit in self.c.fetchall()]

    # Methods for rebuilding queues
    def unparsed_pages(self):
        self.c.execute("SELECT url FROM page_urls WHERE parsed=0 AND downloaded=1;")
        return [_i[1] for _i in self.c.fetchall()]

    def unfetched_links(self):
        self.c.execute("SELECT url FROM flags WHERE downloaded=1;")
        links = [_i[1] for _i in self.c.fetchall()]
        self.c.execute("SELECT * FROM page_urls WHERE downloaded=1;")
        links += [_i[1] for _i in self.c.fetchall()]
        return links

    # Reporting methods
    def flag_count(self) -> int:
        self.c.execute("SELECT id FROM flags")
        return len(self.c.fetchall())

    def page_count(self) -> int:
        self.c.execute("SELECT id FROM flags")
        return len(self.c.fetchall())

    


    # Utility methods
    def set_db(self):
        try:
            self.c.execute("USE flags")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db()
            else:
                print(err)
                exit(1)

    def create_db(self):
        self.c.execute("CREATE DATABASE flags DEFAULT CHARACTER SET 'utf8'")
        self.c.execute("USE flags")
        for table in TABLES:
            self.c.execute(TABLES[table])
            self.new_page_url("https://en.wikipedia.org/wiki/Lists_of_flags")
        self.conn.commit()
