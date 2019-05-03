import sys
import simplestatistics as st

from PyQt5 import QtWidgets, uic

import matplotlib
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

matplotlib.use('QT5Agg')

import matplotlib.pylab as plt


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('theUI.ui', self)

        # Event Handling

        # General tab
        self.general_add_btn.clicked.connect(self.general_add)
        self.general_calc_btn.clicked.connect(self.general_calc)
        self.general_clear_btn.clicked.connect(self.general_lst_clear)

        # Correlation tab
        self.corr_add_btn.clicked.connect(self.corr_add)
        self.corr_calc_btn.clicked.connect(self.corr_calc)
        self.corr_clear_btn.clicked.connect(self.corr_table_clear)

        # Pie chart tab
        self.pie_add_btn.clicked.connect(self.pie_add)
        self.pie_draw_btn.clicked.connect(self.draw_pie_graph)
        self.pie_clear_btn.clicked.connect(self.pie_table_clear)

        # Bar chart tab
        self.bar_add_btn.clicked.connect(self.bar_add)
        self.bar_draw_btn.clicked.connect(self.draw_bar_graph)
        self.bar_clear_btn.clicked.connect(self.bar_table_clear)

        # Box plot tab
        self.box_add_btn.clicked.connect(self.box_add)
        self.box_draw_btn.clicked.connect(self.draw_box_graph)
        self.box_clear_btn.clicked.connect(self.box_table_clear)

        # Histogram
        self.histo_add_btn.clicked.connect(self.histo_add)
        self.histo_draw_btn.clicked.connect(self.histo_draw)
        self.histo_clear_btn.clicked.connect(self.histo_clear_table)

    # ---------------------------------------------General Tab-------------------------------------------------

    def general_add(self):
        try:
            value = float(self.general_input_lineEdit.text())
            self.general_lst.addItem(str(value))
            self.general_input_lineEdit.clear()
        except ValueError:
            self.value_error_msg()

    def general_calc(self):
        try:
            data = []
            for item in range(self.general_lst.count()):
                data.append(float(self.general_lst.item(item).text()))

            self.mean_lineEdit.setText(str(st.mean(data)))
            self.mode_lineEdit.setText(str(st.mode(data)))
            self.median_lineEdit.setText(str(st.median(data)))
            self.standardDeviation_lineEdit.setText(str(st.standard_deviation(data)))
        except ZeroDivisionError:
            self.no_data_msg()

    def general_lst_clear(self):
        self.general_lst.clear()

    # ------------------------------------------------Correlation Tab--------------------------------------------------

    def corr_add(self):
        try:
            xValue = float(self.corr_inputX_lineEdit.text())
            yValue = float(self.corr_inputY_lineEdit.text())
            self.corr_inputX_lineEdit.clear()
            self.corr_inputY_lineEdit.clear()
            self.corr_table.insertRow(self.corr_table.rowCount())
            self.corr_table.setItem(self.corr_table.rowCount() - 1, 0, QTableWidgetItem(str(xValue)))
            self.corr_table.setItem(self.corr_table.rowCount() - 1, 1, QTableWidgetItem(str(yValue)))
        except ValueError:
            self.value_error_msg()

    def corr_calc(self):
        try:
            xValues = []
            yValues = []
            for row in range(self.corr_table.rowCount()):
                xValues.append(float(self.corr_table.item(row, 0).text()))
                yValues.append(float(self.corr_table.item(row, 1).text()))

            self.corr_result_lineEdit.setText(str(st.correlate(xValues, yValues)))
        except ValueError:
            self.no_data_msg()

    def corr_table_clear(self):
        self.clear_table(self.corr_table, 'X', 'Y')

    # --------------------------------------------------Pie chart tab----------------------------------------------

    def pie_add(self):
        self.add_Sdata_to_table(self.pie_chart_table, self.pie_inputX_lineEdit, self.pie_inputY_lineEdit)

    def draw_pie_graph(self):
        plt.clf()
        x, y = self.get_Sdata_from_table(self.pie_chart_table)
        fig, ax1 = plt.subplots()
        x2 = [1, 98, 84, 62]
        y2 = ["amr", "ahmed", "mohamed", "hassan"]
        ax1.pie(x, labels=y, startangle=90, autopct="%1.1f%%    ")
        plt.show()

    def pie_table_clear(self):
        self.clear_table(self.pie_chart_table, "Data", "Name")

    # --------------------------------------------------Bar chart tab----------------------------------------------

    def bar_add(self):
        self.add_data_to_table(self.bar_chart_table, self.bar_inputX_lineEdit, self.bar_inputY_lineEdit)

    def draw_bar_graph(self):
        plt.clf()
        x, y = self.get_data_from_table(self.bar_chart_table)
        fig, ax1 = plt.subplots()
        ax1.bar(x, y)
        ax1.grid(True)
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")
        plt.show()

    def bar_table_clear(self):
        self.clear_table(self.bar_chart_table, "X", "Y")

    # ------------------------------------------------------Box plot-----------------------------------------------

    def box_add(self):
        try:
            value = float(self.box_inputX_lineEdit.text())
            self.box_inputX_lineEdit.clear()
            self.box_plot_table.insertRow(self.box_plot_table.rowCount())
            self.box_plot_table.setItem(self.box_plot_table.rowCount() - 1, 0, QTableWidgetItem(str(value)))
        except ValueError:
            self.value_error_msg()

    def draw_box_graph(self):
        plt.clf()
        data = []
        for row in range(self.box_plot_table.rowCount()):
            data.append(float((self.box_plot_table.item(row, 0).text())))

        fig, ax1 = plt.subplots()
        ax1.boxplot(data, vert=False)
        ax1.grid(True)
        plt.show()

    def box_table_clear(self):
        self.clear_table(self.box_plot_table, "Data")

    # ---------------------------------------------Histogram------------------------------------------------------------

    def histo_add(self):
        try:
            value = float(self.histo_inputX_lineEdit.text())
            self.histo_inputX_lineEdit.clear()
            self.histo_table.insertRow(self.histo_table.rowCount())
            self.histo_table.setItem(self.histo_table.rowCount() - 1, 0, QTableWidgetItem(str(value)))
        except ValueError:
            self.value_error_msg()

    def histo_draw(self):
        plt.clf()
        data = []
        for row in range(self.histo_table.rowCount()):
            data.append(float((self.histo_table.item(row, 0).text())))

        fig, ax1 = plt.subplots()
        ax1.hist(data)
        ax1.grid(True)
        plt.xlabel("Data")
        plt.show()

    def histo_clear_table(self):
        self.clear_table(self.histo_table, "Data")

    # ---------------------------------------------Main Functions-----------------------------------------------------

    def add_data_to_table(self, table, xInput, yInput):
        try:
            xValue = float(xInput.text())
            yValue = float(yInput.text())
            xInput.clear()
            yInput.clear()
            table.insertRow(table.rowCount())
            table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(str(xValue)))
            table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(str(yValue)))
        except ValueError:
            self.value_error_msg()

    def add_Sdata_to_table(self, table, xInput, yInput):
        try:
            xValue = float(xInput.text())
            yValue = yInput.text()
            xInput.clear()
            yInput.clear()
            table.insertRow(table.rowCount())
            table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(str(xValue)))
            table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(str(yValue)))
        except ValueError:
            self.value_error_msg()

    def get_data_from_table(self, table):
        x = []
        y = []
        for row in range(table.rowCount()):
            x.append(float(table.item(row, 0).text()))
            y.append(float(table.item(row, 1).text()))
        return x, y

    def get_Sdata_from_table(self, table):
        x = []
        y = []
        for row in range(table.rowCount()):
            x.append(float(table.item(row, 0).text()))
            y.append((table.item(row, 1).text()))
        return x, y

    def clear_table(self, table, Xcolumn, Ycolumn=''):
        table.clear()
        table.setHorizontalHeaderLabels([Xcolumn, Ycolumn])
        while table.rowCount() > 0:
            table.removeRow(0)

    def value_error_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Please make sure you enter only numbers and filled all the boxes")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def no_data_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("No enough data to calculate")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
