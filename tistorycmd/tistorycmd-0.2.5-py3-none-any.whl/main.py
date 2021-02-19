from .auth import *
from .server import *
from .blog import *
import mistune

USAGE = """USAGE:
    # 블로그 정보 보기
    tistorycmd info

    # 카테고리 목록 보기
    tistorycmd category

    # 글쓰기, 모든 내용수정시
    tistorycmd post <제목> <내용|파일경로> <category_id> <태그>
    
    # 내용만 수정
    tistorycmd update <내용|파일경로>
    """


def main():
    if len(sys.argv) < 2:
        print(USAGE, file=sys.stderr)
        return

    auth = Auth()  # 로그인, oauth, 토큰 관련 클래스
    blog = Blog()  # 글쓰기, 블로그 관련 클래스
    command = sys.argv[1]  # 메뉴
    if command == 'info':
        blog.info()
    elif command == 'category':
        blog.category_list()
    elif command == 'post':
        if len(sys.argv) < 4:
            print(USAGE, file=sys.stderr)
            return

        cont_path = os.path.abspath(sys.argv[3])  # 내용 파일 경로
        history_file = os.path.dirname(cont_path) + os.sep + '.tistory'  # 기존 등록내역파일

        title = sys.argv[2]  # 제목
        category = (len(sys.argv) > 4) and sys.argv[4] or ''  # 카테고리 (필수 x)
        tags = (len(sys.argv) > 5) and sys.argv[5] or ''  # 태그 (필수 x)
        content_md = ""  # 업로드할 파일내용 마크다운 형태
        overwrite_md = ""  # 덮어 쓸 내용 (이미지 계속 업로드 되는거 방지)

        # 이미지 있을 경우 파일 업로드
        with open(cont_path, 'r', encoding='UTF8') as fp:
            for line in fp:
                name_grp = re.search('(\!\[\s*)(\w+)(\s*\])(\(\s*)([^http:\/\/].*)(\s*\))', line)  # 이미지 형태 있는지 검사
                if (name_grp):
                    content_md += blog.file_upload(line, os.path.dirname(cont_path))
                    overwrite_md += blog.file_upload(line, os.path.dirname(cont_path))
                else:
                    content_md += line
                    overwrite_md += line

        # 파일내용 덮어쓰기 (이미지 계속 업로드 되는거 방지)
        if os.path.exists(cont_path):
            with open(cont_path, 'w', encoding='utf-8') as make_file:
                make_file.write(overwrite_md)

        content_html = mistune.markdown(content_md)  # 업로드 할 파일 내용 html 형태
        if (os.path.isfile(history_file)):
            # 글수정
            blog.post_edit(history_file, title, content_html, category, tags)
        else:
            # 글쓰기
            blog.post_write(history_file, title, content_html, category, tags)
    elif command == 'update':
        if not sys.argv[2]:
            print(USAGE, file=sys.stderr)
            return

        cont_path = os.path.abspath(sys.argv[2])  # 내용 파일 경로
        history_file = os.path.dirname(cont_path) + os.sep + '.tistory'  # 기존 등록내역파일

        # history 파일이 없을경우
        if not os.path.exists(history_file):
            print(".tistory 파일이 없습니다.")
            return

        # history 파일 읽기
        with open(history_file, 'r') as f:
            history = json.load(f)
            postId = ("postId" in history) and history['postId'] or ''
            title = ("title" in history) and history['title'] or ''  # 제목
            category = ("category" in history) and history['category'] or ''  # 카테고리 (필수 x)

        # postId 값 없을때
        if not postId:
            print('.history 파일 삭제후 다시 시도해보시기 바랍니다.')

        post_info = blog.post_read(postId)
        if post_info:
            title = post_info["title"]  # 제목
            category = post_info["categoryId"]  # 카테고리 (필수 x)
            content_md = ""  # 업로드할 파일내용 마크다운 형태
            overwrite_md = ""  # 덮어 쓸 내용 (이미지 계속 업로드 되는거 방지)

        # 이미지 있을 경우 파일 업로드
        with open(cont_path, 'r', encoding='UTF8') as fp:
            for line in fp:
                name_grp = re.search('(\!\[\s*)(\w+)(\s*\])(\(\s*)([^http:\/\/].*)(\s*\))', line)  # 이미지 형태 있는지 검사
                if (name_grp):
                    content_md += blog.file_upload(line, os.path.dirname(cont_path))
                    overwrite_md += blog.file_upload(line, os.path.dirname(cont_path))
                else:
                    content_md += line
                    overwrite_md += line

        # 파일내용 덮어쓰기 (이미지 계속 업로드 되는거 방지)
        if os.path.exists(cont_path):
            with open(cont_path, 'w', encoding='utf-8') as make_file:
                make_file.write(overwrite_md)

        content_html = mistune.markdown(content_md)  # 업로드 할 파일 내용 html 형태

        blog.contents_update(postId, title, content_html, category)
    else:
        print(USAGE, file=sys.stderr)
        return