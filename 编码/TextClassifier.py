from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtGui, QtCore
import sys
import requests
from bs4 import BeautifulSoup
import json
import jsonpath
import pymysql
import datetime
from wordcloud import WordCloud
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
import pandas as pd
import pickle

class Table_log(QMainWindow):
    def __init__(self):
        super(Table_log, self).__init__()
        self.ui = uic.loadUi("./temp_and_file/log.ui")
        self.ui.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.ui.PushButton_log.clicked.connect(self.log)
        self.ui.PushButton_reg.clicked.connect(self.reg)

    def log(self):
        account_input = self.ui.lineEdit_account.text()
        password_input = self.ui.lineEdit_password.text()
        if self.ui.checkBox_admin.isChecked():
            user_type = '管理员'
        else:
            user_type = '用户'
        if len(account_input) != 8:
            self.ui.label_info.setText("请输入8位字符账号!")
        else:
            if len(password_input) < 6 or len(password_input) > 12:
                self.ui.label_info.setText("请输入6-12位字符密码!")
            else:
                if self.id_exist(account_input, user_type):
                    if user_type == '用户':
                        sql = 'select Password from user where Account = %s'
                        try:
                            cursor.execute(sql, account_input)
                            db.commit()
                        except:
                            db.rollback()
                        pw = cursor.fetchall()[0][0]
                        if pw == password_input:
                            ol_time = datetime.datetime.now()
                            sql = 'update user set ol_time = %s where Account = %s'
                            value = (ol_time, account_input)
                            try:
                                cursor.execute(sql, value)
                                db.commit()
                            except:
                                db.rollback()
                            with open('./temp_and_file/account_now.txt', 'w', encoding='utf-8') as fp:
                                fp.write(account_input)
                            self.user = Table_user()
                            self.user.ui.setWindowTitle("TextClassifier")
                            self.user.ui.setWindowIcon(QtGui.QIcon('./temp_and_file/icon.ico'))
                            self.user.ui.show()
                            self.ui.close()
                        else:
                            self.ui.label_info.setText("密码错误!")
                    else:
                        sql = 'select Password from admin where Account = %s'
                        try:
                            cursor.execute(sql, account_input)
                            db.commit()
                        except:
                            db.rollback()
                        pw = cursor.fetchall()[0][0]
                        if pw == password_input:
                            ol_time = datetime.datetime.now()
                            sql = 'update admin set ol_time = %s where Account = %s'
                            value = (ol_time, account_input)
                            try:
                                cursor.execute(sql, value)
                                db.commit()
                            except:
                                db.rollback()
                            with open('./temp_and_file/account_now.txt', 'w', encoding='utf-8') as fp:
                                fp.write(account_input)
                            self.admin = Table_admin()
                            self.admin.ui.setWindowTitle("TextClassifier")
                            self.admin.ui.setWindowIcon(QtGui.QIcon('./temp_and_file/icon.ico'))
                            self.admin.ui.show()
                            self.ui.close()
                        else:
                            self.ui.label_info.setText("密码错误!")
                else:
                    self.ui.label_info.setText("账号不存在，请先注册账号!")

    def reg(self):
        self.ui.close()
        self.reg = Table_reg()
        self.reg.ui.setWindowTitle("TextClassifier")
        self.reg.ui.setWindowIcon(QtGui.QIcon('./temp_and_file/icon.ico'))
        self.reg.ui.show()

    def id_exist(self, Account, user_type):
        # 从数据库中查找是否有输入的账号
        if user_type == "用户":
            sql = 'select Account from user where Account = %s'
            try:
                cursor.execute(sql, (Account))
                db.commit()
            except:
                db.rollback()
        else:
            sql = 'select Account from admin where Account = %s'
            try:
                cursor.execute(sql, (Account))
                db.commit()
            except:
                db.rollback()
        data = cursor.fetchall()
        if data:
            return True
        else:
            return False

