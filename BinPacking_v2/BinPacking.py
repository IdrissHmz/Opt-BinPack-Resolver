from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys
from imports import *
from Heuristics import *
from BranchBound import branchAndBound
from SimulatedAnnealing import recuit_simule
from GeneticAlgorithm import AG
from TabuSearch import TS
import BestHeuris
from SA_me import RS
from TB_me import RT,test_RT
from Hyperize import get_params_AG, get_params_SA, get_params_TS
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# meta = []
# items = []

#class MyTable
class MyTable(QTableWidget):
    """docstring for MyTable"""
    #global fileName

    def __init__(self, parent=None):
        super(MyTable, self).__init__(1, 1, parent)
        headertitle = ("Poids", "")
        self.setHorizontalHeaderLabels(headertitle)
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cellChanged.connect(self._cellclicked)

    @QtCore.pyqtSlot(int, int)
    def _cellclicked(self, r, c):
        it = self.item(r, c)
        it.setTextAlignment(QtCore.Qt.AlignCenter)

    @QtCore.pyqtSlot()
    def _addrow(self):
        rowcount = self.rowCount()
        self.insertRow(rowcount)
        a_window.nbr_text.setText(str(int(a_window.nbr_text.text()) + 1))

    @QtCore.pyqtSlot()
    def _removerow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount() - 1)

    def loadInstance(self):
        global fileName
        global meta
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        #global meta
        
        if fileName:
            items,meta,capacity,n = instance_v2(fileName)
            print(meta)
            print(len(meta))
            c = capacity
            if c<500 : 
                famille = 'Facile'
            elif c<10000 : 
                famille = 'Moyenne'  
            else : 
                famille = 'Difficile' 

            if n <= 50 : 
                nbr = 'Tres Petite'
            elif n <= 100 : 
                nbr = 'Petite'  
            elif n <= 200 : 
                nbr = 'Moyenne'
            elif n <= 500 : 
                nbr = 'Grande'      
            else : 
                nbr = 'Tres Grande'    


            a_window.nbr_text.setText(str(nbr))
            a_window.capacity_text.setText(str(c))
            a_window.famille_text.setText(str(famille))
            a_window.diff_text.setText(str(n))
            self.setRowCount(0)
            for i, item in enumerate(items):
                row = self.rowCount()
                self.insertRow(row)
                self.setItem(i, 0, QTableWidgetItem(str(item)))
                #self.setItem(i, 1, QTableWidgetItem(str(item[1])))
            best_heuris = BestHeuris.bestHeuristique(famille, n)
            best_ag = BestHeuris.bestAg(famille, n)
            best_rs = BestHeuris.bestRS(famille, n)
            best_meta = BestHeuris.bestMeta(famille, n)
            best_method = BestHeuris.bestMethod(famille, n)
            a_window.table_widget.tab2.best_text.setText(best_heuris)
            a_window.table_widget.tab3.best_ag_text.setText(best_ag)
            a_window.table_widget.tab3.best_rs_text.setText(best_rs)
            a_window.table_widget.tab3.best_text.setText(best_meta)
            a_window.best_method_text.setText(best_method)

    # def showResult(self):

    #     items = []
    #     for row in range(self.rowCount() - 1):
    #         weight = int(self.item(row, 0).text())
    #         value = int(self.item(row, 1).text())
    #         items.append([weight, value])
    #     capacity = int(a_window.capacity_text.text())
    #     start = time.time()
    #     solution = knapsack_dp(items, capacity)
    #     solution_items = solution[2]
    #     end = time.time()
    #     result = a_window.table_widget.tab1.result_table
    #     result.setRowCount(0)
    #     for i, itemSol in enumerate(solution_items):
    #         row = result.rowCount()
    #         result.insertRow(row)
    #         result.setItem(i, 0, QTableWidgetItem(str(itemSol[0])))
    #         result.setItem(i, 1, QTableWidgetItem(str(itemSol[1])))

    #     a_window.table_widget.tab1.StatsTable.setItem(0, 0, QTableWidgetItem(str(solution[0])))
    #     a_window.table_widget.tab1.StatsTable.setItem(1, 0, QTableWidgetItem(str(solution[1])))
    #     a_window.table_widget.tab1.StatsTable.setItem(2, 0, QTableWidgetItem(str((end - start) * 1000) + "ms"))

    def showResult2(self):

        items = []
        for row in range(self.rowCount()):
            weight = int(self.item(row, 0).text())
            items.append(weight)
        capacity = int(a_window.capacity_text.text())
        start = time.time()
        solution = branchAndBound(items, capacity)
        solution_items = solution[1]
        solution_nbr = solution[0]
        end = time.time()
        result = a_window.table_widget.tab1.result_table2
        result.setRowCount(0)
        for i, itemSol in enumerate(solution_items):
            row = result.rowCount()
            result.insertRow(row)
            result.setItem(i, 0, QTableWidgetItem(str(items[i])))
            result.setItem(i, 1, QTableWidgetItem(str(itemSol)))

        a_window.table_widget.tab1.StatsTable2.setItem(0, 0, QTableWidgetItem(str(solution[0])))
        #a_window.table_widget.tab1.StatsTable2.setItem(1, 0, QTableWidgetItem(str(solution[1])))
        a_window.table_widget.tab1.StatsTable2.setItem(1, 0, QTableWidgetItem(str(solution[2]) + "s"))

    def showResultGreedy1(self):

        items = []
        for row in range(self.rowCount()):
            weight = int(self.item(row, 0).text())
            items.append(weight)
            #value = int(self.item(row, 1).text())
            #items.append([weight, value])
        # print(items)
        capacity = int(a_window.capacity_text.text())
        start = time.time()
        solution = heuristic_FFD(items, capacity)
        solution_items = solution[1]
        solution_nbr = solution[0]
        end = time.time()
        result = a_window.table_widget.tab2.result_table
        result.setRowCount(0)
        for i, itemSol in enumerate(solution_items):
            row = result.rowCount()
            result.insertRow(row)
            result.setItem(i, 0, QTableWidgetItem(str(items[i])))
            result.setItem(i, 1, QTableWidgetItem(str(itemSol)))
            # result.setItem(i, 2, QTableWidgetItem(str(itemSol[2])))

        a_window.table_widget.tab2.StatsTable.setItem(0, 0, QTableWidgetItem(str(solution_nbr)))
        # a_window.table_widget.tab2.StatsTable.setItem(1, 0, QTableWidgetItem(str(solution[3])))
        a_window.table_widget.tab2.StatsTable.setItem(1, 0, QTableWidgetItem(str(solution[2] * 1000) + "ms"))

    def showResultGreedy2(self):

        items = []
        for row in range(self.rowCount()):
            weight = int(self.item(row, 0).text())
            items.append(weight)
        # print(items)
        capacity = int(a_window.capacity_text.text())
        start = time.time()
        solution = heuristic_BF(items, capacity)
        solution_items = solution[1]
        solution_nbr = solution[0]
        # print("solution "+ str(solution_items))

        end = time.time()
        result = a_window.table_widget.tab2.result_table2
        result.setRowCount(0)
        for i, itemSol in enumerate(solution_items):
            row = result.rowCount()
            result.insertRow(row)
            result.setItem(i, 0, QTableWidgetItem(str(items[i])))
            result.setItem(i, 1, QTableWidgetItem(str(itemSol)))
            # result.setItem(i, 2, QTableWidgetItem(str(solution_nbr[i])))
        # print(itemSol)

        a_window.table_widget.tab2.StatsTable2.setItem(0, 0, QTableWidgetItem(str(solution_nbr)))
        #a_window.table_widget.tab2.StatsTable2.setItem(1, 0, QTableWidgetItem(str(solution[3])))
        a_window.table_widget.tab2.StatsTable2.setItem(1, 0, QTableWidgetItem(str(solution[2] * 1000) + "ms"))

    def showResultGreedy3(self):
        items = []
        for row in range(self.rowCount()):
            weight = int(self.item(row, 0).text())
            items.append(weight)
        capacity = int(a_window.capacity_text.text())
        start = time.time()
        solution = heuristic_NF(items, capacity)
        solution_items = solution[1]
        solution_nbr = solution[0]
        end = time.time()
        result = a_window.table_widget.tab2.result_table3
        result.setRowCount(0)
        for i, itemSol in enumerate(solution_items):
            row = result.rowCount()
            result.insertRow(row)
            result.setItem(i, 0, QTableWidgetItem(str(items[i])))
            result.setItem(i, 1, QTableWidgetItem(str(itemSol)))

        a_window.table_widget.tab2.StatsTable3.setItem(0, 0, QTableWidgetItem(str(solution_nbr)))
        #a_window.table_widget.tab2.StatsTable3.setItem(1, 0, QTableWidgetItem(str(solution[3])))
        a_window.table_widget.tab2.StatsTable3.setItem(1, 0, QTableWidgetItem(str(solution[2] * 1000) + "ms"))

    def showResultRS(self):
        items = []
        for row in range(self.rowCount()):
            weight = int(self.item(row, 0).text())
            items.append(weight)
        capacity = int(a_window.capacity_text.text())
        start = time.time()


        # solution_init = heuristic_FFD(items, capacity)
        coolingFactor  = float(a_window.table_widget.tab3.param31_text.text())
        temperatureInit = float(a_window.table_widget.tab3.param32_text.text())
        endingTemperature = float(a_window.table_widget.tab3.param33_text.text())
        iteration = float(a_window.table_widget.tab3.param34_text.text())
        # #solution = recuit_simule(items, capacity, solution_init, samplingSize,
        #                                                    temperatureInit, coolingFactor, endingTemperature)
        
        
        # alpha = 0.94
        # t = 100
        # it_palier = 10
        # k_arret = 10
        # solution = RS(items,capacity,alpha,t,it_palier,k_arret)

        _,solution,_ = heuristic_FFD( items,capacity  )
        #solution = recuit_simule(items,capacity,solution , 0.95 , 10 , 0.1 , 50 )
        solution = recuit_simule(items,capacity,solution , coolingFactor , temperatureInit, endingTemperature ,iteration )


        solution_items = solution[1]
        solution_nbr = solution[0]
        end = time.time()
        result = a_window.table_widget.tab3.result_table2
        result.setRowCount(0)
        for i, itemSol in enumerate(solution_items):
            row = result.rowCount()
            result.insertRow(row)
            result.setItem(i, 0, QTableWidgetItem(str(items[i])))
            result.setItem(i, 1, QTableWidgetItem(str(itemSol)))
            #result.setItem(i, 2, QTableWidgetItem(str(solution_nbr[i])))

        a_window.table_widget.tab3.StatsTable2.setItem(0, 0, QTableWidgetItem(str(solution_nbr)))
        #a_window.table_widget.tab3.StatsTable2.setItem(1, 0, QTableWidgetItem(str(solution[4])))
        a_window.table_widget.tab3.StatsTable2.setItem(1, 0, QTableWidgetItem(str(solution[2]) + "s"))

    def showResultTS(self):
        items = []
        for row in range(self.rowCount()):
            weight = int(self.item(row, 0).text())
            items.append(weight)
        capacity = int(a_window.capacity_text.text())
        start = time.time()
        # solution_init = totalvalue(items, capacity)[4]
        
        

        max_comb_len =float(a_window.table_widget.tab3.param41_text.text())
        max_iter = float(a_window.table_widget.tab3.param42_text.text())
        # coolingFactor = float(a_window.table_widget.tab3.param43_text.text())
        # endingTemperature = int(a_window.table_widget.tab3.param44_text.text())
        # solution = SimulatedAnnealing.simulatedAnnealing(items, capacity, solution_init, samplingSize,
        #                                                    temperatureInit, coolingFactor, endingTemperature)
        
        m,soluce,_ = heuristic_FFD(items,capacity)
        print(m,soluce)
        # k_arret = 100
        # L=100
        solution = TS(capacity,items,max_comb_len,max_iter,meta['MAX_NO_CHANGE_TS'])
        solution_items = solution[1]
        solution_nbr = solution[0]
        print(solution)
        end = time.time()
        result = a_window.table_widget.tab3.result_table1
        result.setRowCount(0)
        for i, itemSol in enumerate(solution_items):
            row = result.rowCount()
            result.insertRow(row)
            result.setItem(i, 0, QTableWidgetItem(str(itemSol[0])))
            result.setItem(i, 1, QTableWidgetItem(str(itemSol[1])))
            #result.setItem(i, 2, QTableWidgetItem(str(solution_nbr[i])))


        a_window.table_widget.tab3.StatsTable1.setItem(0, 0, QTableWidgetItem(str(solution_nbr)))
        #a_window.table_widget.tab3.StatsTable1.setItem(1, 0, QTableWidgetItem(str(solution[4])))
        a_window.table_widget.tab3.StatsTable1.setItem(1, 0, QTableWidgetItem(str(solution[2]) + "s"))

    def showResultAG(self):
        items = []
        for row in range(self.rowCount()):
            weight = int(self.item(row, 0).text())
            items.append(weight)
        capacity = int(a_window.capacity_text.text())
        start = time.time()

        population_size = float(a_window.table_widget.tab3.param11_text.text())
        max_generation = float(a_window.table_widget.tab3.param12_text.text())
        mutation_rate = float(a_window.table_widget.tab3.param13_text.text())
        crossover = float(a_window.table_widget.tab3.param14_text.text())
        
        solution = AG(items, capacity,population_size,max_generation,meta['MAX_NO_CHANGE_AG'],meta['TOURNAMENT_SIZE'],5,mutation_rate,crossover)

        solution_items = solution[1]
        solution_nbr = solution[0]
        end = time.time()
        result = a_window.table_widget.tab3.result_table3
        result.setRowCount(0)
        for i, itemSol in enumerate(solution_items):
            row = result.rowCount()
            result.insertRow(row)
            result.setItem(i, 0, QTableWidgetItem(str(itemSol[0])))
            result.setItem(i, 1, QTableWidgetItem(str(itemSol[1])))
            #result.setItem(i, 2, QTableWidgetItem(str(solution_nbr[i])))

            # print(itemSol)

        a_window.table_widget.tab3.StatsTable3.setItem(0, 0, QTableWidgetItem(str(solution_nbr)))
        #a_window.table_widget.tab3.StatsTable3.setItem(1, 0, QTableWidgetItem(str(solution[3])))
        a_window.table_widget.tab3.StatsTable3.setItem(1, 0, QTableWidgetItem(str((end - start)) + "s"))

    # def showResultAG_A(self):
    #     items = []
    #     weights = []
    #     profits = []
    #     for row in range(self.rowCount()):
    #         weight = int(self.item(row, 0).text())
    #         value = int(self.item(row, 1).text())
    #         items.append([weight, value])
    #         weights.append(weight)
    #         profits.append(value)
    #     capacity = int(a_window.capacity_text.text())
    #     start = time.time()
    #     nbr_iter = int(a_window.table_widget.tab3.param21_text.text())
    #     taille_pop = int(a_window.table_widget.tab3.param22_text.text())
    #     Adaptive_Genetic.Weight = weights
    #     Adaptive_Genetic.C = capacity
    #     Adaptive_Genetic.Profits = profits
    #     Adaptive_Genetic.runSetting = nbr_iter
    #     Adaptive_Genetic.populationSize = taille_pop
    #     solution = Adaptive_Genetic.geneticAlgorithm()
    #     end = time.time()
    #     a_window.table_widget.tab3.StatsTable4.setItem(0, 0, QTableWidgetItem(str(solution)))
    #     # a_window.table_widget.tab3.StatsTable3.setItem(1, 0, QTableWidgetItem(str(solution[3])))
    #     a_window.table_widget.tab3.StatsTable4.setItem(2, 0, QTableWidgetItem(str((end - start)) + "s"))


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


