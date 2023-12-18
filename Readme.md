# 설진을 통한 건강상태 자가진단(Team :p)  
## 프로젝트 요약
```mermaid
graph LR
A(<b><span style='font-size:20px'>  사진 촬영  </span></b><br><br>스마트폰\nor\n웹캠 사용<br><br><br>)-->B[<b><span style='font-size:20px'>이미지 분석</span></b><br><br>OpenCV 라이브러리 활용<br><br>혓바닥, 백태 영역 분리<br>백태 영역 너비 분석<br><br>]
B-->C[<b><span style='font-size:20px'>  결과 출력  </span></b><br><br>증상 유형<br>증상 심각도<br><br>해결책 제시<br><br>]

style A fill:#EFF8FB ,stroke:#333,stroke-width:2px
style B fill:#EFF8FB ,stroke:#333,stroke-width:2px
style C fill:#EFF8FB ,stroke:#333,stroke-width:2px
```
## 구현 방법
```mermaid
graph
A[<b><span style='font-size:20px'>Image</span></b>]-->B[<b><span style='font-size:20px'>Resize<br>640 * 640</span></b>]
B-->C[<b><span style='font-size:20px'>Homomorphic<br>Filtering</span></b>]
C-->D[<b><span style='font-size:20px'>Resize<br>120 * 120</span></b>]
D-->E[<b><span style='font-size:20px'>Meanshift<br>영역분할</span></b>]
E-->F[<b><span style='font-size:20px'>Gaussian<br>Smoothing</span></b>]
F-->G[<b><span style='font-size:20px'>Canny<br>Edge 검출</span></b>]
G-->H[<b><span style='font-size:20px'>Dilate<br>&<br>Erode</span></b>]
H-->I[<b><span style='font-size:20px'>Resize<br>640 * 640</span></b>]


style A fill:#EFF8FB ,stroke:#333,stroke-width:2px
style B fill:#EFF8FB ,stroke:#333,stroke-width:2px
style C fill:#EFF8FB ,stroke:#333,stroke-width:2px
style D fill:#EFF8FB ,stroke:#333,stroke-width:2px
style E fill:#EFF8FB ,stroke:#333,stroke-width:2px
style F fill:#EFF8FB ,stroke:#333,stroke-width:2px
style G fill:#EFF8FB ,stroke:#333,stroke-width:2px
style H fill:#EFF8FB ,stroke:#333,stroke-width:2px
style I fill:#EFF8FB ,stroke:#333,stroke-width:2px
```
## 실제 동작