class Table_reg(QMainWindow):
    def __init__(self):
        super(Table_reg, self).__init__()
        self.ui = uic.loadUi("./temp_and_file/reg.ui")
        self.ui.pushButton_reg.clicked.connect(self.reg)
        self.ui.pushButton_return.clicked.connect(self.return_log)
        self.ui.lineEdit_pswd.setEchoMode(QLineEdit.Password)
        self.ui.lineEdit_pswd_2.setEchoMode(QLineEdit.Password)

    def reg(self):
        Account = self.ui.lineEdit_account.text()  # 获取账号
        Password = self.ui.lineEdit_pswd.text()  # 获取密码
        Password_2 = self.ui.lineEdit_pswd_2.text()  # 确认密码
        if self.ui.checkBox_type.isChecked():
            user_type = '管理员'
        else:
            user_type = '用户'
        if len(Account) != 8:
            self.ui.label_info.setText("请输入8位数字账号!")
        else:
            if self.id_exist(Account, user_type):
                self.ui.label_info.setText("该用户名已存在!")
            else:
                if len(Password) < 6 or len(Password) > 12:
                    self.ui.label_info.setText("请输入6-12位字符密码!")
                else:
                    if Password != Password_2:
                        self.ui.label_info.setText("确认密码输入不一致!")
                    else:
                        if user_type == "用户":
                            sql = 'insert into user (Account, Password) VALUE (%s, %s)'
                            value = (Account, Password)
                            try:
                                cursor.execute(sql, value)
                                db.commit()
                            except:
                                db.rollback()
                        else:
                            sql = 'insert into admin (Account, Password) VALUE (%s, %s)'
                            value = (Account, Password)
                            try:
                                cursor.execute(sql, value)
                                db.commit()
                            except:
                                db.rollback()
                        self.ui.label_info.setText("注册成功!")

    def return_log(self):
        self.ui.close()
        self.log = Table_log()
        self.log.ui.setWindowTitle("TextClassifier")
        self.log.ui.setWindowIcon(QtGui.QIcon('./temp_and_file/icon.ico'))
        self.log.ui.show()

    def id_exist(self, Account, user_type):
        if user_type == "用户":
            sql = 'select Account from user where Account = %s'
            try:
                cursor.execute(sql, Account)
                db.commit()
            except:
                db.rollback()
        else:
            sql = 'select Account from admin where Account = %s'
            try:
                cursor.execute(sql, Account)
                db.commit()
            except:
                db.rollback()
        data = cursor.fetchall()
        if data:
            return True
        else:
            return False

class Table_admin(QMainWindow):
    def __init__(self):
        super(Table_admin, self).__init__()
        self.ui = uic.loadUi("./temp_and_file/admin.ui")
        self.listener()
        self.account_now = None
        self.get_account()
        self.data_request()
        self.data_request_2()
        self.default_add()
        self.add_item()
        self.add_item_1()
        self.pre_crawl_flag = 0
        self.crawl_flag = 0

    def get_account(self):
        with open('./temp_and_file/account_now.txt', 'r', encoding='utf-8') as fp:
            self.account_now = fp.read()

    def listener(self):
        self.ui.pushButton_max.clicked.connect(self.get_max)
        self.ui.pushButton_preview.clicked.connect(self.pre_crawl)
        self.ui.pushButton_crawl.clicked.connect(self.crawl)
        self.ui.pushButton_save.clicked.connect(self.news_save)
        self.ui.pushButton_request.clicked.connect(self.data_request)
        self.ui.pushButton_view_content.clicked.connect(self.content_view)
        self.ui.pushButton_word_freq.clicked.connect(self.wordcloud)
        self.ui.pushButton_delete.clicked.connect(self.delete_news)
        self.ui.pushButton_request_2.clicked.connect(self.data_request_2)
        self.ui.pushButton_classify.clicked.connect(self.classify)
        self.ui.pushButton_reset.clicked.connect(self.reset)
        self.ui.pushButton_change_cate.clicked.connect(self.change_cate)
        self.ui.pushButton_refit.clicked.connect(self.refit)
        self.ui.pushButton_edit.clicked.connect(self.edit)
        self.ui.pushButton_logout.clicked.connect(self.logout)
        self.ui.pushButton_reflash_add.clicked.connect(self.reflash_add)