# class ResultTable(QTableWidget):
#     """docstring for MyTable"""

#     def __init__(self, parent=None):
#         super(ResultTable, self).__init__(1, 2, parent)
#         headertitle = ("Poids", "Bin")
#         self.setHorizontalHeaderLabels(headertitle)
#         self.verticalHeader().hide()
#         self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

class ResultTable(QTableWidget):
    """docstring for MyTable"""

    def __init__(self, parent=None):
        super(ResultTable, self).__init__(1, 2, parent)
        headertitle = ("Poids", "Bin")
        self.setHorizontalHeaderLabels(headertitle)
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


class StatsTable(QTableWidget):
    """docstring for MyTable"""

    def __init__(self, parent=None):
        super(StatsTable, self).__init__(2, 1, parent)
        headertitle = ("Bins", "Temps")
        self.setVerticalHeaderLabels(headertitle)
        self.horizontalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)
        self.tab2 = HeuresTab()
        self.tabs.addTab(self.tab2, "heuristiques")
        self.tab3 = Metaheur()
        self.tabs.addTab(self.tab3, "Méta heuristiques")
        self.tab1 = ExactTab()
        self.tabs.addTab(self.tab1, "Méthodes exactes")

        
        self.tab4 = GraphsTab()
        

        self.tabs.addTab(self.tab4, "Graphs")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @QtCore.pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


