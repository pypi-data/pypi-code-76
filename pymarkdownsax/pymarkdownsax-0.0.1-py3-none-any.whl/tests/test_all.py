#!/usr/bin/python
# -*- coding: <encoding name> -*-

import unittest
import logging

import pymarkdownsax


class TestPandoc(pymarkdownsax.PyMarkDownSax2Html):

    def __init__(self):
        super().__init__()

        self.tagstack = []

    def startElement(self, tag, attributes):
        #print(tag)
        #print(attributes)
        self.tagstack.append([tag, attributes])

    def endElement(self, tag):
        #print("Stopping element: "+tag)
        pass

    def characters(self, token):
        #print("characters")
        attributes = {"text" : token.group(0)}
        self.tagstack.append([pymarkdownsax.PyMarkDownSax2Html.CHARACTERS, attributes])


class TestPyMarkDownSax(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_title(self):

        data = '''---
title: mytitle
---

Test
'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag0 = pan.tagstack[0]
        self.assertTrue( tag0[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag0[1]
        self.assertTrue( tag0[1]['title'] == "mytitle")

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n')

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'Test')

    def test_title_space(self):

        data = '''---
title : mytitle
---

Test
'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag0 = pan.tagstack[0]
        self.assertTrue( tag0[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag0[1]
        self.assertTrue( tag0[1]['title'] == "mytitle")

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'Test')

    def test_title_quotes(self):

        data = '''---
title : "mytitle"
---

Test
'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag0 = pan.tagstack[0]
        self.assertTrue( tag0[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        self.assertTrue( tag0[1]['title'] == "mytitle")

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'Test')

    def test_header_advanced(self):

        data = '''---
title: "My Test Title"
date: 2020-08-11 21:21
draft: false
tags : [
    "Sociology",
]
categories : [
    "Sociology",
]
---

Test
'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        self.assertTrue( tag[1]['title'] == 'My Test Title')
        self.assertTrue( tag[1]['draft'] == 'false')
        self.assertTrue( tag[1]['date'] == '2020-08-11 21:21')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'Test')

    def test_heading(self):

        data = '''---
title: mytitle
---

# myheading
'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.H1 )
        self.assertTrue( tag[1]['text'] == 'myheading' )

    def test_subheading(self):

        data = '''---
title: mytitle
---

# myheading

## subheading
'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.H1 )
        self.assertTrue( tag[1]['text'] == 'myheading' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.H2 )
        self.assertTrue( tag[1]['text'] == 'subheading' )

    def test_heading_text(self):

        data = '''---
title: mytitle
---

# myheading

Text

More


'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.H1 )
        self.assertTrue( tag[1]['text'] == 'myheading' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'Text' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[6]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'More' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

    def test_text_sections(self):

        data = '''---
title: mytitle
---

text_1.

text_2.
'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'text_1.' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'text_2.' )

    def test_list(self):

        data = '''---
title: mytitle
---

 - list1
 - list2

'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n ' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LIST )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'list1' )

        tag = pan.tagstack[5]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n ' )

        tag = pan.tagstack[6]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LIST )

        tag = pan.tagstack[7]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[8]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'list2' )

    def test_list_mul(self):

        data = '''---
title: mytitle
---

 * list1
 * list2

'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n ' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LIST )
        self.assertTrue( tag[1]['list_type'] == '*' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'list1' )

        tag = pan.tagstack[5]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n ' )

        tag = pan.tagstack[6]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LIST )
        self.assertTrue( tag[1]['list_type'] == '*' )

        tag = pan.tagstack[7]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[8]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'list2' )

    def test_list_plus(self):

        data = '''---
title: mytitle
---

 + list1
 + list2

'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n ' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LIST )
        self.assertTrue( tag[1]['list_type'] == '+' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'list1' )

        tag = pan.tagstack[5]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n ' )

        tag = pan.tagstack[6]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LIST )
        self.assertTrue( tag[1]['list_type'] == '+' )

        tag = pan.tagstack[7]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[8]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'list2' )

    def test_link(self):

        data = '''---
title: mytitle
---

[MyLink](./indekx.html)
[Main Page](./index.html)


