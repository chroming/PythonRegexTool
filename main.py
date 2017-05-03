# -*- coding:utf-8 -*-

import sys
from PyQt4 import QtGui, uic
import re


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

    def run_button_clicked(self):
        result = self.get_re_result(re.S)
        self.result_text_edit.setPlainText(u"结果数量： %s" % str(len(result)) + '\n')
        for r in result:
            self.set_re_result(self.list_to_str(r))

    @property
    def re_text(self):
        return self.get_text_edit_unicode(self.regex_text_edit)

    @property
    def content_text(self):
        return self.get_text_edit_unicode(self.content_text_edit)

    @property
    def result_text(self):
        return self.get_text_edit_unicode(self.result_text_edit)

    def set_result_text(self, text):
        return self.result_text_edit.appendPlainText(text+'\n')

    def get_re_result(self, mode):
        return re.findall(r'%s' % self.re_text, self.content_text, mode)

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