class GraphsTab(QWidget):
    def __init__(self, parent=None):
        super(GraphsTab, self).__init__(parent)
        
        
        
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(1)
        content = QWidget()
        self.scroll.setWidget(content)

        h_box = QVBoxLayout(content)
        v_box = QVBoxLayout()

        self.Gb_label = QLabel("Visualisation des différences \nen nombre de bins: \n")
        self.Gb_label.setStyleSheet("font-family: seorge; font: bold 20px")
        #self.show_result_btn = QPushButton("Actualiser le graph")
        v_box.addWidget(self.Gb_label,1)
        #v_box.addWidget(self.show_result_btn,1)
        sc_bins = MplCanvas(self, width=10, height=5, dpi=100)
        sc_bins.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        toolbar_bins = NavigationToolbar(sc_bins, self)
        v_box.addWidget(toolbar_bins,1)
        v_box.addWidget(sc_bins,8)

        
        # v_box2 = QVBoxLayout()
        # self.Gb_label = QLabel("Visualisation des différences \nen nombre de bins: ")
        # self.Gb_label.setStyleSheet("font-family: seorge; font: bold 20px")
        # #self.show_result_btn = QPushButton("Actualiser le graph")
        # v_box2.addWidget(self.Gb_label,1)
        # #v_box.addWidget(self.show_result_btn,1)
        # sc_bins = MplCanvas(self, width=10, height=5, dpi=100)
        # sc_bins.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        # toolbar_bins = NavigationToolbar(sc_bins, self)
        # v_box2.addWidget(toolbar_bins,1)
        # v_box2.addWidget(sc_bins,8)


        # v_box3 = QVBoxLayout()
        # self.Gb_label = QLabel("Visualisation des différences \nen nombre de bins: ")
        # self.Gb_label.setStyleSheet("font-family: seorge; font: bold 20px")
        # #self.show_result_btn = QPushButton("Actualiser le graph")
        # v_box3.addWidget(self.Gb_label,1)
        # #v_box.addWidget(self.show_result_btn,1)
        # sc_bins = MplCanvas(self, width=10, height=1000, dpi=100)
        # sc_bins.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        # toolbar_bins = NavigationToolbar(sc_bins, self)
        # v_box3.addWidget(toolbar_bins,1)
        # v_box3.addWidget(sc_bins,8)
        

        h_box.addLayout(v_box, 10)
        # h_box.addLayout(v_box2, 10)
        # h_box.addLayout(v_box3, 10)

        # qw = QWidget(h_box)
        # scrollArea = QScrollArea()
        # scrollArea.setWidget(qw)


        self.setLayout(h_box)