#################### 新闻爬取 ###################

    def add_item(self):
        self.ui.comboBox.addItem('新闻')
        self.ui.comboBox.addItem('国内')
        self.ui.comboBox.addItem('国际')
        self.ui.comboBox.addItem('社会')
        self.ui.comboBox.addItem('法治')
        self.ui.comboBox.addItem('文娱')
        self.ui.comboBox.addItem('科技')
        self.ui.comboBox.addItem('生活')

    def get_url(self, type):
        switcher = {
            '新闻': 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/news_1.jsonp?cb=news',
            '国内': 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp?cb=china',
            '国际': 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/world_1.jsonp?cb=world',
            '社会': 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/society_1.jsonp?cb=society',
            '法治': 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/law_1.jsonp?cb=law',
            '文娱': 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/ent_1.jsonp?cb=ent',
            '科技': 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/tech_1.jsonp?cb=tech',
            '生活': 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/life_1.jsonp?cb=life'
        }
        return switcher.get(type, 'wrong value')

    def get_len(self, type):
        switcher = {
            '新闻': 5,
            '国内': 6,
            '国际': 6,
            '社会': 8,
            '法治': 4,
            '文娱': 4,
            '科技': 5,
            '生活': 5
        }
        return switcher.get(type, 'wrong value')

    def get_max(self):
        self.ui.spinBox_n.setValue(99)

    def pre_crawl(self):
        self.ui.label_3.setText('请稍候')
        self.ui.textBrowser_preview.clear()
        news_type = self.ui.comboBox.currentText()
        url = self.get_url(news_type)
        num = self.ui.spinBox_n.value()
        headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.content, 'html.parser')
            content = soup.prettify()
            l = self.get_len(news_type)
            content = content[l:-2]
            with open('./temp_and_file/temp.json', 'w', encoding='utf-8') as fp:
                fp.write(content)
            obj = json.load(open('./temp_and_file/temp.json', encoding='utf-8'))
            title_lst = jsonpath.jsonpath(obj, '$..title')
            url_lst = jsonpath.jsonpath(obj, '$..url')
            if num > len(title_lst):
                num = len(title_lst)
                self.ui.spinBox_n.setValue(num)
            self.url_lst = url_lst[:num]
            self.title_lst = title_lst[:num]
            for i in range(num):
                self.ui.textBrowser_preview.append('【' + str(i+1) + '】' + title_lst[i] + '\n')
            self.pre_crawl_flag = 1
            self.ui.label_3.setText('预爬取成功!')
        except Exception as a:
            self.ui.textBrowser_preview.setText('预爬取失败!')

    def crawl(self):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
        if self.pre_crawl_flag == 0:
            self.ui.label_3.setText('请先完成预爬取!')
        else:
            self.ui.label_3.setText('爬取中，请耐心等待!')
            self.ui.textBrowser_preview.clear()
            lst = self.url_lst
            lose_num = 0
            self.index_lst = []
            self.content_lst = []
            for i in range(len(lst)):
                try:
                    res = requests.get(url=lst[i], headers=headers)
                    soup = BeautifulSoup(res.content, 'html.parser')
                    text = soup.select_one('.content_area').text.strip()
                    text_ = text.split('　　')
                    text_line = ''
                    for t in text_:
                        text_line += '\n　　' + t
                    self.content_lst.append(text)
                    self.ui.textBrowser_preview.append('>>>>>>>' + str(i+1) + text_line +'\n \n \n')
                    self.index_lst.append(i)
                except:
                    lose_num += 1
            self.crawl_flag = 1
            self.ui.label_3.setText('爬取失败' + str(lose_num) + '条!')

    def news_save(self):
        if self.crawl_flag == 1:
            now_time = datetime.datetime.now()
            index = 0
            lose_num = 0
            for i in self.index_lst:
                sql = 'insert into news (title, content, url, admin, dl_time) VALUE (%s, %s, %s, %s, %s)'
                value = (self.title_lst[i], self.content_lst[index], self.url_lst[i], self.account_now, now_time)
                index += 1
                try:
                    cursor.execute(sql, value)
                    db.commit()
                except:
                    db.rollback()
                    lose_num += 1
            self.ui.label_3.setText('保存完成，失败' + str(lose_num) + '条!')
        else:
            self.ui.label_3.setText('请先爬取!')

