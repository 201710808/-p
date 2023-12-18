# 설진을 통한 건강상태 자가진단(Team :p)  
## 프로젝트 요약
```mermaid
graph LR
A[<b><span style='font-size:20px'>  사진 촬영  </span></b><br><br>스마트폰\nor\n웹캠 사용<br><br><br>]-->B[<b><span style='font-size:20px'>이미지 분석</span></b><br><br>OpenCV 라이브러리 활용<br><br>혓바닥, 백태 영역 분리<br>백태 영역 너비 분석<br><br>]
B-->C[<b><span style='font-size:20px'>  결과 출력  </span></b><br><br>증상 유형<br>증상 심각도<br><br>해결책 제시<br><br>]

style A fill:#EFF8FB ,stroke:#333,stroke-width:2px
style B fill:#EFF8FB ,stroke:#333,stroke-width:2px
style C fill:#EFF8FB ,stroke:#333,stroke-width:2px
```
## 구현 방법
```mermaid
graph
A[<b><span style='font-size:20px'>Image</span></b>]-->B[<b><span style='font-size:20px'>Resize<br>640 * 640</span></b>]
B-->C1[<b><span style='font-size:20px'>R</span></b>]
B-->C2[<b><span style='font-size:20px'>G</span></b>]
B-->C3[<b><span style='font-size:20px'>B</span></b>]
C1-->D[<b><span style='font-size:20px'>Homomorphic filtering</span></b>]
D-->E1[<b><span style='font-size:20px'>H</span></b>]
D-->E2[<b><span style='font-size:20px'>S</span></b>]
D-->E3[<b><span style='font-size:20px'>V</span></b>]


style A fill:#EFF8FB ,stroke:#333,stroke-width:2px
style B fill:#EFF8FB ,stroke:#333,stroke-width:2px
style C1 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style C2 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style C3 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style D fill:#EFF8FB ,stroke:#333,stroke-width:2px
style E1 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style E2 fill:#EFF8FB ,stroke:#333,stroke-width:2px
style E3 fill:#EFF8FB ,stroke:#333,stroke-width:2px
```
## 실제 동작