class ExactTab(QWidget):
    def __init__(self, parent=None):
        super(ExactTab, self).__init__(parent)
        h_box = QHBoxLayout()

        # result section
        self.show_result_btn = QPushButton("Afficher la solution")
        # self.show_result_btn.

        # result table
        self.result_table = ResultTable()
        self.StatsTable = StatsTable()
        self.DP_label = QLabel("La programmation dynamique: ")
        self.DP_label.setStyleSheet("font-family: seorge; font: bold 20px")
        # Vbox2
        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.DP_label)
        v_box2.addWidget(self.show_result_btn)
        v_box2.addWidget(self.StatsTable, 1)
        v_box2.addWidget(self.result_table, 5)

        self.result_table2 = ResultTable()
        self.StatsTable2 = StatsTable()
        self.BB_label = QLabel("Branch and Bound ")
        self.BB_label.setStyleSheet("font-family: seorge; font: bold 20px")
        self.show_result_btn2 = QPushButton("Afficher la solution")
        # VBox3
        v_box3 = QVBoxLayout()
        v_box3.addWidget(self.BB_label)
        v_box3.addWidget(self.show_result_btn2)
        v_box3.addWidget(self.StatsTable2, 1)
        v_box3.addWidget(self.result_table2, 5)
        h_box.addLayout(v_box2, 1)
        h_box.addLayout(v_box3, 1)
        self.setLayout(h_box)


