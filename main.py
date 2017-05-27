# -*- coding:utf-8 -*-

import sys
from PyQt4 import QtGui, uic
import re
from lxml.html import fromstring, soupparser, html5parser, tostring, HtmlElement


Ui_MainWindow, QtBaseClass = uic.loadUiType('main_ui.ui')


class QtToPython(object):
    """
    获取Qt界面元素的Python类型值
    """
    @staticmethod
    def get_line_edit_unicode(line_edit):
        return line_edit.text().toUtf8().data().decode('utf-8')

    @staticmethod
    def get_line_edit_string(line_edit):
        return line_edit.text().toUtf8().data()

    @staticmethod
    def get_line_edit_int(line_edit):
        return int(line_edit.text().toUtf8().data())

    @staticmethod
    def get_text_edit_unicode(text_edit):
        return text_edit.toPlainText().toUtf8().data().decode('utf-8')

    @staticmethod
    def get_text_edit_str(text_edit):
        return text_edit.toPlainText().toUtf8().data()

    @staticmethod
    def get_text_edit_int(text_edit):
        return int(text_edit.toPlainText().toUtf8().data())

    @staticmethod
    def get_current_item_string(tree_widget, column):
        return tree_widget.currentItem().text(column).toUtf8().data() if tree_widget.currentItem() else ''


class MainUi(QtGui.QMainWindow, Ui_MainWindow, QtToPython):
    def __init__(self):
        super(MainUi, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(u'Python正则测试器 V0.1')
        self.run_button.clicked.connect(self.run_button_clicked)
        self.RE_XPATH = [self.get_re_result, self.get_xpath_result]
        self.RE_MODE = [re.S, 0]
        self.XPATH_MODE = [soupparser.fromstring, fromstring, html5parser.fromstring]

    @property
    def re_xpath(self):
        return 0 if self.re_button.isChecked() else 1


    def choice_mode(self):
        return self.re_mode_box.currentIndex() if self.re_button.isChecked() else self.xpath_mode_box.currentIndex()

    @property
    def re_text(self):
        return self.get_text_edit_unicode(self.regex_text_edit)

    @property
    def content_text(self):
        return self.get_text_edit_unicode(self.content_text_edit)

    @property
    def result_text(self):
        return self.get_text_edit_unicode(self.result_text_edit)

    def run_button_clicked(self):
        result = self.RE_XPATH[self.re_xpath](self.RE_MODE[self.choice_mode()] if self.re_xpath == 0 else self.XPATH_MODE[self.choice_mode()])
        self.result_text_edit.setPlainText(u"结果数量： %s" % str(len(result)) + '\n')
        for r in result:
            self.set_re_result(self.list_to_str(r))

    def set_result_text(self, text):
        return self.result_text_edit.appendPlainText(text+'\n')

    def get_re_result(self, mode):
        return re.findall(r'%s' % self.re_text, self.content_text, mode)

    def get_parser_result(self, parser):
        return parser(self.content_text).xpath(self.re_text)

    def get_xpath_result(self, parser):
        return [tostring(r, encoding='utf-8').decode('utf-8', 'ignore') if isinstance(r, HtmlElement) else r for r in self.get_parser_result(parser)]

    def set_re_result(self, text):
        return self.set_result_text(text)

    def list_to_str(self, lists):
        result_list = []
        if isinstance(lists, (list, tuple)):
            for item in lists:
                if isinstance(item, (list, tuple)):
                    list_str = self.list_to_str(item)
                    result_list.append(list_str)
                elif isinstance(item, int):
                    result_list.append(str(item))
                elif isinstance(item, unicode):
                    result_list.append(item.decode('utf-8'))
                elif isinstance(item, str):
                    result_list.append(item)
                else:
                    print u"未知类型转换错误！"
                    raise TypeError
            result_str = '[' + ','.join(result_list) + ']'
            return result_str
        return lists


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainUi()
    window.show()
    sys.exit(app.exec_())
