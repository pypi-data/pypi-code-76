from . import Base


class animeindo(Base):
    tag = "anime"
    host = "https://animeindo.asia"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        if (eps := soup.findAll(class_="episode_list")):
            d = {}
            for ep in eps:
                d[ep.a.text.split(" -")[0]] = self.getPath(ep.a.attrs["href"])
            key = self.choice(d.keys())
            return self.extract(d[key])

        formats = self.re.findall(r"(Format .+?):", str(soup))
        result = {fm: {} for fm in formats}
        for p in soup.findAll("p", class_="has-text-align-center"):
            if (aa := p.findAll("a")):
                info = [self.re.split(r"\s*:", i)[0] for i in
                        self.re.findall(r">\s*(\d+p(?:\s+.+?)?)\s*:", str(p))]
                if len(info) == 1:
                    d = {info[0]: {
                        a.text: a.attrs["href"] for a in aa
                    }}
                else:
                    formats.pop(0)
                    d = {}
                    for sub, dom in self.re.findall(r"(\d+p.+?):.+?((?:<a.+?>.+?</a>(?:\s*\|\s*)?)+)", str(p)):
                        aa = self.soup(dom).findAll("a")
                        d[sub] = {
                            a.text: a.attrs["href"] for a in aa
                        }
                result[formats[0]] = d
        return result

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        for animposx in soup.findAll(class_="animposx"):
            a = animposx.find("a")
            yield {
                "title": a.attrs["title"],
                "id": self.getPath(a.attrs["href"])
            }
            break