class HeuresTab(QWidget):
    def __init__(self, parent=None):
        super(HeuresTab, self).__init__(parent)
        h_box = QHBoxLayout()

        # result section
        self.show_result_btn = QPushButton("Afficher la solution")
        # self.show_result_btn.

        # result table
        self.result_table = ResultTable()
        self.StatsTable = StatsTable()
        self.DP_label = QLabel("First Fit Dicreasing : ")
        self.DP_label.setStyleSheet("font-family: seorge; font: bold 20px")
        # Vbox2
        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.DP_label)
        v_box2.addWidget(self.show_result_btn)
        v_box2.addWidget(self.StatsTable, 1)
        v_box2.addWidget(self.result_table, 4)

        self.result_table2 = ResultTable()
        self.StatsTable2 = StatsTable()
        self.BB_label = QLabel("Best Fit : ")
        self.BB_label.setStyleSheet("font-family: seorge; font: bold 20px")
        self.show_result_btn2 = QPushButton("Afficher la solution")
        # VBox3
        v_box3 = QVBoxLayout()
        v_box3.addWidget(self.BB_label)
        v_box3.addWidget(self.show_result_btn2)
        v_box3.addWidget(self.StatsTable2, 1)
        v_box3.addWidget(self.result_table2, 4)

        self.result_table3 = ResultTable()
        self.StatsTable3 = StatsTable()
        self.greedy3_label = QLabel("Next Fit :")
        self.greedy3_label.setStyleSheet("font-family: seorge; font: bold 20px")
        self.show_result_btn3 = QPushButton("Afficher la solution")
        v_box4 = QVBoxLayout()
        v_box4.addWidget(self.greedy3_label)
        v_box4.addWidget(self.show_result_btn3)
        v_box4.addWidget(self.StatsTable3, 1)
        v_box4.addWidget(self.result_table3, 4)

        best_label = QLabel("Meilleure heuristique:  ")

        self.best_text = QLineEdit()
        best_box = QHBoxLayout()
        best_box.addWidget(best_label)
        best_box.addWidget(self.best_text)
        h_box.addLayout(v_box2, 1)
        h_box.addLayout(v_box3, 1)
        h_box.addLayout(v_box4, 1)
        v_box = QVBoxLayout()
        v_box.addLayout(best_box)
        v_box.addLayout(h_box)
        self.setLayout(v_box)