'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LINK )
        self.assertTrue( tag[1]['name'] == 'MyLink' )
        self.assertTrue( tag[1]['link'] == './indekx.html' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LINK )
        self.assertTrue( tag[1]['name'] == 'Main Page' )
        self.assertTrue( tag[1]['link'] == './index.html' )

        tag = pan.tagstack[5]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n\n' )

    def test_nolink(self):

        data = '''---
title: mytitle
---

[MyLink] info

'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '[MyLink]' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'info' )

    def test_image(self):

        data = '''---
title: mytitle
---

![MyLink](./indekx.html)


'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.IMAGE )
        self.assertTrue( tag[1]['name'] == 'MyLink' )
        self.assertTrue( tag[1]['link'] == './indekx.html' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n\n' )

    def test_image_dot(self):

        data = '''---
title: mytitle
---

![MyLink](./indekx.html).


'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.IMAGE )
        self.assertTrue( tag[1]['name'] == 'MyLink' )
        self.assertTrue( tag[1]['link'] == './indekx.html' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '.' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n\n' )

    def test_link_image(self):

        data = '''---
title: mytitle
---

[MyLink](./indekx.html)

![MyImage](./img.jpg)

'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LINK )
        self.assertTrue( tag[1]['name'] == 'MyLink' )
        self.assertTrue( tag[1]['link'] == './indekx.html' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.IMAGE )
        self.assertTrue( tag[1]['name'] == 'MyImage' )
        self.assertTrue( tag[1]['link'] == './img.jpg' )

        tag = pan.tagstack[5]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

    def test_image_in_link(self):

        data = '''---
title: mytitle
---

[![MyImage](./img.jpg)](./indekx.html)

'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.LINK )
        self.assertTrue( tag[1]['name'] == '![MyImage](./img.jpg)' )
        self.assertTrue( tag[1]['link'] == './indekx.html' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.IMAGE )
        self.assertTrue( tag[1]['name'] == 'MyImage' )
        self.assertTrue( tag[1]['link'] == './img.jpg' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

    def test_text_sections_advanced(self):

        data = '''---
title: mytitle
---

test one

text three

whatever

'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'test' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'one' )

        tag = pan.tagstack[5]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[6]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'text' )

        tag = pan.tagstack[7]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[8]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'three' )

        tag = pan.tagstack[9]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[10]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'whatever' )

    def test_bold_italic(self):

        data = '''---
title: mytitle
---

test **one** *two* ***three***

four

'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'test' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.BOLD )
        self.assertTrue( tag[1]['text'] == 'one' )

        tag = pan.tagstack[5]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[6]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.ITALIC )
        self.assertTrue( tag[1]['text'] == 'two' )

        tag = pan.tagstack[7]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[8]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.BOLD_ITALIC )
        self.assertTrue( tag[1]['text'] == 'three' )

        tag = pan.tagstack[9]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[10]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'four' )

    def test_text_sections_minus(self):

        data = '''---
title: mytitle
---

test - one

text three

'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'test' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[4]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '-' )

        tag = pan.tagstack[5]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[6]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'one' )

        tag = pan.tagstack[7]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[8]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'text' )

        tag = pan.tagstack[9]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == ' ' )

        tag = pan.tagstack[10]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == 'three' )

        tag = pan.tagstack[11]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

    def test_embed(self):

        data = '''---
title: mytitle
---

$[MyLink](./indekx.html)


'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.EMBED )
        self.assertTrue( tag[1]['name'] == 'MyLink' )
        self.assertTrue( tag[1]['link'] == './indekx.html' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n\n' )

    def test_embed_yt(self):

        data = '''---
title: mytitle
---

$YT[MyLink](./indekx.html)


'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.EMBED_YT )
        self.assertTrue( tag[1]['name'] == 'MyLink' )
        self.assertTrue( tag[1]['link'] == './indekx.html' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n\n' )

    def test_hr(self):

        data = '''---
title: mytitle
---

----
'''

        pan = TestPandoc()
        pan.parse_data(data)

        self.assertTrue( len(pan.tagstack) > 0)

        tag = pan.tagstack[0]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HEADER )
        attr = tag[1]

        self.assertTrue( attr['title'] == 'mytitle')

        tag = pan.tagstack[1]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n\n' )

        tag = pan.tagstack[2]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.HR )
        self.assertTrue( tag[1]['text'] == '----' )

        tag = pan.tagstack[3]
        self.assertTrue( tag[0] == pymarkdownsax.PyMarkDownSax2Html.CHARACTERS )
        self.assertTrue( tag[1]['text'] == '\n' )


if __name__ == '__main__':
    unittest.main()
