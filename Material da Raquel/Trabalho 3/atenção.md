ATENÇÃO - MUITO IMPORTANTE
Raquel Frizera Vassallo
•
Ontem
Nos arquivos .json que contém os dados de calibração das câmeras do espaço inteligente, a matriz de rotação e translação que representam os parâmetros extrínsecos representam a transformação [R,T] que converte do referencial da câmera para o mundo.
Para resolver o trabalho, de acordo com o modelo de projeção pinhole, vocês precisam da transformação que converte do mundo para a câmera, ou seja, do inverso da matriz fornecida. Então..... ATENÇÃO!!!!!

Vocês devem extrair os dados de R e T, montar a matriz de transformação geométrica e invertê-la antes de usar.
Depois de inverter, a matrix representa a transformação que converte do mundo para a câmera, ou seja, o R e T que vocês precisam. 

Outro detalhe importante, filtrem as detecções de ArUco para o ID = 0 (zero), pois às vezes ocorre a detecção de outros IDs e isso pode causar problemas para vocês.