class Metaheur(QWidget):
    def __init__(self, parent=None):
        super(Metaheur, self).__init__(parent)
        h_box = QHBoxLayout()

        self.load_params_btn2 = QPushButton("Meilleurs paramètres")
        self.load_params_btn2.clicked.connect(self.loadParamsRS)
        # result section
        self.show_result_btn2 = QPushButton("Afficher la solution")
        # self.show_result_btn.

        # result table
        self.result_table2 = ResultTable()
        self.StatsTable2 = StatsTable()
        self.DP_label = QLabel("Recuit simulé:")
        self.DP_label.setStyleSheet("font-family: seorge; font: bold 20px")
        self.param31_label = QLabel("Facteur de refroidissement ")
        self.param31_text = QLineEdit()
        self.param31_box = QHBoxLayout()
        self.param31_box.addWidget(self.param31_label, 1)
        self.param31_box.addWidget(self.param31_text, 1)
        self.param32_label = QLabel("Température initiale  ")
        self.param32_text = QLineEdit()
        self.param32_box = QHBoxLayout()
        self.param32_box.addWidget(self.param32_label, 1)
        self.param32_box.addWidget(self.param32_text, 1)
        self.param33_label = QLabel("Température finale ")
        self.param33_text = QLineEdit()
        self.param33_box = QHBoxLayout()
        self.param33_box.addWidget(self.param33_label, 1)
        self.param33_box.addWidget(self.param33_text, 1)
        self.param34_label = QLabel("ITERATIONS")
        self.param34_text = QLineEdit()
        self.param34_box = QHBoxLayout()
        self.param34_box.addWidget(self.param34_label, 1)
        self.param34_box.addWidget(self.param34_text, 1)
        # Vbox2
        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.DP_label)
        v_box2.addLayout(self.param31_box)
        v_box2.addLayout(self.param32_box)
        v_box2.addLayout(self.param33_box)
        v_box2.addLayout(self.param34_box)
        v_box2.addWidget(self.load_params_btn2)
        v_box2.addWidget(self.show_result_btn2)
        v_box2.addWidget(self.StatsTable2, 1)
        v_box2.addWidget(self.result_table2, 4)

        self.result_table1 = ResultTable()
        self.StatsTable1 = StatsTable()

        self.DP_label2 = QLabel("Recherche Tabou: ")
        self.DP_label2.setStyleSheet("font-family: seorge; font: bold 20px")
        self.param41_label = QLabel("Taille de la liste tabou")
        self.param41_text = QLineEdit()
        self.param41_box = QHBoxLayout()
        self.param41_box.addWidget(self.param41_label, 1)
        self.param41_box.addWidget(self.param41_text, 1)
        self.param42_label = QLabel("ITERATIONS")
        self.param42_text = QLineEdit()
        self.param42_box = QHBoxLayout()
        self.param42_box.addWidget(self.param42_label, 1)
        self.param42_box.addWidget(self.param42_text, 1)
        self.show_result_btn1 = QPushButton("Afficher la solution")
        self.load_params_btn1 = QPushButton("Meilleurs paramètres")
        self.load_params_btn1.clicked.connect(self.loadParamsTS)

        # Vbox1
        v_box1 = QVBoxLayout()
        v_box1.addWidget(self.DP_label2)
        v_box1.addLayout(self.param41_box)
        v_box1.addLayout(self.param42_box)
        v_box1.addWidget(self.load_params_btn1)
        v_box1.addWidget(self.show_result_btn1)
        v_box1.addWidget(self.StatsTable1, 1)
        v_box1.addWidget(self.result_table1, 4)

        self.result_table3 = ResultTable()
        self.StatsTable3 = StatsTable()

        self.BB_label = QLabel("Algorithme génétique:")
        self.BB_label.setStyleSheet("font-family: seorge; font: bold 20px")
        self.param11_label = QLabel("Nombre de tours  ")
        self.param11_text = QLineEdit()
        self.param11_box = QHBoxLayout()
        self.param11_box.addWidget(self.param11_label)
        self.param11_box.addWidget(self.param11_text)
        self.param12_label = QLabel("Nombre de solutions  ")
        self.param12_text = QLineEdit()
        self.param12_box = QHBoxLayout()
        self.param12_box.addWidget(self.param12_label)
        self.param12_box.addWidget(self.param12_text)
        self.param13_label = QLabel("Taille de tournoi ")
        self.param13_text = QLineEdit()
        self.param13_box = QHBoxLayout()
        self.param13_box.addWidget(self.param13_label)
        self.param13_box.addWidget(self.param13_text)
        self.param14_label = QLabel("Proba de mutation ")
        self.param14_text = QLineEdit()
        self.param14_box = QHBoxLayout()
        self.param14_box.addWidget(self.param14_label)
        self.param14_box.addWidget(self.param14_text)
        self.show_result_btn3 = QPushButton("Afficher la solution")
        self.load_params_btn3 = QPushButton("Meilleurs paramètres")
        self.load_params_btn3.clicked.connect(self.loadParamsAG)

        v_box3 = QVBoxLayout()
        v_box3.addWidget(self.BB_label)
        v_box3.addLayout(self.param11_box)
        v_box3.addLayout(self.param12_box)
        v_box3.addLayout(self.param13_box)
        v_box3.addLayout(self.param14_box)
        v_box3.addWidget(self.load_params_btn3)
        v_box3.addWidget(self.show_result_btn3)
        v_box3.addWidget(self.StatsTable3, 1)
        v_box3.addWidget(self.result_table3, 4)

        self.result_table4 = ResultTable()
        self.StatsTable4 = StatsTable()
        self.greedy3_label = QLabel("Algorithme génétique \nadaptatif")
        self.greedy3_label.setStyleSheet("font-family: seorge; font: bold 20px")
        self.param21_label = QLabel("Nombre d'itérations ")
        self.param21_text = QLineEdit()
        self.param21_box = QHBoxLayout()
        self.param21_box.addWidget(self.param21_label)
        self.param21_box.addWidget(self.param21_text)
        self.param22_label = QLabel("Taille de la population ")
        self.param22_text = QLineEdit()
        self.param22_box = QHBoxLayout()
        self.param22_box.addWidget(self.param22_label)
        self.param22_box.addWidget(self.param22_text)

        self.show_result_btn4 = QPushButton("Afficher la solution")
        self.load_params_btn4 = QPushButton("Meilleurs paramètres")
        best_label = QLabel("Meilleure méta heuristique:  ")
        best_ag_label = QLabel("Meilleur Algorithme génétique")
        self.best_ag_text = QLineEdit()
        best_rs_lable = QLabel("Meilleur récuit simulé")
        self.best_rs_text = QLineEdit()
        self.best_text = QLineEdit()
        best_box = QHBoxLayout()
        best_box.addWidget(best_label)
        best_box.addWidget(self.best_text)
        h_box.addLayout(v_box1, 1)
        h_box.addLayout(v_box2, 1)
        h_box.addLayout(v_box3, 1)
        #h_box.addLayout(v_box4, 1) #ENLEVER
        v_box = QVBoxLayout()
        v_box.addLayout(best_box)
        # v_box.addLayout(best_ag_box)
        # v_box.addLayout(best_rs_box)
        v_box.addLayout(h_box)
        self.setLayout(v_box)

    def loadParamsAG(self):
        '''options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:'''
        # famille = a_window.famille_text.text()
        # taille = a_window.diff_text.text()
        #params = getParams.getBestParamsAG(famille, taille)
        
        #params = meta[6:12]
        if len(meta)!=13:
            params = get_params_AG(fileName)
        else : params = meta
        
        self.param11_text.setText(str(params['POPULATION_SIZE']))
        self.param12_text.setText(str(params['MAX_GENERATIONS']))
        self.param13_text.setText(str(params['MUTATION_RATE']))
        self.param14_text.setText(str(params['CROSSOVER_RATE']))

    def loadParamsRS(self):
        '''options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:'''
        # famille = a_window.famille_text.text()
        # taille = a_window.diff_text.text()
        
        #params = getParams.getBestParamsRS(famille, taille)
        if len(meta)!=13:
            params = get_params_SA(fileName)
        else : params = meta
        
        self.param31_text.setText(str(params['ALPHA']))
        self.param32_text.setText(str(params['TEMPERATURE']))
        self.param33_text.setText(str(params['T_CIBLE']))
        self.param34_text.setText(str(params['ITERATIONS']))

    def loadParamsTS(self):
        '''options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)

        if fileName:'''
        # famille = a_window.famille_text.text()
        # taille = a_window.diff_text.text()
        # params = getParams.getBestParamsRG(famille, taille)
        if len(meta)!=13:
            params = get_params_TS(fileName)
            
        else : params = meta
        
        self.param41_text.setText(str(params['MAX_COMBINATION_LENGTH']))
        self.param42_text.setText(str(params['MAX_ITERATIONS']))

        """
        params = meta[12:]
        print(params)
        self.param41_text.setText(str(params[0]))
        self.param42_text.setText(str(params[1]))
        """
      
        #  self.param43_text.setText(str(params[2]))
        # self.param44_text.setText(str(params[3]))

    # def loadParamsAGA(self):
    #     '''options = QFileDialog.Options()
    #     options |= QFileDialog.DontUseNativeDialog
    #     fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
    #                                               "All Files (*);;Python Files (*.py)", options=options)
    #     if fileName:'''
    #     famille = a_window.famille_text.text()
    #     taille = a_window.diff_text.text()
    #     params = getParams.getBestParamsAGA(famille, taille)
    #     self.param21_text.setText(str(params[0]))
    #     self.param22_text.setText(str(params[1]))


