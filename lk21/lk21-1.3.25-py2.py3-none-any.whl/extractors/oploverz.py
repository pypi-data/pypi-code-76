from . import Base


class oploverz(Base):
    host = "https://www.oploverz.in"
    tag = "anime"

    def extract(self, id, rextract=False):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        self._write(str(soup))
        if (ep_list := soup.find(class_="episodelist")):
            d = {}
            for li in ep_list.findAll("li"):
                a = li.find("a")
                d[a.text.strip()] = a.attrs["href"]
            key = self.choice(d.keys())
            return self.extract(d[key], rextract=True)

        elif not rextract and (all_eps := soup.find(class_="btn-full-eps")):
            ch = self.choice(["Lanjut", all_eps.text])
            if ch != "Lanjut":
                return self.extract(self.getPath(all_eps.attrs["href"]))

        title = [
            a for a in self.re.findall(r"(?s)strong>([^>]+?)</strong", str(soup))
            if self.re.search(r"\([^)]+", a)
        ]

        result = {}
        for ttl, ddl in zip(title, soup.findAll(class_="soraddl")):
            d = {}
            for p in ddl.findAll("p"):
                if (t1 := p.find(class_="sorattl")):
                    d1 = {}
                    for a in p.findAll("a"):
                        d1[a.text] = a.attrs["href"]
                    d[t1.text] = d1
            result[ttl] = d
        return result

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}/",
                               params={"s": query, "post_type": "post"})
        soup = self.soup(raw)

        for dtl in soup.findAll("div", class_="dtl"):
            a = dtl.find("a")
            yield {
                "title": a.text,
                "id": self.getPath(a.attrs["href"]),
                "release": dtl.findAll("span")[1].text
            }