#################### 数据预处理 ###################

    def data_request(self):
        try:
            sql = 'select title, url from news where admin = %s'
            try:
                cursor.execute(sql, self.account_now)
                db.commit()
            except:
                db.rollback()
            result = cursor.fetchall()
            row = cursor.rowcount
            vol = len(result[0])
            self.ui.tableWidget.setRowCount(row)
            self.ui.tableWidget.setColumnCount(vol)
            self.ui.tableWidget.verticalHeader().setDefaultSectionSize(20)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.ui.tableWidget.setAlternatingRowColors(True)
            self.ui.tableWidget.setHorizontalHeaderLabels(['title', 'url'])
            for i in range(row):
                for j in range(vol):
                    data = QTableWidgetItem(str(result[i][j]))
                    self.ui.tableWidget.setItem(i, j, data)
        except:
            self.ui.tableWidget.clearContents()
            self.ui.label_4.setText('未找到数据!')

    def content_view(self):
        self.ui.textBrowser_content.clear()
        try:
            select_row = self.ui.tableWidget.currentRow()
            select_url = self.ui.tableWidget.item(select_row, 1).text()
            sql = 'select content from news where url = %s'
            try:
                cursor.execute(sql, select_url)
                db.commit()
            except:
                db.rollback()
            select_content = cursor.fetchall()[0][0]
            select_content = select_content.split('　　')
            for t in select_content:
                self.ui.textBrowser_content.append('　　' + t)
        except:
            self.ui.label_4.setText('请先选中新闻!')

    def wordcloud(self):
        try:
            select_row = self.ui.tableWidget.currentRow()
            select_url = self.ui.tableWidget.item(select_row, 1).text()
            sql = 'select content from news where url = %s'
            try:
                cursor.execute(sql, select_url)
                db.commit()
            except:
                db.rollback()
            txt = str(cursor.fetchall()[0][0])
            words = jieba.lcut(txt)
            newtxt = ''.join(words)
            wordcloud = WordCloud(background_color="white", font_path='./temp_and_file/msyh.ttc', width=540, height=370).generate(newtxt)
            wordcloud.to_file('./temp_and_file/wordcloud.png')
            pixmap = QPixmap('./temp_and_file/wordcloud.png')
            self.ui.label_wordcloud.setPixmap(pixmap)
        except:
            self.ui.label_4.setText('请先选中新闻!')

    def delete_news(self):
        self.ui.textBrowser_content.clear()
        try:
            select_row = self.ui.tableWidget.currentRow()
            select_url = self.ui.tableWidget.item(select_row, 1).text()
            sql = 'select title from news where url = %s'
            try:
                cursor.execute(sql, select_url)
                db.commit()
            except:
                db.rollback()
            select_title = cursor.fetchall()[0][0]
            sql = 'delete from news where title = %s'
            try:
                cursor.execute(sql, select_title)
                db.commit()
            except:
                db.rollback()
            self.ui.textBrowser_content.setText('已删除《' + select_title + '》')
            self.data_request()
        except:
            self.ui.label_4.setText('请先选中新闻!')