class window(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Capacity field
        self.capacity_label = QLabel("Capacité: ")
        self.capacity_text = QLineEdit()
        self.nbr_label = QLabel("Nombre d'objets: ")
        self.nbr_text = QLineEdit()
        self.famille_label = QLabel("Famille: ")
        self.famille_text = QLineEdit()
        self.diff_label = QLabel("Taille: ")
        self.diff_text = QLineEdit()
        self.nbr_text.setText('0')
        # self.nbr_text.setDisabled(True)
        capacity_hbox = QHBoxLayout()
        capacity_hbox.addWidget(self.capacity_label)
        capacity_hbox.addWidget(self.capacity_text)
        nbr_hbox = QHBoxLayout()
        nbr_hbox.addWidget(self.nbr_label)
        nbr_hbox.addWidget(self.nbr_text)
        self.famille_hbox = QHBoxLayout()
        self.famille_hbox.addWidget(self.famille_label)
        self.famille_hbox.addWidget(self.famille_text)
        self.diff_hbox = QHBoxLayout()
        self.diff_hbox.addWidget(self.diff_label)
        self.diff_hbox.addWidget(self.diff_text)
        # objects table
        self.objects_table = MyTable()
        table_hbox = QHBoxLayout()
        table_hbox.addWidget(self.objects_table)
        # Vbox1
        self.add_btn = QPushButton("Ajouter un objet")
        self.add_btn.clicked.connect(self.objects_table._addrow)

        self.loadData = QPushButton("Télécharger une instance")
        self.loadData.clicked.connect(self.objects_table.loadInstance)
        v_box1 = QVBoxLayout()
        v_box1.addLayout(capacity_hbox)
        v_box1.addLayout(nbr_hbox)
        v_box1.addLayout(self.famille_hbox)
        v_box1.addLayout(self.diff_hbox)
        v_box1.addWidget(self.add_btn)
        v_box1.addWidget(self.loadData)
        v_box1.addLayout(table_hbox)
        v_box4 = QVBoxLayout()
        self.table_widget = MyTableWidget(self)
        self.best_method_label = QLabel("Meilleure Méthode: ")
        self.best_method_text = QLineEdit()
        H_box = QHBoxLayout()
        H_box.addWidget(self.best_method_label)
        H_box.addWidget(self.best_method_text)
        v_box4.addLayout(H_box)
        v_box4.addWidget(self.table_widget)
        #self.table_widget.tab1.show_result_btn.clicked.connect(self.objects_table.showResult)
        self.table_widget.tab1.show_result_btn2.clicked.connect(self.objects_table.showResult2)
        self.table_widget.tab2.show_result_btn.clicked.connect(self.objects_table.showResultGreedy1)
        self.table_widget.tab2.show_result_btn2.clicked.connect(self.objects_table.showResultGreedy2)
        self.table_widget.tab2.show_result_btn3.clicked.connect(self.objects_table.showResultGreedy3)
        self.table_widget.tab3.show_result_btn2.clicked.connect(self.objects_table.showResultRS)
        self.table_widget.tab3.show_result_btn1.clicked.connect(self.objects_table.showResultTS)
        self.table_widget.tab3.show_result_btn3.clicked.connect(self.objects_table.showResultAG)
        #self.table_widget.tab3.show_result_btn4.clicked.connect(self.objects_table.showResultAG_A)

        # main layout
        h_box = QHBoxLayout()
        h_box.addLayout(v_box1, 1)
        h_box.addLayout(v_box4, 5)

        self.setLayout(h_box)
        self.setGeometry(0, 0, 1800, 700)
        self.setWindowTitle("Bin Packing")
        self.show()


WEIGHT, VALUE = range(2)
items = []
capacity = 0
app = QApplication(sys.argv)
app.setStyle('Fusion')
palette = QtGui.QPalette()
palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
app.setPalette(palette)
app.setFont(QtGui.QFont("Seorge"))
a_window = window()
sys.exit(app.exec_())