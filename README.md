# Formal and Informal English Classification

formalityClassification.ipynb에 formal/informal sentence classification 실험이 모두 담겨있으며 data와 feature 파일들 또한 download하여야 한다.

텍스트 분류의 목적은 텍스트 문서를 다른 미리 정의된 클래스(여기서는 formal/informal)로 분류하는 것이다. English에서 formal(격식체) 텍스트와 informal(비격식체) 텍스트의 분류에 대한 발표된 연구는 거의 없다. 특히나 Speaking에 관한 것은 전무하다. spoken 텍스트 형식 분류에 대한 체계적인 연구는 아직까지 찾아볼 수 없기 때문에 텍스트의 formality나 informality에 어떤 핵심 요소가 기여하는지 알아보고 텍스트 스타일을 바꿀 수 있는 몇 가지 아이디어와 해결책을 찾아내는 것이 주목적이다. 모델의 개념은 스타트 학기 종료 후 수정 및 후속 연구가 가능하도록 구성하려고 노력하였다. formal/informal data에서 feature들을 추출하고 각 data에 대해 원하는 기능을 추출한 후 계층화된 k-폴드 교차 검증으로 모델을 훈련하고 검증했다. 그 후, RFECV (Recursive Feature Elimination with Cross Validation) 방법으로 formal 텍스트와 informal 텍스트를 구별할 때 feature의 subset이 필수적인지 알아보기 위해 특징을 조사한다.

# Word Frequency Count

NLTK 라이브러리를 이용하게 쉽게 단어의 빈도수를 구한다. 여기에 활용되는 data는 그 어떤 것도 상관없으나 diary sample, O Captain! My Captain!, random text를 첨부하였다. 
