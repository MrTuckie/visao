Nesta atividade vocês deverão fazer a reconstrução 3D da caixa fotografada nas duas imagens.
Para isso, vocês usarão o material postado logo abaixo:

1. O par de imagens da câmera esquerda e direita, já retificadas. São os arquivos "esquerda.ppm" e "direita.ppm"
2. Os dados de calibração da câmera, assim como o deslocamento entre as duas câmeras. Tais dados estão no arquivo "box_data.py"
3. Duas rotinas que calculam o mapa de disparidade entre as duas imagens. Vocês poderão usar a rotina baseada apenas na Correlação Cruzada Normalizada ou a rotina baseda na Correlação Cruzada Normalizada com filtro Gaussiano. Testem e vejam qual vocês acham melhor para o seu trabalho. Tais rotinas podem ser encontradas nos arquivos do  "Material em Python e Google Colab - No.13" - depth_map.py ou depth_map.ipynb

Como tarefas deste trabalho vocês deverão:

1. Calcular e mostrar o mapa de disparidade entre as imagens retificadas
2. Realizar a reconstrução da profundidade Z, usando o método de reconstrução com imagens retificadas visto na Aula 11. A seguir, realizar a reconstrução das coordenadas X e Y.
3. Plotar a reconstrução colorindo cada ponto reconstruído com a cor de seu pixel correspondente. Um exemplo de como selecionar as cores dos pixels e usar na reconstrução pode ser visto em "Material em Python e Google Colab - No.13" - sparse_reconstruction01.py ou sparse_reconstruction01.ipynb

Obs: Caso queiram, vocês podem realizar a reconstrução de apenas um pedaço da imagem selecionando uma região de interesse (ROI - Region of Interest). Para selecionar uma ROI vocês podem usar a função "cv2.selectROI(image)" do OpenCV.


A reconstrução que vocês obtiverem deve ser semelhante às imagens mostradas nos arquivos Result01.png, Result02.png e Result03.png . Atenção: tais imagens são apenas para que vocês possam comparar com o resultado de vocês. Não deverão ser usadas para nada no trabalho.