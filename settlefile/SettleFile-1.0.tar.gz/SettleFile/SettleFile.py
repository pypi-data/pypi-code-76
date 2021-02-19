import os


class SettleFile:
    def __init__(self, file_name, pattern, long=False, encoding=None):
        self.file_name = file_name
        self.pattern = pattern
        self.long = long
        self.encoding = encoding

    def read_file(self):
        try:
            with open(self.file_name, self.pattern, encoding=self.encoding) as f:
                if self.long:
                    content = f.readlines()
                    print(''.join(content))
                else:
                    content = f.read()
                    print(content)
        except FileNotFoundError as e:
            print(e)
        except UnicodeDecodeError as e:
            print(e)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)

    def write_file(self, content):
        if os.path.exists(self.file_name):
            choice = input('文件已存在，是否继续(是/否)？')
            if choice == '是':
                try:
                    with open(self.file_name, self.pattern, encoding=self.encoding) as f:
                        if self.long:
                            f.writelines(content)
                        else:
                            f.write(content)
                except TypeError:
                    print('长数据缺少long参数，请添加long=True参数')
                except ValueError:
                    print('文件读写模式错误！')
                except Exception as e:
                    print(e)
            else:
                print('文件未更改！')
        else:
            try:
                with open(self.file_name, self.pattern, encoding=self.encoding) as f:
                    if self.long:
                        f.writelines(content)
                    else:
                        f.write(content)
            except TypeError:
                print('长数据缺少long参数，请添加long=True参数')
            except ValueError:
                print('文件读写模式错误！')
            except Exception as e:
                print(e)


file = SettleFile('3.txt', 'w', long=True, encoding='utf8')
file.read_file()
# file.write_file(['gsdg', 'sgsfdg'])



