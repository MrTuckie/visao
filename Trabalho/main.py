import sys
import matplotlib.pyplot as plt
import numpy as np
from math import pi,cos,sin
from stl import mesh
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton,QGroupBox
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D


###### Crie suas funções de translação, rotação, criação de referenciais, plotagem de setas e qualquer outra função que precisar

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
        self.objeto_original = self.read_stl_model_as_array();
        self.objeto = self.objeto_original
        self.cam_original = self.generate_cam();
        self.cam = self.ideal_cam_point(self.cam_original)
        self.px_base = 1280  #modificar
        self.px_altura = 720 #modificar
        self.dist_foc = 50 #modificar
        self.stheta = 0 #modificar
        self.ox = self.px_base/2 #modificar
        self.oy = self.px_altura/2 #modificar
        self.ccd = [36,24] #modificar
        self.projection_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
        
    def setup_ui(self):
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

    def create_intrinsic_widget(self, title):
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
    
    def create_world_widget(self, title):
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
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_world ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_world(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_cam_widget(self, title):
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
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_cam ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_cam(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_matplotlib_canvas(self):
        # Criar um widget para exibir os gráficos do Matplotlib
        canvas_widget = QWidget()
        canvas_layout = QHBoxLayout()
        canvas_widget.setLayout(canvas_layout)

        # Criar um objeto FigureCanvas para exibir o gráfico 2D
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_title("Imagem")
        self.canvas1 = FigureCanvas(self.fig1)

        ##### Falta acertar os limites do eixo X
        
        ##### Falta acertar os limites do eixo Y
        
        object_2d = self.projection_2d()
        self.ax1.plot(object_2d[0,:],object_2d[1,:])          
        self.ax1.grid('True')
        self.ax1.set_aspect('equal')  
        canvas_layout.addWidget(self.canvas1)

        # Criar um objeto FigureCanvas para exibir o gráfico 3D
        self.fig2 = plt.figure()
        self.ax2 = self.fig2.add_subplot(111, projection='3d')
        self.ax2 = self.set_plot(ax=self.ax2, lim=[-100, 100])
        self.ax2.plot3D(self.objeto[0,:],self.objeto[1,:],self.objeto[2,:],'r')
        self.draw_arrows(self.cam[:,-1],self.cam[:,0:3],self.ax2)
        ##### Falta plotar o seu objeto 3D e os referenciais da câmera e do mundo
        
        self.canvas2 = FigureCanvas(self.fig2)
        canvas_layout.addWidget(self.canvas2)

        # Retornar o widget de canvas
        return canvas_widget


    ##### Você deverá criar as suas funções aqui

    def update_world(self,line_edits):
        return

    def update_cam(self,line_edits):
        return 
    
    def projection_2d(self):
        canonical_projection_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
        intrinsic_matrix = self.generate_intrinsic_params_matrix;
        extrinsic_matrix = np.linalg.inv(self.cam)
        projection_matrix = intrinsic_matrix@canonical_projection_matrix@extrinsic_matrix
        objeto_projetado_homog = projection_matrix@self.objeto
        objeto_projetado_cart = objeto_projetado_homog/objeto_projetado_homog[2,:]
        return objeto_projetado_cart;
    
    def generate_intrinsic_params_matrix(self,line_edits):
        n_pixels_base = line_edits[0]
        n_pixels_altura = line_edits[1]
        largura_sensor = line_edits[2]
        altura_sensor = line_edits[3]
        f = line_edits[4]
        s_theta = line_edits[5]

        #Define os parametros com os valores passados
        sx = n_pixels_base/largura_sensor
        sy = n_pixels_altura/altura_sensor
        Ox = n_pixels_base/2
        Oy = n_pixels_altura/2

        return np.array([[f*sx, f*s_theta, Ox],
                            [0, f*sy, Oy],
                            [0, 0, 1]])

    def update_canvas(self):
        return 
    
    def reset_canvas(self):
        return
    
    @staticmethod
    def read_stl_model_as_array():
        your_mesh = mesh.Mesh.from_file('Trabalho\donkey_kong.STL')
        x = your_mesh.x.flatten()
        y = your_mesh.y.flatten()
        z = your_mesh.z.flatten()
        return np.array([x.T,y.T,z.T,np.ones(x.size)])

    @staticmethod
    def generate_cam():
        e1 = np.array([[1],[0],[0],[0]]) # X
        e2 = np.array([[0],[1],[0],[0]]) # Y
        e3 = np.array([[0],[0],[1],[0]]) # Z
        base = np.hstack((e1,e2,e3))
        point =np.array([[0],[0],[0],[1]])
        return np.hstack((base,point))

    def ideal_cam_point(self,cam):
        Rx = self.x_rotation(-90)
        T = self.move(0,-100,40)
        M = np.dot(T,Rx)
        cam = np.dot(M,cam)
        return cam

    @staticmethod
    def draw_arrows(point,base,axis,length=5):
        # Plot vector of x-axis
        axis.quiver(point[0],point[1],point[2],base[0,0],base[1,0],base[2,0],color='red',pivot='tail',  length=length)
        # Plot vector of y-axis
        axis.quiver(point[0],point[1],point[2],base[0,1],base[1,1],base[2,1],color='green',pivot='tail',  length=length)
        # Plot vector of z-axis
        axis.quiver(point[0],point[1],point[2],base[0,2],base[1,2],base[2,2],color='blue',pivot='tail',  length=length)

        return axis

    @staticmethod
    def set_plot(ax=None,figure = None,lim=[-2,2]):
        if figure ==None:
            figure = plt.figure(figsize=(50,50))
        if ax==None:
            ax = plt.axes(projection='3d')

        ax.set_title("camera referecnce")
        ax.set_xlim(lim)
        ax.set_xlabel("x axis")
        ax.set_ylim(lim)
        ax.set_ylabel("y axis")
        ax.set_zlim(lim)
        ax.set_zlabel("z axis")
        return ax

    @staticmethod
    def z_rotation(angle):
        angle = float(angle)
        angle = angle*pi/180
        rotation_matrix=np.array([[cos(angle),-sin(angle),0,0],[sin(angle),cos(angle),0,0],[0,0,1,0],[0,0,0,1]])
        return rotation_matrix
    
    @staticmethod
    def x_rotation(angle):
        angle = float(angle)
        angle = angle*pi/180
        rotation_matrix=np.array([[1,0,0,0],[0, cos(angle),-sin(angle),0],[0, sin(angle), cos(angle),0],[0,0,0,1]])
        return rotation_matrix

    @staticmethod
    def y_rotation(angle):
        angle = float(angle)
        angle = angle*pi/180
        rotation_matrix=np.array([[cos(angle),0, sin(angle),0],[0,1,0,0],[-sin(angle), 0, cos(angle),0],[0,0,0,1]])
        return rotation_matrix
    
    @staticmethod
    def move (dx,dy,dz):
        T = np.eye(4)
        T[0,-1] = dx
        T[1,-1] = dy
        T[2,-1] = dz
        return T

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())