#################### 文本分类 ###################

    def data_request_2(self):
        try:
            sql = 'select title, cate from news where admin = %s'
            try:
                cursor.execute(sql, self.account_now)
                db.commit()
            except:
                db.rollback()
            result = cursor.fetchall()
            row = cursor.rowcount
            vol = len(result[0])
            self.ui.tableWidget_2.setRowCount(row)
            self.ui.tableWidget_2.setColumnCount(vol)
            self.ui.tableWidget_2.setHorizontalHeaderLabels(['title', 'category'])
            for i in range(row):
                for j in range(vol):
                    data = QTableWidgetItem(str(result[i][j]))
                    self.ui.tableWidget_2.setItem(i, j, data)
            self.ui.tableWidget_2.verticalHeader().setDefaultSectionSize(20)
            self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.ui.tableWidget_2.setAlternatingRowColors(True)
        except:
            self.ui.tableWidget_2.clearContents()
            self.ui.label_5.setText('未找到数据!')

    def get_type_name(self, num):
        switcher = {
            0:'finance',
            1:'reality',
            2:'stocks',
            3:'education',
            4:'science',
            5:'society',
            6:'politics',
            7:'sports',
            8:'game',
            9:'entertainment'
        }
        return switcher.get(num, 'wrong value')

    def classify(self):
        try:
            with open('./temp_and_file/model.pkl', 'rb') as f:
                clf = pickle.load(f)
            with open('./temp_and_file/vectorizer.pkl', 'rb') as f:
                vectorizer = pickle.load(f)
            sql = 'select content from news where cate is null and admin = %s'
            try:
                cursor.execute(sql, self.account_now)
                db.commit()
            except:
                db.rollback()
            result = cursor.fetchall()
            data = [str(result[i][0]) for i in range(len(result))]
            data = pd.DataFrame({'content': data})
            data_seg = [' '.join(jieba.cut(text)) for text in data['content']]
            X = vectorizer.transform(data_seg)
            cates = clf.predict(X)
            data['cate'] = cates
            for i in range(len(cates)):
                sql = 'update news set cate = %s where content = %s'
                value = (self.get_type_name(data.loc[i, 'cate']), data.loc[i, 'content'])
                try:
                    cursor.execute(sql, value)
                    db.commit()
                except:
                    db.rollback()
            self.ui.label_5.setText('分类成功!')
            self.data_request_2()
        except:
            self.ui.label_5.setText('分类异常!')

    def reset(self):
        sql = 'update news set cate = null where cate is not null and admin = %s'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        self.ui.label_5.setText('已重置!')
        self.data_request_2()

    def add_item_1(self):
        self.ui.comboBox_2.addItem('finance')
        self.ui.comboBox_2.addItem('reality')
        self.ui.comboBox_2.addItem('stocks')
        self.ui.comboBox_2.addItem('education')
        self.ui.comboBox_2.addItem('science')
        self.ui.comboBox_2.addItem('society')
        self.ui.comboBox_2.addItem('politics')
        self.ui.comboBox_2.addItem('sports')
        self.ui.comboBox_2.addItem('game')
        self.ui.comboBox_2.addItem('entertainment')

    def change_cate(self):
        try:
            select_row = self.ui.tableWidget_2.currentRow()
            new_cate = self.ui.comboBox_2.currentText()
            select_title = self.ui.tableWidget_2.item(select_row, 0).text()
            sql = 'update news set cate = %s where title = %s'
            value = (new_cate, select_title)
            try:
                cursor.execute(sql, value)
                db.commit()
            except:
                db.rollback()
            self.ui.label_5.setText('修改成功!')
            self.data_request_2()
        except:
            self.ui.label_5.setText('修改失败!')

    def refit(self):
        try:
            data = pd.read_excel('./temp_and_file/train.xlsx')
            data_seg = [' '.join(jieba.cut(text)) for text in data['title']]
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(data_seg)
            clf = MultinomialNB(alpha=1)
            clf.fit(X, data['category'])
            with open('./temp_and_file/model.pkl', 'wb') as f:
                pickle.dump(clf, f)
            with open('./temp_and_file/vectorizer.pkl', 'wb') as f:
                pickle.dump(vectorizer, f)
            if self.ui.pushButton_refit.text() == '训练模型':
                self.ui.label_5.setText('模型训练成功!')
                self.ui.pushButton_refit.setText('更新模型')
            else:
                self.ui.label_5.setText('模型已更新!')
        except:
            self.ui.label_5.setText('模型训练失败!')

