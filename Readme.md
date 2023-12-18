# 설진을 통한 건강상태 자가진단(Team :p)  
## 프로젝트 요약
```mermaid
graph LR
A(<b><span style='font-size:20px'>  사진 촬영  </span></b><br><br>스마트폰\nor\n웹캠 사용<br><br><br>)-->B[<b><span style='font-size:20px'>이미지 분석</span></b><br><br>OpenCV 라이브러리 활용<br><br>혓바닥, 백태 영역 분리<br>백태 영역 너비 분석<br><br>]
B-->C(<b><span style='font-size:20px'>  결과 출력  </span></b><br><br>증상 유형<br>증상 심각도<br><br>해결책 제시<br><br>)

style A fill:#EFF8FB ,stroke:#333,stroke-width:2px
style B fill:#EFF8FB ,stroke:#333,stroke-width:2px
style C fill:#EFF8FB ,stroke:#333,stroke-width:2px
```
## 구현 방법
```mermaid
graph
A(<b><span style='font-size:18px'>Image</span></b>)-->B[<b><span style='font-size:20px'>Resize<br>640 * 640</span></b>]
B-->C[<b><span style='font-size:18px'>Homomorphic<br>Filtering</span></b>]
C-->D1[<b><span style='font-size:18px'>Resize<br>120 * 120</span></b>]
D1-->E1[<b><span style='font-size:18px'>Meanshift<br>영역분할</span></b>]
E1-->F1[<b><span style='font-size:18px'>Gaussian<br>Smoothing</span></b>]
F1-->G[<b><span style='font-size:18px'>Canny<br>Edge 검출</span></b>]
G-->H[<b><span style='font-size:18px'>Dilate<br>&<br>Erode</span></b>]
H-->I[<b><span style='font-size:18px'>Resize<br>640 * 640</span></b>]
I-->J[<b><span style='font-size:18px'>Binarization</span></b>]

C-->D2[<b><span style='font-size:18px'>Resize<br>640 * 640</span></b>]
D2-->E2[<b><span style='font-size:18px'>HSV기준 배경제거</span></b>]
E2-->F2[<b><span style='font-size:18px'>전경 공백<br>Interpolation</span></b>]

J-->K
F2-->K[<b><span style='font-size:18px'>if img_bin==0:<br>img_h=0</span></b>]
K-->L[<b><span style='font-size:18px'>Labeling</span></b>]
L-->M[<b><span style='font-size:18px'>이미지의 중앙<br>Label만 선택</span></b>]
M-->N[<b><span style='font-size:18px'>Label 공백<br>Interpolation</span></b>]
N-->O1[<b><span style='font-size:18px'>상하 영역 분할<br>기준점 탐색</span></b>]

C-->O2
N-->O2[<b><span style='font-size:18px'>img_homomorphic에<br>Label 적용</span></b>]


style A fill:#EFF8FB ,stroke:#333,stroke-width:2px
style B fill:#EFF8FB ,stroke:#333,stroke-width:2px
style C fill:#EFF8FB ,stroke:#333,stroke-width:2px
style D1 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style E1 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style F1 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style G fill:#EFF8FB ,stroke:#333,stroke-width:2px
style H fill:#EFF8FB ,stroke:#333,stroke-width:2px
style I fill:#EFF8FB ,stroke:#333,stroke-width:2px
style J fill:#EFF8FB ,stroke:#333,stroke-width:2px

style D2 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style E2 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style F2 fill:#EFF8FB ,stroke:#333,stroke-width:2px

style K fill:#EFF8FB ,stroke:#333,stroke-width:2px
style L fill:#EFF8FB ,stroke:#333,stroke-width:2px
style M fill:#EFF8FB ,stroke:#333,stroke-width:2px
style N fill:#EFF8FB ,stroke:#333,stroke-width:2px
style O1 fill:#EFF8FB ,stroke:#333,stroke-width:2px

style O2 fill:#EFF8FB ,stroke:#333,stroke-width:2px
```
## 실제 동작
