import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton,QGroupBox
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from numpy import array
from read_stl import read_mesh
from transformations import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #definindo as variaveis
        self.set_variables()
        #Ajustando a tela    
        self.setWindowTitle("Grid Layout")
        self.setGeometry(100, 100,1280 , 720)
        self.setup_ui()

    def set_variables(self):
        """Função que define as variáveis. Ela é chamada no __init__(self).\n
        Acredito que não precise de modificações, por enquanto.
        """
        # TODO: Alterar as variáveis
        self.objeto_original = read_mesh()
        self.objeto = self.objeto_original
        self.cam_original = [] #modificar
        self.cam = [] #modificar
        self.px_base = 1280  #modificar
        self.px_altura = 720 #modificar
        self.dist_foc = 50 #modificar
        self.stheta = 0 #modificar
        self.ox = self.px_base/2 #modificar
        self.oy = self.px_altura/2 #modificar
        self.ccd = [36,24] #modificar
        self.projection_matrix = [] #modificar
        ax_3d:Axes3D
        
    def setup_ui(self):
        """Função que cria a interface do usuário através dos grids
        e dos widgets. Ela é chamada no __init__() também.\n
        Não parece ser uma função que precise de alteração"""
        # Criar o layout de grade
        grid_layout = QGridLayout()

        # Criar os widgets
        line_edit_widget1 = self.create_world_widget("Ref mundo")
        line_edit_widget2  = self.create_cam_widget("Ref camera")
        line_edit_widget3  = self.create_intrinsic_widget("params instr")

        self.canvas = self.create_matplotlib_canvas()

        # Adicionar os widgets ao layout de grade
        grid_layout.addWidget(line_edit_widget1, 0, 0)
        grid_layout.addWidget(line_edit_widget2, 0, 1)
        grid_layout.addWidget(line_edit_widget3, 0, 2)
        grid_layout.addWidget(self.canvas, 1, 0, 1, 3)

        # Criar um widget para agrupar o botão de reset
        reset_widget = QWidget()
        reset_layout = QHBoxLayout()
        reset_widget.setLayout(reset_layout)

        # Criar o botão de reset vermelho
        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(50, 30)  # Define um tamanho fixo para o botão (largura: 50 pixels, altura: 30 pixels)
        style_sheet = """
            QPushButton {
                color : white ;
                background: rgba(255, 127, 130,128);
                font: inherit;
                border-radius: 5px;
                line-height: 1;
            }
        """
        reset_button.setStyleSheet(style_sheet)
        reset_button.clicked.connect(self.reset_canvas)

        # Adicionar o botão de reset ao layout
        reset_layout.addWidget(reset_button)

        # Adicionar o widget de reset ao layout de grade
        grid_layout.addWidget(reset_widget, 2, 0, 1, 3)

        # Criar um widget central e definir o layout de grade como seu layout
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        
        # Definir o widget central na janela principal
        self.setCentralWidget(central_widget)

    def create_intrinsic_widget(self, title:str) -> QGroupBox:
        """Função que cria os widgets referente as características intrísecas
        da câmera.\n
        Não parece ser uma função que precise ser alterada.

        Args:
            title (str): _description_

        Returns:
            QGroupBox: _description_
        """
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:', 'dist_focal:', 'sθ:']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_params_intrinsc ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_params_intrinsc(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget
    
    def create_world_widget(self, title:str) -> QGroupBox:
        """Função que cria o widget das informações do mundo.\n
        Não parece ser uma função que precise de alteração.

        Args:
            title (str): _description_

        Returns:
            QGroupBox: _description_
        """
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar Mundo")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_world ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_world(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_cam_widget(self, title:str) -> QGroupBox:
        """Função que cria o widget da câmera.\n
        Aparentemente, não é uma função que precise de alteração.
        Tem que ficar atento a função self.update_cam()

        Args:
            title (str): _description_

        Returns:
            QGroupBox: _description_
        """
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        # Olha essa maracutaia:
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar Câmera")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_cam ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_cam(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_matplotlib_canvas(self) -> QWidget:
        """Função que cria o canvas do matplolib. Tanto a parte 2D e 3D.\n
        Não parece ser uma função que precise ser alterada. Talvez apenas os
        limites do eixo x e y

        Returns:
            QWidget: _description_
        """
        # Criar um widget para exibir os gráficos do Matplotlib
        canvas_widget = QWidget()
        canvas_layout = QHBoxLayout()
        canvas_widget.setLayout(canvas_layout)

        # Criar um objeto FigureCanvas para exibir o gráfico 2D
        fig_2d, ax_2d = plt.subplots()
        ax_2d.set_title("Visão da Câmera")
        self.canvas1 = FigureCanvas(fig_2d)

        ##### TODO acertar os limites do eixo X
        
        ##### TODO acertar os limites do eixo Y
        
        ##### TODO Você deverá criar a função de projeção 
        # object_2d = self.projection_2d()
        ######################
        # World reference frame plotted at the origin


        ##### TODO plotar o object_2d que retornou da projeção
        # ax_2d = axis
        ax_2d.grid('True')
        ax_2d.set_aspect('equal')  
        canvas_layout.addWidget(self.canvas1)

        # Criar um objeto FigureCanvas para exibir o gráfico 3D


        e1,e2,e3,base,origin_point,cam = initial_setup()

        # Criando a figura 3D e o Axes3D
        fig_3d = plt.figure()
        ax_3d = fig_3d.add_subplot(111, projection='3d')
        ax_3d:Axes3D


        # Criação do objeto
        object_3d = read_mesh()
        ax_3d.plot(object_3d[0,:],object_3d[1,:],object_3d[2,:],'r')
        length = 0.5
        # # Plot vector of x-axis
        # ax_3d.quiver(origin_point[0],origin_point[1],origin_point[2],base[0,0],base[1,0],base[2,0],color='red',pivot='tail',  length=length)
        # # Plot vector of y-axis
        # ax_3d.quiver(origin_point[0],origin_point[1],origin_point[2],base[0,1],base[1,1],base[2,1],color='green',pivot='tail',  length=length)
        # # Plot vector of z-axis
        # ax_3d.quiver(origin_point[0],origin_point[1],origin_point[2],base[0,2],base[1,2],base[2,2],color='blue',pivot='tail',  length=length)
        
        # Definindo os limites 3D
        ax_3d.set_xlim3d(min(object_3d[0,:]),max(object_3d[0,:]))
        ax_3d.set_ylim3d(min(object_3d[1,:]),max(object_3d[1,:]))
        ax_3d.set_zlim3d(min(object_3d[2,:]),max(object_3d[2,:]))

        ##### TODO Falta plotar o seu objeto 3D e os referenciais da câmera e do mundo


        
        # passando a figura para o canvas_layout
        self.canvas2 = FigureCanvas(fig_3d)
        canvas_layout.addWidget(self.canvas2)

        # Retornar o widget de canvas
        return canvas_widget


    ##### Você deverá criar as suas funções aqui
    
    def update_params_intrinsc(self, line_edits):
        # TODO
        return 

    def update_world(self,line_edits):
        # TODO
        return

    def update_cam(self,line_edits):
        # TODO
        print("update_cam chamada:",line_edits)
        # line_edits é uma lista contendo objetos do tipo <PyQt5.QtWidgets.QLineEdit object at 0x7fefea741f30>
        return 
    
    def projection_2d(self):
        # TODO
        return 
    
    def generate_intrinsic_params_matrix(self):
        # TODO
        return 
    

    def update_canvas(self):
        # TODO
        return 
    
    def reset_canvas(self):
        # TODO
        return
    