#################### 个人中心 ###################

    def default_add(self):
        pixmap = QPixmap('./temp_and_file/photo.png')
        self.ui.label_photo.setPixmap(pixmap)
        self.ui.label_ID.setText(self.account_now)
        sql = 'select * from news where admin = %s and cate is not null'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        count = cursor.rowcount
        self.ui.label_count.setText(str(count))
        sql = 'select nickname, p_introduction from admin where Account = %s'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        data = cursor.fetchall()
        nickname = data[0][0]
        introd = data[0][1]
        self.ui.label_nickname.setText(nickname)
        self.ui.label_introduction.setText(introd)
        try:
            sql = 'select cate as Category, count(title) as Count from news ' \
                  'where cate is not null and admin = %s group by cate'
            try:
                cursor.execute(sql, self.account_now)
                db.commit()
            except:
                db.rollback()
            result = cursor.fetchall()
            row = cursor.rowcount
            vol = len(result[0])
            self.ui.tableWidget_info.setRowCount(row)
            self.ui.tableWidget_info.setColumnCount(vol)
            self.ui.tableWidget_info.verticalHeader().setDefaultSectionSize(40)
            self.ui.tableWidget_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.ui.tableWidget_info.setAlternatingRowColors(True)
            self.ui.tableWidget_info.setHorizontalHeaderLabels(['Category', 'Count'])
            for i in range(row):
                for j in range(vol):
                    data = QTableWidgetItem(str(result[i][j]))
                    self.ui.tableWidget_info.setItem(i, j, data)
        except:
            pass
        '''
        try:
            pixmap = QPixmap('./temp_and_file/wordcloud_all.png')
            self.ui.label_cloud_all.setPixmap(pixmap)
        except:
            self.ui.label_cloud_all.setText('请刷新')
        '''

    def reflash_add(self):
        sql = 'select * from news where admin = %s and cate is not null'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        count = cursor.rowcount
        self.ui.label_count.setText(str(count))
        sql = 'select cate as Category, count(title) as Count from news ' \
              'where cate is not null and admin = %s group by cate'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        result = cursor.fetchall()
        row = cursor.rowcount
        vol = len(result[0])
        self.ui.tableWidget_info.setRowCount(row)
        self.ui.tableWidget_info.setColumnCount(vol)
        self.ui.tableWidget_info.verticalHeader().setDefaultSectionSize(40)
        self.ui.tableWidget_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_info.setAlternatingRowColors(True)
        self.ui.tableWidget_info.setHorizontalHeaderLabels(['Category', 'Count'])
        for i in range(row):
            for j in range(vol):
                data = QTableWidgetItem(str(result[i][j]))
                self.ui.tableWidget_info.setItem(i, j, data)
        sql = 'select content from news where admin = %s'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        #管理员的词云
        '''
        row = cursor.rowcount
        text = ''
        result = cursor.fetchall()
        for r in range(row):
            text += result[r][0]
        words = jieba.lcut(text)
        newtxt = ''.join(words)
        wordcloud = WordCloud(background_color="white", font_path='./temp_and_file/msyh.ttc', width=570,
                              height=200).generate(newtxt)
        wordcloud.to_file('./temp_and_file/wordcloud_all.png')
        pixmap = QPixmap('./temp_and_file/wordcloud_all.png')
        self.ui.label_cloud_all.setPixmap(pixmap)
        '''

    def edit(self):
        self.edit = Table_admin_edit()
        self.edit.ui.setWindowTitle("TextClassifier")
        self.edit.ui.setWindowIcon(QtGui.QIcon('./temp_and_file/icon.ico'))
        self.edit.ui.show()
        self.edit.signal_info.connect(self.edit_)
        self.edit.signal_pw.connect(self.change_pw)

    def edit_(self, nickname, introd):
        if len(introd) > 0:
            self.ui.label_introduction.setText(introd)
            sql = 'update admin set p_introduction = %s where Account = %s'
            value = (introd, self.account_now)
            try:
                cursor.execute(sql, value)
                db.commit()
            except:
                db.rollback()
        if len(nickname) > 0:
            self.ui.label_nickname.setText(nickname)
            sql = 'update admin set nickname = %s where Account = %s'
            value = (nickname, self.account_now)
            try:
                cursor.execute(sql, value)
                db.commit()
            except:
                db.rollback()

    def change_pw(self, pw_new):
        sql = 'update admin set Password = %s where Account = %s'
        value = (pw_new, self.account_now)
        try:
            cursor.execute(sql, value)
            db.commit()
        except:
            db.rollback()

    def logout(self):
        self.log = Table_log()
        self.log.ui.setWindowTitle("TextClassifier")
        self.log.ui.setWindowIcon(QtGui.QIcon('./temp_and_file/icon.ico'))
        self.log.ui.show()
        self.ui.close()

class Table_admin_edit(QMainWindow):
    signal_info = QtCore.pyqtSignal(str, str)
    signal_pw = QtCore.pyqtSignal(str)
    def __init__(self):
        super(Table_admin_edit, self).__init__()
        self.ui = uic.loadUi("./temp_and_file/admin_edit.ui")
        self.ui.pushButton_confirm.clicked.connect(self.edit_info)
        self.ui.pushButton_confirm_2.clicked.connect(self.change_pw)
        self.account_now = None
        self.get_account()

    def get_account(self):
        with open('./temp_and_file/account_now.txt', 'r', encoding='utf-8') as fp:
            self.account_now = fp.read()

    def edit_info(self):
        nickname = self.ui.lineEdit_nickname.text()
        introd = self.ui.textEdit_introduction.toPlainText()
        self.signal_info.emit(nickname, introd)
        self.ui.close()

    def change_pw(self):
        pw_old = self.ui.lineEdit_password_old.text()
        pw_new_1 = self.ui.lineEdit_password_new.text()
        pw_new_2 = self.ui.lineEdit_password_confirm.text()
        sql = 'select Password from admin where Account = %s'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        pw_real = cursor.fetchall()[0][0]
        if len(pw_new_1) < 6 or len(pw_new_1) > 12 or len(pw_old) < 6 or len(pw_old) > 12:
            self.ui.label_info.setText("请输入6-12位字符密码!")
        else:
            if pw_real != pw_old:
                self.ui.label_info.setText("密码错误!")
            else:
                if pw_new_1 != pw_new_2:
                    self.ui.label_info.setText("确认密码输入不一致!")
                else:
                    self.signal_pw.emit(pw_new_1)
                    self.ui.close()

