# 👑 SpeaKing 👑
AI 기반 영어 말하기 분석 애플리케이션 **👑** **SpeaKing 👑**

## 🎙 프로젝트 소개

영어 자격증을 공부할 때, 영어로 업무를 처리해야할 때, 외국인과 이야기를 나눌 때 등 다양한 상황에서 영어 말하기 실력이 요구되고 있다. 그러나 한국의 영어 말하기 수준은 토플 speaking 성적을 기준으로 168개국 중 122위로 세계 하위권이며, 한국의 영어 학습자는 교실 밖에서 영어를 사용하는 일이 적을 뿐 아니라 교사에게 일대일로 피드백을 제공받기 어려운 스피킹 암흑 지대에 살고있다.


자체 진행한 설문조사에 따르면, 응답자 모두 영어 말하기 첨삭이 필요하다고 생각했지만 첨삭을 받아본 경험이 있다고 응답한 비율은 단 13% 였다. 
첨삭을 받지 않은 주된 이유로는 “어디서 어떻게 받아야 할지 모르겠다, 사람을 상대로 말하는 것이 부담스럽다, 기관을 통해 피드백을 받는 과정이 번거롭다” 가 선택되었다.

이 결과를 바탕으로 사용자가 자신의 발화속도를 확인할 수 있고, 격식/비격식체 문장을 구분할 수 있으며, 반복되는 표현을 얼마나 사용했는지 확인할 수 있는 기능을 어플리케이션에 담고자 한다. 



- [SpeaKing 시연 영상](https://youtu.be/U1pjF98pG2o)
- [SpeaKing 프로토타입](https://youtube.com/shorts/pbpJTnrToT0?feature=share)
- [SpeaKing 제품 설명서](https://www.notion.so/77ba9bb0b97b4460bd5cf4b1281eaf95)

<img width="800" src="https://user-images.githubusercontent.com/68412683/206727129-ffb64038-e4ed-4009-be13-83722bb4c059.png" />

## 🎙 예상 프로젝트 구조

<img width="800" src="https://user-images.githubusercontent.com/68412683/206727399-44b678ce-4cd4-4ea8-9783-fa6ca0523e8d.png" />

- Client: Swift(iOS)
- Server: django, SQLite 및 AWS를 사용한 배포 
- NLP: GBert

## 🎙 팀원 소개

| <img width="200" src="https://user-images.githubusercontent.com/68412683/206727368-df94675f-d152-494c-9535-b99006796519.png"/> | <img width="200" src="https://user-images.githubusercontent.com/68412683/206727359-a653906e-0847-4702-a7e4-4c1ac532bd46.png"/> | <img width="200" src="https://user-images.githubusercontent.com/68412683/206727349-a0454fb5-8b5e-446c-a3ab-c14b19b1c9b9.png"/> |
| --- | --- | --- |
| **이서영** | **이지영** | **이남영** |
| 클라이언트 | 백엔드 | NLP |

## 🎙 클라이언트

- [레포지토리](https://github.com/YoungSisters/client-lab)

## 🎙 Formal and Informal English Classification

formalityClassification.ipynb에 formal/informal sentence classification 실험이 모두 담겨있다.

jupyter notebook, Colab 등 자신이 편한 환경에서 ipynb 파일을 실행하면 굳이 코드를 돌리지 않아도 실행결과를 볼 수 있지만 만약 직접 실행을 원한다면 data와 feature 파일들 또한 download하여 데이터를 불러오는 경로를 수정해주고 실행하면 된다.

텍스트 분류의 목적은 텍스트 문서를 다른 미리 정의된 클래스로 분류하는 것이다. English에서 formal(격식체) 텍스트와 informal(비격식체) 텍스트의 분류에 대한 발표된 연구는 거의 없다. 특히나 Speaking에 관한 것은 전무하다. spoken 텍스트 형식 분류에 대한 체계적인 연구는 아직까지 찾아볼 수 없기 때문에 텍스트의 formality나 informality에 어떤 핵심 요소가 기여하는지 알아보고 텍스트 스타일을 바꿀 수 있는 몇 가지 아이디어와 해결책을 찾아내는 것이 주목적이다. 모델의 개념은 스타트 학기 종료 후 수정 및 후속 연구가 가능하도록 구성하려고 노력하였다. formal/informal data에서 feature들을 추출하고 각 data에 대해 원하는 기능을 추출한 후 계층화된 k-폴드 교차 검증으로 모델을 훈련하고 검증했다. 그 후, RFECV (Recursive Feature Elimination with Cross Validation) 방법으로 formal 텍스트와 informal 텍스트를 구별할 때 feature의 subset이 필수적인지 알아보기 위해 특징을 조사한다.

## 🎙 Word Frequency Count

wordFrequency.ipynb에 단어빈도수를 구하는 소스코드가 담겨있다. include_stopwords 파일은 불용어를 제거하지 않았을 때의 결과 파일이다.

마찬가지로 ipynb 파일로 굳이 코드를 돌리지 않아도 실행결과를 볼 수 있지만 만약 직접 실행을 원한다면 sample 파일을 download하여 데이터를 불러오는 경로를 수정하면 된다.

NLTK 라이브러리를 이용하였고 주석을 통해 단계를 구별했다.
