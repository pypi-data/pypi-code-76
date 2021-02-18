import requests
from bs4 import BeautifulSoup as bs

class SMFscraper():
    """Scraping SMF and getting values"""
    def __init__(self, mainURL):
        self.mainURL = mainURL
        self.mainScrap = bs(requests.get(mainURL).text, 'html.parser')
        self.boardsList = self.getBoards()
    
    def getBoards(self):
        """
        Returns a list of boards with their boardids.
        """
        TDtags = self.mainScrap.findAll('td', {'class': 'info'})
        boardsList = []
        for TDtag in TDtags:
            aTag = TDtag.find('a')
            link = aTag['href']
            boardID = link.split('board=')[1].split('.')[0]
            title = aTag.text
            boardsList.append((boardID, title, link))
        return boardsList
    
    def getAllPosts(self, boardID, page = 1):
        """
        Returns all posts within the board.
        """
        for board in self.boardsList:
            if boardID == int(board[0]):
                if page == 1 or page == 0:
                    boardScrap = bs(requests.get(board[2]).text, 'html.parser')
                else:
                    newBoardID = f'{boardID}.' + str((page-1)*2) + '0'
                    url = self.mainURL + '?board=' + newBoardID
                    boardScrap = bs(requests.get(url).text, 'html.parser')
                spanTags = boardScrap.findAll('span', {'class': 'subject_title'})
                postsList = []
                for spanTag in spanTags:
                    aTag = spanTag.find('a')
                    link = aTag['href']
                    title = aTag.text
                    postsList.append((title, link))
                return postsList
        else:
            print('Board not found')

    def getStickyPosts(self, boardID):
        """
        Returns posts that are sticky.
        """
        for board in self.boardsList:
            if boardID == int(board[0]):
                boardScrap = bs(requests.get(board[2]).text, 'html.parser')
                spanTags = boardScrap.findAll('span', {'class': 'subject_title'})
                postsList = []
                for spanTag in spanTags:
                    TD_tag = spanTag.parent
                    while TD_tag.name != 'td':
                        TD_tag = TD_tag.parent
                    if 'stickybg' in TD_tag['class']:
                        aTag = spanTag.find('a')
                        link = aTag['href']
                        title = aTag.text
                        postsList.append((title, link))
                if len(postsList) == 0:
                    print('There are no sticky posts.')
                    return None
                else: 
                    return postsList
    
    def getLockedPosts(self, boardID):
        """
        Returns posts that are locked.
        """
        for board in self.boardsList:
            if boardID == int(board[0]):
                boardScrap = bs(requests.get(board[2]).text, 'html.parser')
                spanTags = boardScrap.findAll('span', {'class': 'subject_title'})
                postsList = []
                for spanTag in spanTags:
                    TD_tag = spanTag.parent
                    while TD_tag.name != 'td':
                        TD_tag = TD_tag.parent
                    if 'lockedbg2' in TD_tag['class'] or 'locked_sticky2' in TD_tag['class']:
                        aTag = spanTag.find('a')
                        link = aTag['href']
                        title = aTag.text
                        postsList.append((title, link))
                if len(postsList) == 0:
                    print('There are no locked posts.')
                    return None
                else: 
                    return postsList
    
    def getNormalPosts(self, boardID):
        """
        Returns posts that are neither locked nor sticky.
        """
        for board in self.boardsList:
            if boardID == int(board[0]):
                boardScrap = bs(requests.get(board[2]).text, 'html.parser')
                spanTags = boardScrap.findAll('span', {'class': 'subject_title'})
                postsList = []
                for spanTag in spanTags:
                    TD_tag = spanTag.parent
                    while TD_tag.name != 'td':
                        TD_tag = TD_tag.parent
                    if 'lockedbg2' not in TD_tag['class'] and 'locked_sticky2' not in TD_tag['class']:
                        aTag = spanTag.find('a')
                        link = aTag['href']
                        title = aTag.text
                        postsList.append((title, link))
                if len(postsList) == 0:
                    print('There are no locked posts.')
                    return None
                else: 
                    return postsList
    
    def getLatestPost(self, boardID):
        """
        Returns the latests non-sticky/unlocked post.
        """
        posts = self.getNormalPosts(boardID)
        return posts[0]