class Table_user(QMainWindow):
    def __init__(self):
        super(Table_user, self).__init__()
        self.ui = uic.loadUi("./temp_and_file/user.ui")
        self.account_now = None
        self.get_account()
        self.add_item()
        self.data_request()
        self.default_add()
        self.listener()

    def listener(self):
        self.ui.pushButton_request.clicked.connect(self.data_request)
        self.ui.pushButton_view_content.clicked.connect(self.content_view)
        self.ui.pushButton_edit.clicked.connect(self.edit)
        self.ui.pushButton_logout.clicked.connect(self.logout)

#################### 主页 ###################

    def get_account(self):
        with open('./temp_and_file/account_now.txt', 'r', encoding='utf-8') as fp:
            self.account_now = fp.read()

    def add_item(self):
        self.ui.comboBox.addItem('all')
        self.ui.comboBox.addItem('finance')
        self.ui.comboBox.addItem('reality')
        self.ui.comboBox.addItem('stocks')
        self.ui.comboBox.addItem('education')
        self.ui.comboBox.addItem('science')
        self.ui.comboBox.addItem('society')
        self.ui.comboBox.addItem('politics')
        self.ui.comboBox.addItem('sports')
        self.ui.comboBox.addItem('game')
        self.ui.comboBox.addItem('entertainment')

    def data_request(self):
        try:
            search_key = self.ui.lineEdit_search.text()
            select_cate = self.ui.comboBox.currentText()
            if select_cate == 'all':
                if search_key == '':
                    sql = f"select title, url from news"
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()
                else:
                    sql = f"select title, url from news where title like '%{search_key}%'"
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()
            else:
                if search_key == '':
                    sql = f"select title, url from news where cate = %s"
                    try:
                        cursor.execute(sql, select_cate)
                        db.commit()
                    except:
                        db.rollback()
                else:
                    sql = f"select title, url from news where cate = {select_cate} and title like '%{search_key}%'"
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()
            result = cursor.fetchall()
            row = cursor.rowcount
            vol = len(result[0])
            self.ui.tableWidget.setRowCount(row)
            self.ui.tableWidget.setColumnCount(vol)
            self.ui.tableWidget.verticalHeader().setDefaultSectionSize(20)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.ui.tableWidget.setAlternatingRowColors(True)
            self.ui.tableWidget.setHorizontalHeaderLabels(['title', 'url'])
            for i in range(row):
                for j in range(vol):
                    data = QTableWidgetItem(str(result[i][j]))
                    self.ui.tableWidget.setItem(i, j, data)
        except:
            self.ui.tableWidget.clearContents()
            self.ui.label_4.setText('未找到数据!')

    def content_view(self):
        self.ui.textBrowser_content.clear()
        try:
            select_row = self.ui.tableWidget.currentRow()
            select_url = self.ui.tableWidget.item(select_row, 1).text()
            sql = 'select content from news where url = %s'
            try:
                cursor.execute(sql, select_url)
                db.commit()
            except:
                db.rollback()
            select_content = cursor.fetchall()[0][0]
            select_content = select_content.split('　　')
            for t in select_content:
                self.ui.textBrowser_content.append('　　' + t)
        except:
            self.ui.label_4.setText('请先选中新闻!')

