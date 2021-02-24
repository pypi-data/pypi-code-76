#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from bapy import IPBase
from bapy import IPLoc
from bapy import IPv4Address
from bapy import localhost
from bapy import Obj

from bapy.data.nmap import samples


google_addr = '8.8.8.8'
google_country_name = 'United States'
google_name = 'dns.google'
password_addr = '54.39.133.43'

local = IPBase(localhost)
password = IPBase(password_addr)
name = IPBase(google_name, name=True)

addr = IPBase(IPBase.addr(google_addr))
addr_loc = IPBase(IPBase.addr(google_addr), loc=True)
addr_name = IPBase(IPBase.addr(google_addr), name=True)
addr_loc_name = IPBase(IPBase.addr(google_addr), loc=True, name=True)

nmap_dict = samples[google_addr]
nmap_addr = nmap_dict['host']['address']['addr']
nmap = IPBase(nmap_dict)

dict_ip = IPBase(nmap, loc=True, name=True)
dict_info1 = IPBase(addr.asdict['info'])
dict_info2 = IPBase(info=addr.asdict['info'])
dict_loc1 = IPBase(addr_loc.asdict['loc'], name=True)
dict_loc2 = IPBase(loc=addr_loc.asdict['loc'], name=True)
dict_dict = IPBase(**addr_loc_name.kwargs)

mine = IPBase()
mine_loc = IPBase(loc=True)
mine_name = IPBase(name=True)
mine_loc_name = IPBase(loc=True, name=True)

base = IPBase(mine)
base_loc = IPBase(mine_loc)
base_name = IPBase(mine_name)
base_loc_name = IPBase(mine_loc_name)

text = IPBase(google_addr)
text_loc = IPBase(google_addr, loc=True)
text_name = IPBase(google_addr, name=True)
text_loc_name = IPBase(google_addr, loc=True, name=True)


# noinspection DuplicatedCode
def test_init_addr():
    assert Obj(addr.ip).str
    assert Obj(addr.info).instance(IPv4Address)
    assert Obj(addr.loc).instance(IPLoc)
    assert addr.ip == google_addr
    assert addr.ip == addr.info.exploded
    assert str(addr) == addr.info.exploded
    assert addr.ip != addr.loc.IPv4
    assert addr.loc.IPv4 is None
    assert addr.name is None

    assert addr_loc.ip == addr_loc.loc.IPv4
    assert addr_loc.loc.country_name == google_country_name
    assert any([addr_loc.loc.values])

    assert addr_name.name
    assert addr_name.name == google_name

    assert addr_loc_name.ip == addr_loc_name.loc.IPv4
    assert addr_loc_name.loc.country_name == google_country_name
    assert any([addr_loc_name.loc.values])
    assert addr_loc_name.name == google_name


def test_init_base():
    assert base == base
    assert base_loc == mine_loc
    assert base_name == mine_name
    assert base_loc_name == mine_loc_name


def test_init_dict_ip():
    assert dict_ip.ip == nmap_addr


def test_init_dict_info():
    assert dict_info1.ip == google_addr
    assert dict_info1.info == addr.info
    assert dict_info2.ip == google_addr
    assert dict_info2.info == addr.info


def test_init_dict_loc():
    assert dict_loc1.ip == google_addr
    assert dict_loc1.info.exploded == google_addr
    assert dict_loc1.loc.country_name == google_country_name
    assert dict_loc1.name == google_name

    assert dict_loc2.ip == google_addr
    assert dict_loc2.info.exploded == google_addr
    assert dict_loc2.loc.country_name == google_country_name
    assert dict_loc2.name == google_name


def test_init_dict_dict():
    assert dict_dict.ip == google_addr
    assert dict_dict.info.exploded == google_addr
    assert dict_dict.loc.country_name == google_country_name
    assert dict_dict.name == google_name


# noinspection DuplicatedCode
def test_init_mine():
    assert Obj(mine.ip).str
    assert Obj(mine.info).instance(IPv4Address)
    assert Obj(mine.loc).instance(IPLoc)
    assert mine.ip == mine.info.exploded
    assert str(mine) == mine.info.exploded
    assert mine.ip != mine.loc.IPv4
    assert mine.loc.IPv4 is None
    assert mine.name is None

    assert mine_loc.ip == mine_loc.loc.IPv4
    assert any([mine_loc.loc.values])

    assert mine_name.name
    assert mine_name.name[0:1] == mine_name.info.reverse_pointer[0:1]

    assert mine_loc_name.ip == mine_loc_name.loc.IPv4
    assert any([mine_loc_name.loc.values])
    assert mine_loc_name.name


def test_init_name():
    assert name.name == addr_name.name


def test_init_nmap():
    assert nmap.ip == nmap_addr


# noinspection DuplicatedCode
def test_init_text():
    assert Obj(text.ip).str
    assert Obj(text.info).instance(IPv4Address)
    assert Obj(text.loc).instance(IPLoc)
    assert text.ip == google_addr
    assert text.ip == text.info.exploded
    assert str(text) == text.info.exploded
    assert text.ip != text.loc.IPv4
    assert text.loc.IPv4 is None
    assert text.name is None

    assert text_loc.ip == text_loc.loc.IPv4
    assert text_loc.loc.country_name == google_country_name
    assert any([text_loc.loc.values])

    assert text_name.name
    assert text_name.name == google_name

    assert text_loc_name.ip == text_loc_name.loc.IPv4
    assert text_loc_name.loc.country_name == google_country_name
    assert any([text_loc_name.loc.values])
    assert text_loc_name.name == google_name


def test_password():
    assert not addr.password()
    assert not asyncio.run(addr.password_aio())
    assert password.password()
    assert asyncio.run(password.password_aio())


def test_ping():
    assert addr.ping()
    assert asyncio.run(addr.ping_aio())
    assert IPBase('24.24.23.2').ping() is False


def test_sort():
    sort = sorted([mine, password, addr, local])
    assert sort[0].ip == google_addr
    assert sort[1].ip == password_addr
    assert sort[2].ip == mine.ip
    assert sort[3].ip == localhost
