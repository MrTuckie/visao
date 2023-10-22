# Trabalho 1 de Visão

Feito por Arthur Lorencin e João Bimbato


## Tarefas do Arthur
Lista:
- Colocar o donkey kong
- Mover novamente para ver o donkey kong
## Tarefas do bimbato
Lista:
- lidar a projeção 2d
- tirar as funções inúteis tipo generate_projection_matrix,

# Parâmetros de Entrada

## Câmera
['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']
## Mundo
['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']
## Parâmetros Intrísecos da Câmera
['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:', 'dist_focal:', 'sθ:']
# TODO

DICA: No código, procure por TODO nos comentários

## Funções genéricas

- [ ] Importar o arquivo .stl do donkey kong
- [ ] Plotar o donkey kong




## Funções para serem alteradas

set_variables:
- [ ] Alterar as variáveis da câmera

create_matplotlib_canvas:
- [ ] Acertar os limites do eixo X
- [ ] Acertar os limites do eixo Y
- [ ] Criar a função de projeção que retorna um object_2d.
- [ ] Plotar o object_2d.
- [ ] Falta plotar o seu objeto 3D e os referenciais da câmera e do mundo

## Funções para serem criadas para a classe MainWindow

update_params_intrinsc:
- [ ]

update_world:
- [ ]

update_cam:<br>
Essa função é chamada em create_cam_widget quando o botão de atualizar é clicado.
- [ ]

projection_2d:<br>
Essa função é chamada em create_matplotlib_canvas e deve retornar um objeto.
- [ ]

generate_intrinsic_params_matrix:
- [ ]

update_canvas:
- [ ]

reset_canvas:
- [ ]


## Descrição do trabalho

Nesse primeiro trabalho vocês deverão fazer um programa onde será possível:

- Visualizar a posição e orientação tridimensional de uma câmera e de um objeto.

- Alterar a posição e orientação da câmera (parâmetros extrínsecos) através de translações e rotações tridimensionais. 
  ATENÇÃO: O objeto não precisa ser movimentado, apenas a câmera.

- As translações e rotações poderão ser feitas tanto em relação ao referencial do mundo quanto em relação ao referencial próprio da câmera.

- Visualizar a imagem do objeto gerada pela câmera.

- Alterar os parâmetros intrínsecos da câmera (distância focal e fator de escala de cada eixo). O ponto principal será alterado automaticamente quando o tamanho da imagem ou sensor for alterado.
ATENÇÃO: A origem dos eixos da imagem deve estar no canto superior esquerdo!!! 

- Toda vez que algo for alterado, a visualização 3D e a imagem gerada pela câmera deverão ser atualizadas.

O trabalho poderá ser feito em dupla e deverá ser feito usando a linguagem Python e deverá ser entregue como arquivos .py

Vocês deverão me devolver o trabalho através do Google Classroom ou, caso haja problemas, enviá-lo para raquel.vassallo@ufes.br 
Lembrem-se de enviar todos os arquivos necessários para a execução do trabalho. 


Data de entrega: 20/10/2023