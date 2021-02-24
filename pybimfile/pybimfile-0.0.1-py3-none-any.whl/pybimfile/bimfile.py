import os


def to_bytes(buf, blen=1):
    # return buf.to_bytes(blen, byteorder=Node.BYTEORD)
    rc = []
    for i in range(0, blen):
        b = buf & 0xFF
        rc.append(b)
        buf >>= 8
    return bytes(reversed(rc))


def from_bytes(buf):
    # return int.from_bytes(buf, byteorder=Node.BYTEORD)
    rc = 0
    for i in range(0, len(buf)):
        rc <<= 8
        rc |= buf[i]
    return rc


def _split(buf, blen):
    return buf[:blen], buf[blen:]


LINK_SIZE = 8
SEG_MAGIC = 0xDEADBEEF
SEG_MAGIC_SIZE = 4


class BeforeImageFile:
    def __init__(
        self,
        fnam,
        mode="r",
        bimfile=None,
        blksize=512,
        keep_bim=False,
        link_size=LINK_SIZE,
        **kwargs,
    ):
        self.link_size = link_size
        self.seg_size = SEG_MAGIC_SIZE + self.link_size * 2
        self.fnam = fnam
        self.fd = None
        self.flen = None
        self.mode = mode
        self.kwargs = kwargs
        self.bimfd = None
        self.bimfile = bimfile
        self.keep_bim = keep_bim
        self.blksize = blksize

        self.already_exist = False
        self.binary = self.mode.find("b") >= 0
        if self.binary == False:
            raise Exception("only binary mode supported")

    def close(self):

        if self.fd:
            self.fd.close()
            self.fd = None
        self._close()

    def _close(self):
        if self.bimfd:
            if not self.keep_bim:
                self.bimfd.truncate()
            self.bimfd.close()
            self.bimfd = None
            if not self.keep_bim:
                os.remove(self.bimfile)

    def open(self):
        if self.fd:
            raise Exception("file already open")

        mode = self.mode
        if not self.binary:
            mode += "b"

        self.flen = os.path.getsize(self.fnam)
        self.fd = open(self.fnam, mode)

        if self.bimfile == None:
            self.bimfile = self.fnam + ".bim"

        try:
            fs = os.stat(self.bimfile)
            self.already_exist = True
            self.bimfd = open(self.bimfile, "+rb")
            # append to end
            self.bimfd.seek(0, os.SEEK_END)
        except:
            # file dont exist
            self.bimfd = open(self.bimfile, "+wb")
            # init file structure
            buf = self._pack(self.flen, SEG_MAGIC)
            self._writebim(buf)

        return self

    def seek(self, offset, whence=0):
        return self.fd.seek(offset, whence)

    def tell(self):
        return self.fd.tell()

    def flush(self):
        self.fd.flush()
        os.fsync(self.fd.fileno())

    def read(self, size=None):
        return self.fd.read(size)

    def write(self, buf):
        fpos = self.tell()

        if fpos < self.flen:  # changing, not appending
            # preserve the content
            l = len(buf)
            while l > 0:
                toread = min(l, self.blksize)
                bb = self.read(toread)
                self._writebim(bb)
                l -= len(bb)

            blen = len(buf)

            bb = self._pack(fpos, blen)
            self._writebim(bb)

            cpos = self.seek(fpos)
            if cpos != fpos:
                raise Exception(f"seek failed cpos={cpos}, expected={fpos}")

        if not isinstance(buf, bytes):
            buf = buf.encode()
        self.fd.write(buf)

    def comit(self):
        self.flush()
        self.close()
        self.open()

    def rollback(self):

        if self.fd and self.bimfd:
            blen = self.bimfd.seek(0, os.SEEK_END)
            bpos = blen - self.seg_size

            while bpos > self.seg_size:
                fpos, blen, bpos = self._searchsegment(bpos)

                self.fd.seek(fpos)
                self.bimfd.seek(bpos - blen)

                l = blen
                while l > 0:
                    toread = min(l, self.blksize)
                    buf = self.bimfd.read(toread)
                    self.fd.write(buf)
                    l -= len(buf)

                bpos -= blen

            flen, dead1, dead2 = self._searchsegment(0)
            if dead1 != SEG_MAGIC:
                raise Exception("invalid bim file format")

            # preserve old file size
            self.fd.truncate(flen)
            # close bim file
            self._close()

    def _searchsegment(self, bpos):
        """search a segment"""
        while True:
            if bpos < 0:
                raise Exception("invalid bim file format")
            self.bimfd.seek(bpos)
            buf = self.bimfd.read(self.seg_size)

            fpos, blen, deadbeef = self._unpack(buf)

            if deadbeef == SEG_MAGIC:
                break
            # continue searching one below
            bpos -= 1
        return fpos, blen, bpos

    def _pack(self, fpos, blen):
        buf = []
        buf.extend(to_bytes(fpos, self.link_size))
        buf.extend(to_bytes(blen, self.link_size))
        buf.extend(to_bytes(SEG_MAGIC, SEG_MAGIC_SIZE))
        return bytes(buf)

    def _unpack(self, buf):
        b, buf = _split(buf, self.link_size)
        fpos = from_bytes(b)
        b, buf = _split(buf, self.link_size)
        blen = from_bytes(b)
        b, buf = _split(buf, SEG_MAGIC_SIZE)
        deadbeef = from_bytes(b)
        if len(buf) > 0:
            raise Exception("invalid segment")
        return fpos, blen, deadbeef

    def _writebim(self, buf):
        self.bimfd.write(buf)
        self.bimfd.flush()