#################### 个人中心 ###################

    def default_add(self):
        pixmap = QPixmap('./temp_and_file/photo.png')
        self.ui.label_photo.setPixmap(pixmap)
        self.ui.label_ID.setText(self.account_now)
        # sql = 'select * from news where admin = %s and cate is not null'
        # try:
        #     cursor.execute(sql, self.account_now)
        #     db.commit()
        # except:
        #     db.rollback()
        # count = cursor.rowcount
        # self.ui.label_count.setText(str(count))
        sql = 'select nickname, p_introduction from user where Account = %s'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        data = cursor.fetchall()
        nickname = data[0][0]
        introd = data[0][1]
        self.ui.label_nickname.setText(nickname)
        self.ui.label_introduction.setText(introd)
        # sql = 'select cate as Category, count(title) as Count from news ' \
        #       'where cate is not null and admin = %s group by cate'
        # try:
        #     cursor.execute(sql, self.account_now)
        #     db.commit()
        # except:
        #     db.rollback()
        # result = cursor.fetchall()
        # row = cursor.rowcount
        # vol = len(result[0])
        # self.ui.tableWidget_info.setRowCount(row)
        # self.ui.tableWidget_info.setColumnCount(vol)
        # self.ui.tableWidget_info.verticalHeader().setDefaultSectionSize(40)
        # self.ui.tableWidget_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.ui.tableWidget_info.setAlternatingRowColors(True)
        # self.ui.tableWidget_info.setHorizontalHeaderLabels(['Category', 'Count'])
        # for i in range(row):
        #     for j in range(vol):
        #         data = QTableWidgetItem(str(result[i][j]))
        #         self.ui.tableWidget_info.setItem(i, j, data)
        # try:
        #     pixmap = QPixmap('./temp_and_file/wordcloud_all.png')
        #     self.ui.label_cloud_all.setPixmap(pixmap)
        # except:
        #     self.ui.label_cloud_all.setText('请刷新')

    def reflash_add(self):
        sql = 'select * from news where admin = %s and cate is not null'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        count = cursor.rowcount
        self.ui.label_count.setText(str(count))
        sql = 'select cate as Category, count(title) as Count from news ' \
              'where cate is not null and admin = %s group by cate'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        result = cursor.fetchall()
        row = cursor.rowcount
        vol = len(result[0])
        self.ui.tableWidget_info.setRowCount(row)
        self.ui.tableWidget_info.setColumnCount(vol)
        self.ui.tableWidget_info.verticalHeader().setDefaultSectionSize(40)
        self.ui.tableWidget_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_info.setAlternatingRowColors(True)
        self.ui.tableWidget_info.setHorizontalHeaderLabels(['Category', 'Count'])
        for i in range(row):
            for j in range(vol):
                data = QTableWidgetItem(str(result[i][j]))
                self.ui.tableWidget_info.setItem(i, j, data)
        sql = 'select content from news where admin = %s'
        try:
            cursor.execute(sql, self.account_now)
            db.commit()
        except:
            db.rollback()
        row = cursor.rowcount
        text = ''
        result = cursor.fetchall()
        for r in range(row):
            text += result[r][0]
        words = jieba.lcut(text)
        newtxt = ''.join(words)
        wordcloud = WordCloud(background_color="white", font_path='./temp_and_file/msyh.ttc', width=570,
                              height=540).generate(newtxt)
        wordcloud.to_file('./temp_and_file/wordcloud_all.png')
        pixmap = QPixmap('./temp_and_file/wordcloud_all.png')
        self.ui.label_cloud_all.setPixmap(pixmap)

    def edit(self):
        self.edit = Table_admin_edit()
        self.edit.ui.setWindowTitle("TextClassifier")
        self.edit.ui.setWindowIcon(QtGui.QIcon('./temp_and_file/icon.ico'))
        self.edit.ui.show()
        self.edit.signal_info.connect(self.edit_)
        self.edit.signal_pw.connect(self.change_pw)

    def edit_(self, nickname, introd):
        if len(introd) > 0:
            self.ui.label_introduction.setText(introd)
            sql = 'update user set p_introduction = %s where Account = %s'
            value = (introd, self.account_now)
            try:
                cursor.execute(sql, value)
                db.commit()
            except:
                db.rollback()
        if len(nickname) > 0:
            self.ui.label_nickname.setText(nickname)
            sql = 'update user set nickname = %s where Account = %s'
            value = (nickname, self.account_now)
            try:
                cursor.execute(sql, value)
                db.commit()
            except:
                db.rollback()

    def change_pw(self, pw_new):
        sql = 'update user set Password = %s where Account = %s'
        value = (pw_new, self.account_now)
        try:
            cursor.execute(sql, value)
            db.commit()
        except:
            db.rollback()

    def logout(self):
        self.log = Table_log()
        self.log.ui.setWindowTitle("TextClassifier")
        self.log.ui.setWindowIcon(QtGui.QIcon('./temp_and_file/icon.ico'))
        self.log.ui.show()
        self.ui.close()

if __name__ == '__main__':
    db = pymysql.connect(host='localhost', user='root', password='Password_12345', database='text_classifier')
    cursor = db.cursor()
    app = QApplication(sys.argv)
    log = Table_log()
    log.ui.setWindowTitle("TextClassifier")
    log.ui.setWindowIcon(QtGui.QIcon('./temp_and_file/icon.ico'))
    log.ui.show()
    app.exec_()
    db.close()