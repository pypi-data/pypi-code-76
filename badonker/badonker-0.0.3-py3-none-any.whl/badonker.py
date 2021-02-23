import urllib

from . import http, dict, errors

noresponse = "eyy sorry im just a dog.."

def honker():
    try:
        return http.get("/honker.php?tags=big_breasts")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)


def badonkers():
    try:
        return http.get("/honker.php?tags=large_breasts")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)


def hhonker():
    try:
        return http.get("/r.php?tags?=big_breasts")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def ass():
    try:
        return http.get("/r.php?tags?=ass")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def hass():
    try:
        return http.get("/honker.php?tags?=ass")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def thicc():
    try:
        return http.get("/r.php?tags?=thighhighs")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def hthicc():
    try:
        return http.get("/honker.php?tags=thighhighs")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def milf():
    try:
        return http.get("/honker.php?tags=milf")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def hmilf():
    try:
        return http.get("/r.php?tags?=milf")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def milk():
    try:
        return http.get("/honker.php?tags=huge_breasts")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def hmilk():
    try:
        return http.get("/r.php?tags?=huge_breasts")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def booty():
    try:
        return http.get("/honker.php?tags=huge_ass")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def hbooty():
    try:
        return http.get("/r.php?tags=huge_ass")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def belly():
    try:
        return http.get("/honker.php?tags=big_belly")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def hbelly():
    try:
        return http.get("/r.php?tags=big_belly")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def gifTits():
    try:
        return http.get("/g.php?tags=tits")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def gifPussy():
    try:
        return http.get("/g.php?tags=pussy")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def gifAss():
    try:
        return http.get("/g.php?tags=ass")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def gifMissionary():
    try:
        return http.get("/g.php?tags=missionary")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def gifCowgirl():
    try:
        return http.get("/g.php?tags=cowgirl")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def gifBj():
    try:
        return http.get("/g.php?tags=blowjob")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def gifCumshots():
    try:
        return http.get("/g.php?tags=cumshots")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def random():
    try:
        return http.get("/g.php")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def ahegao():
    try:
        return http.get("/ahe.php")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)
