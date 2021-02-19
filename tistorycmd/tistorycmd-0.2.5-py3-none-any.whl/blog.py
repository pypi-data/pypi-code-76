from . import config
import requests, json, os, re


class Blog:
    def __init__(self):
        self.output_type = 'json'

    # 블로그 정보 출력
    def info(self):
        """
            GET https://www.tistory.com/apis/blog/info?
            access_token={access-token}
            &output={output-type}

            응답
            id: 사용자 로그인 아이디
            userId: 사용자 id
            blogs
                url: 티스토리 기본 url
                secondaryUrl: 독립도메인 url
                title: 블로그 타이틀
                description: 블로그 설명
                default: 대표블로그 여부 (Y/N)
                blogIconUrl: 블로그 아이콘 URL
                faviconUrl: 파비콘 URL
                profileThumbnailImageUrl: 대표이미지 썸네일 URL
                profileImageUrl: 대표이미지 URL
                blogId: 블로그 아이디
                nickname: 블로그에서의 닉네임
                role: 블로그 권한
                statistics: 블로그 컨텐츠 개수
                post: 글 수
                comment: 댓글 수
                trackback: 트랙백 수
                guestbook: 방명록 수
                invitation: 초대장 수
        """
        url = 'https://www.tistory.com/apis/blog/info'
        data = {'access_token': config.config['access_token'], 'output': self.output_type}
        res = requests.get(url, params=data)
        if res.status_code == 200:
            print(json.dumps(res.json(), indent=4, ensure_ascii=False))

        else:
            print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    # 블로그의 카테고리 리스트 얻기
    def category_list(self):
        """
        GET https://www.tistory.com/apis/category/list?
        access_token={access-token}
        &output={output-type}
        &blogName={blog-name}

        blogName: Blog 이름
        """
        url = 'https://www.tistory.com/apis/category/list'
        data = {'access_token': config.config['access_token'], 'output': self.output_type, 'blogName': config.config['blog_name']}
        res = requests.get(url, params=data)

        if res.status_code == 200:
            print('==================category list==================')
            print('[ID] = [카테고리명]')
            print('-------------------------------------------------')
            categories = res.json()["tistory"]["item"]["categories"]
            for category in categories:
                print(category["id"] + " = " + category["label"])
        else:
            print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    # 블로그에 글쓰기
    def post_write(self, history_file, title, content, category_id, tag):
        url = 'https://www.tistory.com/apis/post/write'
        visibility = 3
        published = ''
        slogan = ''
        acceptComment = 1
        password = ''
        '''
        blogName: Blog Name (필수)
        title: 글 제목 (필수)
        content: 글 내용
        visibility: 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
        category: 카테고리 아이디 (기본값: 0)
        published: 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)
        slogan: 문자 주소
        tag: 태그 (',' 로 구분)
        acceptComment: 댓글 허용 (0, 1 - 기본값)
        password: 보호글 비밀번호
        '''
        data = {'access_token': config.config['access_token'], 'output': self.output_type, 'blogName': config.config['blog_name'], 'title': title,
                'content': content, 'visibility': visibility, 'category': category_id, 'published': published,
                'slogan': slogan, 'tag': tag, 'acceptComment': acceptComment, 'password': password}
        res = requests.post(url, data=data)
        if res.status_code == 200:
            history_json = dict()
            history_json['postId'] = res.json()["tistory"]["postId"]
            history_json['url'] = res.json()["tistory"]["url"]
            history_json['title'] = title
            history_json['category'] = category_id

            if not os.path.exists(history_file):
                with open(history_file, 'w', encoding='utf-8') as make_file:
                    json.dump(history_json, make_file, indent="\t")

            print('Post Registration Successful')
            print(res.json()["tistory"]["url"])
        else:
            print('Post Registration Fail')
            print(res.json())

    # 블로그에 글수정 (모든내용 수정)
    def post_edit(self, history_file, title, content, category_id, tag):
        url = 'https://www.tistory.com/apis/post/modify'
        visibility = 3
        published = ''
        slogan = ''
        acceptComment = 1
        password = ''
        with open(history_file, 'r') as f:
            history = json.load(f)
            postId = history['postId']
        '''
        blogName: Blog Name (필수)
        title: 글 제목 (필수)
        content: 글 내용
        visibility: 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
        category: 카테고리 아이디 (기본값: 0)
        published: 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)
        slogan: 문자 주소
        tag: 태그 (',' 로 구분)
        acceptComment: 댓글 허용 (0, 1 - 기본값)
        password: 보호글 비밀번호
        '''
        data = {'access_token': config.config['access_token'], 'output': self.output_type,
                'postId': postId,
                'blogName': config.config['blog_name'], 'title': title,
                'content': content, 'visibility': visibility, 'category': category_id, 'published': published,
                'slogan': slogan, 'tag': tag, 'acceptComment': acceptComment, 'password': password}
        res = requests.post(url, data=data)
        if res.status_code == 200:
            print('Post Modification Successful')
            print(res.json()["tistory"]["url"])
        else:
            print('Post Modification Fail')
            print(res.json())
            print('.tistory 파일 삭제후 다시 시도해주세요')

    # 파일 업로드
    def file_upload(self, line, dir_path):
        """
            POST https://www.tistory.com/apis/post/attach?
            access_token={access-token}
            &blogName={blog-name}
            [uploadedfile]
            blogName: Blog Name 입니다.
            uploadedfile: 업로드할 파일 (multipart/form-data)
        """
        # 파일명
        name_grp = re.search('(\!\[\s*)(\w+)(\s*\])(\(\s*)([^http:\/\/].*)(\s*\))', line)
        if(name_grp):
            file_name = name_grp.group(5)

            # 업로드
            files = {"uploadedfile": open(os.path.abspath(dir_path + file_name), 'rb')}
            url = 'https://www.tistory.com/apis/post/attach'
            data = {'access_token': config.config['access_token'], 'blogName': config.config['blog_name'], 'output': self.output_type}
            res = requests.post(url, params=data, files=files)

            # 업로드된 url로 변경
            line = re.sub('(\!\[\s*)(\w+)(\s*\])(\(\s*)([^http:\/\/].*)(\s*\))', '\\1\\2\\3(' + res.json()["tistory"]["url"] + ')',line)

        return line

    def post_read(self, post_id):
        '''
        postId: 글 ID - 리스트 얻기로 알 수 있음
        '''
        url = 'https://www.tistory.com/apis/post/read'
        data = {'access_token': config.config['access_token'], 'output': self.output_type, 'blogName': config.config['blog_name'],
                'postId': post_id}
        res = requests.get(url, params=data)
        if res.status_code == 200:
            return res.json()["tistory"]["item"]
        else:
            print(res.json())
            return res.json()["tistory"]["item"]

    # 블로그 내용수정
    def contents_update(self, postId, title, content, category_id):
        url = 'https://www.tistory.com/apis/post/modify'
        visibility = 3
        published = ''
        slogan = ''
        acceptComment = 1
        password = ''
        '''
        blogName: Blog Name (필수)
        title: 글 제목 (필수)
        content: 글 내용
        visibility: 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
        category: 카테고리 아이디 (기본값: 0)
        published: 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)
        slogan: 문자 주소
        tag: 태그 (',' 로 구분)
        acceptComment: 댓글 허용 (0, 1 - 기본값)
        password: 보호글 비밀번호
        '''
        data = {'access_token': config.config['access_token'], 'output': self.output_type,
                'postId': postId,
                'blogName': config.config['blog_name'], 'title': title,
                'content': content, 'visibility': visibility, 'category': category_id, 'published': published,
                'slogan': slogan, 'acceptComment': acceptComment, 'password': password}
        res = requests.post(url, data=data)
        if res.status_code == 200:
            print('Post Update Successful')
            print(res.json()["tistory"]["url"])
        else:
            print('Post Update Fail')
            print(res.json())
            print('.tistory 파일 삭제후 다시 시도해주세요')

if __name__ == '__main__':
    blog = Blog()