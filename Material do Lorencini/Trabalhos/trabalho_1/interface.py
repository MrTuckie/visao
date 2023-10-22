import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from numpy import array
from read_stl import read_mesh
from transformations import *
from pprint import pprint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # definindo as variaveis
        self.set_variables()
        # Ajustando a tela
        self.setWindowTitle("Grid Layout")
        self.setGeometry(100, 100, 1280, 720)
        self.setup_ui()

    def set_variables(self):
        """Função que define as variáveis. Ela é chamada no __init__(self).\n
        Acredito que não precise de modificações, por enquanto.
        """
        # TODO: Alterar as variáveis
        self.objeto_original = read_mesh()
        self.objeto = self.objeto_original
        self.cam_original = initial_setup()[-1]
        self.cam = np.dot(translation(0,-50,25),np.dot(x_rotation(-90),self.cam_original))
        self.px_base = 1280  # modificar
        self.px_altura = 720  # modificar
        self.dist_foc = 10  # modificar
        self.stheta = 0  # modificar
        self.ox = self.px_base/2  # modificar
        self.oy = self.px_altura/2  # modificar
        self.ccd = [36, 24]  # modificar
        self.projection_matrix = np.eye(3, 4)

    def setup_ui(self):
        """Função que cria a interface do usuário através dos grids
        e dos widgets. Ela é chamada no __init__() também.\n
        Não parece ser uma função que precise de alteração"""
        # Criar o layout de grade
        grid_layout = QGridLayout()

        # Criar os widgets
        line_edit_widget1 = self.create_world_widget("Ref mundo")
        line_edit_widget2 = self.create_cam_widget("Ref camera")
        line_edit_widget3 = self.create_intrinsic_widget("params instr")

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
        # Define um tamanho fixo para o botão (largura: 50 pixels, altura: 30 pixels)
        reset_button.setFixedSize(50, 30)
        style_sheet = """
            QPushButton {
                color : red ;
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

    def create_intrinsic_widget(self, title: str) -> QGroupBox:
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
        labels = ['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:',
                  'dist_focal:', 'sθ:']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            # Aplicar o validador ao QLineEdit
            line_edit.setValidator(validator)
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1) % 2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1) % 2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        # Você deverá criar, no espaço reservado ao final, a função self.update_params_intrinsc ou outra que você queira
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(
            lambda: self.update_params_intrinsc(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_world_widget(self, title: str) -> QGroupBox:
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
        # Texto a ser exibido antes de cada QLineEdit
        labels = ['X(move):', 'X(angle):', 'Y(move):',
                  'Y(angle):', 'Z(move):', 'Z(angle):']

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            # Aplicar o validador ao QLineEdit
            line_edit.setValidator(validator)
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1) % 2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1) % 2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar Mundo")

        # Você deverá criar, no espaço reservado ao final, a função self.update_world ou outra que você queira
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_world(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_cam_widget(self, title: str) -> QGroupBox:
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
        # Texto a ser exibido antes de cada QLineEdit
        labels = ['X(move):', 'X(angle):', 'Y(move):',
                  'Y(angle):', 'Z(move):', 'Z(angle):']

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        # Olha essa maracutaia:
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            # Aplicar o validador ao QLineEdit
            line_edit.setValidator(validator)
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1) % 2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1) % 2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar Câmera")

        # Você deverá criar, no espaço reservado ao final, a função self.update_cam ou outra que você queira
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
        # Criar um objeto FigureCanvas para exibir o gráfico 2D
        self.fig_2d, self.ax_2d = plt.subplots()
        self.ax_2d.set_title("Imagem")
        self.canvas_2d = FigureCanvas(self.fig_2d)

        # Acerte os limites do eixo X
        self.ax_2d.set_xlim([0, self.px_base])

        # Acerte os limites do eixo Y
        self.ax_2d.set_ylim([self.px_altura, 0])

        object_2d = self.projection_2d()

        self.ax_2d.plot(object_2d[0, :], object_2d[1, :])
        self.ax_2d.grid('True')
        self.ax_2d.set_aspect('equal')
        canvas_layout.addWidget(self.canvas_2d)

        # Criar um objeto FigureCanvas para exibir o gráfico 3D
        self.fig_3d = plt.figure()
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')
        self.ax_3d = set_plot(ax=self.ax_3d)
        self.ax_3d.set_title("visão do mundo")
        x_lim_max = np.concatenate((self.objeto[0, :],self.cam[0,:])).max()
        y_lim_max = np.concatenate((self.objeto[1, :],self.cam[1,:])).max()
        z_lim_max = np.concatenate((self.objeto[2, :],self.cam[2,:])).max()

        x_lim_min = np.concatenate((self.objeto[0, :],self.cam[0,:])).min()
        y_lim_min = np.concatenate((self.objeto[1, :],self.cam[1,:])).min()
        z_lim_min = np.concatenate((self.objeto[2, :],self.cam[2,:])).min()

        self.ax_3d.set_xlim3d(x_lim_min, x_lim_max)
        self.ax_3d.set_ylim3d(y_lim_min, y_lim_max)
        self.ax_3d.set_zlim3d(z_lim_min, z_lim_max)

        self.ax_3d.plot3D(
            self.objeto[0, :], self.objeto[1, :], self.objeto[2, :], 'red')
        draw_arrows(self.cam[:, -1], self.cam[:, 0:3], self.ax_3d)
        self.canvas_3d = FigureCanvas(self.fig_3d)
        canvas_layout.addWidget(self.canvas_3d)

        # Retornar o widget de canvas
        return canvas_widget

    # Você deverá criar as suas funções aqui

    def update_params_intrinsc(self, line_edits):
        # Confesso que isso é uma maracutaia muito feia.
        # Resumindo, se eu não recebo nada da interface, então o valor é o antigo ainda
        old_values = [self.px_base, self.px_altura,
                      self.dist_foc, self.stheta, self.ccd[0], self.ccd[1]]
        new_values = [float(line.text()) if line.text() else old_values[i]
                      for i, line in enumerate(line_edits)]
        self.px_base, self.px_altura, self.dist_foc, self.stheta, self.ccd[
            0], self.ccd[1] = new_values
        self.ox, self.oy = self.px_base/2, self.px_altura/2
        self.update_canvas()


    def update_world(self, line_edits):
        # 'X(move):', 'X(angle):', 'Y(move):',
        # 'Y(angle):', 'Z(move):', 'Z(angle):'

        new_values = [float(line.text()) if line.text() else 0
                      for line in line_edits]
        T = translation(new_values[0],new_values[2],new_values[4])
        rot_list = (x_rotation(new_values[1]),y_rotation(new_values[3]),z_rotation(new_values[5]))
        for rot in rot_list:
            self.cam = np.dot(rot,self.cam)
        self.cam = np.dot(T,self.cam)
        self.update_canvas()

    def update_cam(self, line_edits):
        # X_move, X_angle, Y_move, Y_angle, Z_move, Z_angle
        new_values = [float(line.text()) if line.text() else 0
                      for line in line_edits]
        T = translation(new_values[0],new_values[2],new_values[4])
        self.cam = np.dot(self.cam,np.dot(T,self.cam_original))

        rot_list = (x_rotation(new_values[1]),y_rotation(new_values[3]),z_rotation(new_values[5]))
        for rot in rot_list:
            self.cam = np.dot(self.cam,np.dot(rot,self.cam_original))

        self.update_canvas()

    def projection_2d(self):
        matrix_G = np.linalg.inv(self.cam)
        matrix_K = self.generate_intrinsic_params_matrix()
        object_2d = np.dot(matrix_G, self.objeto)
        object_2d = np.dot(self.projection_matrix, object_2d)
        object_2d = np.dot(matrix_K, object_2d)
        object_2d[0, :] = object_2d[0, :]/object_2d[2, :]
        object_2d[1, :] = object_2d[1, :]/object_2d[2, :]
        object_2d[2, :] = object_2d[2, :]/object_2d[2, :]
        return object_2d

    def generate_intrinsic_params_matrix(self):
        ox = self.px_base/2
        oy = self.px_altura/2
        fsx = self.px_base*self.dist_foc/self.ccd[0]
        fsy = self.px_altura*self.dist_foc/self.ccd[1]
        fstheta = self.stheta*self.dist_foc
        K = array([[fsx, fstheta, ox], [0, fsy, oy], [0, 0, 1]])
        return K

    def update_canvas(self):
        plt.close('all')
        object_2d = self.projection_2d()
    
        # Atualizar o gráfico 2D
        self.ax_2d.clear()
        self.ax_2d.set_title("Imagem")
        self.ax_2d.set_xlim([0, self.px_base])
        self.ax_2d.set_ylim([self.px_altura, 0])
        self.ax_2d.plot(object_2d[0, :], object_2d[1, :])
        self.ax_2d.grid(True)
        self.ax_2d.set_aspect('equal')

        # Atualizar o gráfico 3D
        self.ax_3d.clear()
        self.ax_3d.set_title("visão do mundo")
        self.ax_3d.grid(True)
        self.ax_3d.set_xlabel("x axis")
        self.ax_3d.set_ylabel("y axis")
        self.ax_3d.set_zlabel("z axis")
        x_lim_max = np.concatenate((self.objeto[0, :],self.cam[0,:])).max()
        y_lim_max = np.concatenate((self.objeto[1, :],self.cam[1,:])).max()
        z_lim_max = np.concatenate((self.objeto[2, :],self.cam[2,:])).max()

        x_lim_min = np.concatenate((self.objeto[0, :],self.cam[0,:])).min()
        y_lim_min = np.concatenate((self.objeto[1, :],self.cam[1,:])).min()
        z_lim_min = np.concatenate((self.objeto[2, :],self.cam[2,:])).min()

        self.ax_3d.set_xlim3d(x_lim_min, x_lim_max)
        self.ax_3d.set_ylim3d(y_lim_min, y_lim_max)
        self.ax_3d.set_zlim3d(z_lim_min, z_lim_max)
        self.ax_3d.plot3D(
            self.objeto[0, :], self.objeto[1, :], self.objeto[2, :], 'red')
        draw_arrows(self.cam[:, -1], self.cam[:, 0:3], self.ax_3d)

        # Redesenhar os canvas
        self.canvas_2d.draw()
        self.canvas_3d.draw()
        self.canvas.layout().itemAt(1).widget().draw()

    def reset_canvas(self):
        self.set_variables()
        self.update_canvas()
