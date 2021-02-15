from . import Base


class lk21(Base):
    desc = "Film, Movie (default)"
    host = "http://149.56.24.226/"

    def extract(self, id: str):
        raw = self.session.post("http://dl.sharemydrive.xyz/verifying.php",
                                headers={
                                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                    "Accept": "*/*",
                                    "X-Requested-With": "XMLHttpRequest"
                                },
                                params={"slug": id},
                                data={"slug": id}
                                )
        soup = self.soup(raw)
        tb = soup.find("tbody")

        result = {}
        for tr in tb.findAll("tr"):
            title = tr.find("strong").text
            result[title] = {}
            for td in tr.findAll("td")[1:]:
                if (a := td.a):
                    result[title][a.attrs["class"]
                                  [-1].split("-")[-1]] = a.attrs["href"]
        return result

    def search(self, title: str, page=1):
        if page > 1:
            return
        raw = self.session.get(self.host,
                               params={"s": title})

        soup = self.soup(raw)
        for item in soup.findAll(class_="search-item"):
            a = item.a
            extra = {"genre": [], "star": [], "country": [],
                     "size": [""], "quality": [""], "year": [""]}
            for tag in item.find(class_="cat-links").findAll("a"):
                name, it = self.re.findall(r"/([^/]+)/([^/]+)", str(tag))[0]
                extra[name].insert(0, it)

            for p in filter(lambda x: x.strong is not None, item.findAll("p")):
                np, vl = self.re.findall(
                    r"^([^:]+):\s+(.+)", p.text.strip())[0]
                np = "star" if np == "Bintang" else "director" if np == "Sutradara" else np
                extra[np] = self.re.split(r"\s*,\s*", vl) if "," in vl else vl

            extra["id"] = self.re.search(
                r"\w/([^/]+)", a.attrs["href"]).group(1)
            result = {
                "title": (item.find("h2").text or a.img.attrs["alt"]).strip(),
            }
            result.update(extra)
            yield result
