import datetime
import sys
from selenium import webdriver
import webbrowser
from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import *


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        # 타이틀
        self.setWindowTitle("뉴스기사 검색 프로그램")

        # 변수 선언
        self.lst = []
        self.href = []
        self.page = 1

        # 크롬 드라이버 설정
        cd = "chromedriver"
        chOpt = webdriver.ChromeOptions()
        chOpt.add_argument("headless")
        chOpt.add_argument("lang=ko_KR")
        self.driver = webdriver.Chrome(cd, chrome_options=chOpt)

        # 검색어
        self.lnKeyword = QLineEdit("검색어를 입력해주세요.")

        # 정렬기준
        self.rdSort_0 = QRadioButton("관련도")
        self.rdSort_1 = QRadioButton("최신")
        self.rdSort_2 = QRadioButton("오래된")
        hbSort = QHBoxLayout()
        hbSort.addWidget(self.rdSort_0)
        hbSort.addWidget(self.rdSort_1)
        hbSort.addWidget(self.rdSort_2)
        grpSort = QGroupBox()
        grpSort.setLayout(hbSort)

        # 기사유형
        self.rdType_0 = QRadioButton("전체")
        self.rdType_1 = QRadioButton("동영상")
        self.rdType_2 = QRadioButton("포토")
        self.rdType_3 = QRadioButton("지면기사")
        hbType = QHBoxLayout()
        hbType.addWidget(self.rdType_0)
        hbType.addWidget(self.rdType_1)
        hbType.addWidget(self.rdType_2)
        hbType.addWidget(self.rdType_3)
        grpType = QGroupBox()
        grpType.setLayout(hbType)

        self.rdField_0 = QRadioButton("전체")
        self.rdField_1 = QRadioButton("제목만")
        hbFeild = QHBoxLayout()
        hbFeild.addWidget(self.rdField_0)
        hbFeild.addWidget(self.rdField_1)
        grpFeild = QGroupBox()
        grpFeild.setLayout(hbFeild)

        self.rdDate_0 = QRadioButton("전체")
        self.rdDate_1 = QRadioButton("1일")
        self.rdDate_2 = QRadioButton("1주")
        self.rdDate_3 = QRadioButton("1개월")
        self.rdDate_4 = QRadioButton("6개월")
        self.rdDate_5 = QRadioButton("1년")
        self.rdDate_6 = QRadioButton("선택")
        self.dtStart = QDateEdit(datetime.date.today())
        self.dtEnd = QDateEdit(datetime.date.today())
        hbDate_0 = QHBoxLayout()
        hbDate_0.addWidget(self.rdDate_0)
        hbDate_0.addWidget(self.rdDate_1)
        hbDate_0.addWidget(self.rdDate_2)
        hbDate_1 = QHBoxLayout()
        hbDate_1.addWidget(self.rdDate_3)
        hbDate_1.addWidget(self.rdDate_4)
        hbDate_1.addWidget(self.rdDate_5)
        frmDateCustom = QFormLayout()
        frmDateCustom.addRow("시작: ", self.dtStart)
        frmDateCustom.addRow("종료: ", self.dtEnd)
        hbDate_2 = QHBoxLayout()
        hbDate_2.addWidget(self.rdDate_6)
        hbDate_2.addLayout(frmDateCustom)
        vbDate = QVBoxLayout()
        vbDate.addLayout(hbDate_0)
        vbDate.addLayout(hbDate_1)
        vbDate.addLayout(hbDate_2)
        grpDate = QGroupBox()
        grpDate.setLayout(vbDate)

        frm = QFormLayout()
        frm.addRow("검색어:", self.lnKeyword)
        frm.addRow("정렬기준: ", grpSort)
        frm.addRow("기사유형: ", grpType)
        frm.addRow("검색범위: ", grpFeild)
        frm.addRow("검색기간: ", grpDate)

        self.model = QStandardItemModel(0, 1, self)
        self.model.setHorizontalHeaderLabels(["기사 제목"])
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setColumnWidth(0, 450)
        self.table.setFixedSize(450, 350)
        self.btnNext = QPushButton("다음")
        self.btnPrev = QPushButton("이전")
        self.btnSearch = QPushButton("검색")

        hbPageCnt = QHBoxLayout()
        hbPageCnt.addWidget(self.btnSearch)
        hbPageCnt.addStretch()
        hbPageCnt.addWidget(self.btnPrev)
        hbPageCnt.addWidget(self.btnNext)
        vbList = QVBoxLayout()
        vbList.addLayout(hbPageCnt)
        vbList.addWidget(self.table)

        hbMain = QHBoxLayout()
        hbMain.addLayout(frm)
        hbMain.addLayout(vbList)

        self.setLayout(hbMain)

        self.rdSort_0.toggle()
        self.rdType_0.toggle()
        self.rdField_0.toggle()
        self.rdDate_0.toggle()

        self.btnSearch.clicked.connect(self.searchNews)
        self.btnNext.clicked.connect(self.lstNext)
        self.table.clicked.connect(self.select)

    def lstNext(self):
        self.page += 10
        self.searchNews()

    def lstPrev(self):
        if self.page > 1:
            self.page -= 10
        self.searchNews()

    def closeEvent(self, QCloseEvent):
        self.driver.close()

    def searchNews(self):
        if self.sender().text() == "검색":
            self.page = 1
        if self.rdSort_0.isChecked():
            sort = "&sort=0"
        if self.rdSort_1.isChecked():
            sort = "&sort=1"
        if self.rdSort_2.isChecked():
            sort = "&sort=2"
        if self.rdType_0.isChecked():
            ntype = "&photo=0"
        if self.rdType_1.isChecked():
            ntype = "&photo=1"
        if self.rdType_2.isChecked():
            ntype = "&photo=2"
        if self.rdType_3.isChecked():
            ntype = "&photo=3"
        if self.rdField_0.isChecked():
            feild = "&field=0"
        if self.rdField_1.isChecked():
            feild = "&field=1"

        url = "https://search.naver.com/search.naver?where=news&query=" \
              + self.lnKeyword.text() + sort + ntype + feild + "&start={}".format(self.page)
        print(url)
        self.driver.get(url)
        self.lst = self.driver.find_elements_by_class_name("news_tit")
        self.apply_lst()

    def apply_lst(self):
        self.href.clear()
        self.model.removeRows(0, self.model.rowCount())
        self.model.setRowCount(len(self.lst))
        self.model.setVerticalHeaderLabels(['' for i in range(len(self.lst))])
        for idx, pre in enumerate(self.lst):
            self.model.setData(self.model.index(idx, 0), pre.text)
            self.href.append(pre.get_attribute("href"))

    def select(self, e):
        webbrowser.open(self.href[e.row()])

if __name__ == "__main__":
    app = QApplication([])
    form = Form()
    form.show()
    sys.exit(app.exec_())