import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton,QGroupBox
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from numpy import array
from funcoes import generate_house_origin,generate_cam_origin,draw_arrows,set_plot,move_cam_to_initial_point,generate_projection_matrix,generate_inv,np_dot,move,x_rotation,y_rotation,z_rotation

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
        self.house_original = generate_house_origin()
        self.house = self.house_original
        self.cam_original = generate_cam_origin()
        self.cam = move_cam_to_initial_point(self.cam_original)
        self.px_base = 1280 
        self.px_altura = 720
        self.dist_foc = 50
        self.stheta = 0
        self.ox = self.px_base/2
        self.oy = self.px_altura/2
        self.ccd = [36,24]
        self.projection_matrix = generate_projection_matrix()

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

        # Acerte os limites do eixo X
        self.ax1.set_xlim([0,self.px_base])

        # Acerte os limites do eixo Y
        self.ax1.set_ylim([self.px_altura,0])

        object_2d = self.projection_2d()

        self.ax1.plot(object_2d[0,:],object_2d[1,:])  
        self.ax1.grid('True')
        self.ax1.set_aspect('equal')  
        canvas_layout.addWidget(self.canvas1)

        # Criar um objeto FigureCanvas para exibir o gráfico 3D
        self.fig2 = plt.figure()
        self.ax2 = self.fig2.add_subplot(111, projection='3d')
        self.ax2 = set_plot(ax=self.ax2,lim=[-15,30])
        self.ax2.plot3D(self.house[0,:], self.house[1,:], self.house[2,:], 'red')
        draw_arrows(self.cam[:,-1],self.cam[:,0:3],self.ax2)
        self.canvas2 = FigureCanvas(self.fig2)
        canvas_layout.addWidget(self.canvas2)

        # Retornar o widget de canvas
        return canvas_widget


    def update_world(self,line_edits):
        # Criar uma lista para armazenar o texto de cada caixa de texto
        x = line_edits[0].text()
        x_ang = line_edits[1].text()
        y = line_edits[2].text()
        y_ang = line_edits[3].text()
        z = line_edits[4].text()
        z_ang = line_edits[5].text()

        dz = z if z else 0
        dx = x if x else 0
        dy = y if y else 0

        translation = move(dx,dy,dz)

        if x_ang:
            xrot = x_rotation(x_ang)
            self.cam = np_dot(xrot,self.cam)
        if y_ang:
            yrot = y_rotation(y_ang)
            self.cam = np_dot(yrot,self.cam)
        if z_ang:
            zrot = z_rotation(z_ang)
            self.cam = np_dot(zrot,self.cam)

        self.cam = np_dot(translation,self.cam)
        self.update_canvas()
        # Limpar o texto de cada caixa de texto
        for line_edit in line_edits:
            line_edit.clear()

    def update_cam(self,line_edits):
        # Criar uma lista para armazenar o texto de cada caixa de texto
        x = line_edits[0].text()
        x_ang = line_edits[1].text()
        y = line_edits[2].text()
        y_ang = line_edits[3].text()
        z = line_edits[4].text()
        z_ang = line_edits[5].text()

        dz = z if z else 0
        dx = x if x else 0
        dy = y if y else 0

        if dz or dx or dy:
            translation = move(dx,dy,dz)
            temp_cam = np_dot(translation,self.cam_original)
            self.cam = np_dot(self.cam,temp_cam)

        if x_ang:
            xrot = x_rotation(x_ang)
            temp_cam = np_dot(xrot,self.cam_original)
            self.cam = np_dot(self.cam,temp_cam)
        if y_ang:
            yrot = y_rotation(y_ang)
            temp_cam = np_dot(yrot,self.cam_original)
            self.cam = np_dot(self.cam,temp_cam)
        if z_ang:
            zrot = z_rotation(z_ang)
            temp_cam = np_dot(zrot,self.cam_original)
            self.cam = np_dot(self.cam,temp_cam)

        self.update_canvas()

        # Limpar o texto de cada caixa de texto
        for line_edit in line_edits:
            line_edit.clear()
    
    def projection_2d(self):
        matrix_G = generate_inv(self.cam)
        matrix_K = self.generate_intrinsic_params_matrix()
        object_2d = np_dot(matrix_G,self.house)
        object_2d = np_dot(self.projection_matrix,object_2d)
        object_2d = np_dot(matrix_K,object_2d)
        object_2d[0,:] = object_2d[0,:]/object_2d[2,:]
        object_2d[1,:] = object_2d[1,:]/object_2d[2,:]
        object_2d[2,:] = object_2d[2,:]/object_2d[2,:]
        return object_2d
    
    def update_params_intrinsc(self, line_edits):
        # Criar uma lista para armazenar o texto de cada caixa de texto
        px_base = line_edits[0].text()
        px_altura = line_edits[1].text()
        ccd_x = line_edits[2].text()
        ccd_y = line_edits[3].text()
        dist_focal = line_edits[4].text()
        stheta = line_edits[5].text()

        if px_base:
            self.px_base = float(px_base)
        if px_altura:
            self.px_altura = float(px_altura)
        if ccd_x:
            self.ccd[0] = float(ccd_x)
        if ccd_y:
            self.ccd[1] = float(ccd_y)
        if dist_focal:
            self.dist_foc = float(dist_focal)
        if stheta:
            self.stheta = float(stheta)

        self.update_canvas()
        # Limpar o texto de cada caixa de texto
        for line_edit in line_edits:
            line_edit.clear()


    def generate_intrinsic_params_matrix(self):
        ox = self.px_base/2
        oy = self.px_altura/2
        fsx = self.px_base*self.dist_foc/self.ccd[0]
        fsy = self.px_altura*self.dist_foc/self.ccd[1]
        fstheta = self.stheta*self.dist_foc
        K = array([[fsx, fstheta,ox], [0,fsy, oy],[0,0,1]])
        return K
    

    def update_canvas(self):
        plt.close('all')
        object_2d = self.projection_2d()

        # Atualizar o gráfico 2D
        self.ax1.clear()
        self.ax1.set_xlim([0, self.px_base])
        self.ax1.set_ylim([self.px_altura, 0])
        self.ax1.plot(object_2d[0, :], object_2d[1, :])
        self.ax1.grid(True)
        self.ax1.set_aspect('equal')

        # Atualizar o gráfico 3D
        self.ax2.clear()
        self.ax2 = set_plot(ax=self.ax2, lim=[-15, 30])
        self.ax2.plot3D(self.house[0, :], self.house[1, :], self.house[2, :], 'red')
        draw_arrows(self.cam[:, -1], self.cam[:, 0:3], self.ax2)

        # Redesenhar os canvas
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas.layout().itemAt(1).widget().draw()
    
    def reset_canvas(self):
        self.set_variables()
        self.update_canvas()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
