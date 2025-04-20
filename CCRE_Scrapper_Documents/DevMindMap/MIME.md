

**MIME**([영어](https://ko.wikipedia.org/wiki/%EC%98%81%EC%96%B4 "영어"): Multipurpose Internet Mail Extensions)는 [전자 우편](https://ko.wikipedia.org/wiki/%EC%A0%84%EC%9E%90_%EC%9A%B0%ED%8E%B8 "전자 우편")을 위한 인터넷 표준 포맷이다. 전자 우편은 7비트 [ASCII](https://ko.wikipedia.org/wiki/ASCII "ASCII") 문자를 사용하여 전송되기 때문에 8비트 이상의 코드를 사용하는 문자나 [이진 파일](https://ko.wikipedia.org/wiki/%EC%9D%B4%EC%A7%84_%ED%8C%8C%EC%9D%BC "이진 파일")들은 MIME 포맷으로 변환되어 [SMTP](https://ko.wikipedia.org/wiki/%EA%B0%84%EC%9D%B4_%EC%9A%B0%ED%8E%B8_%EC%A0%84%EC%86%A1_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C "간이 우편 전송 프로토콜")로 전송된다. 실질적으로 SMTP로 전송되는 대부분의 전자 우편은 MIME 형식이다. MIME 표준에 정의된 content types은 [HTTP](https://ko.wikipedia.org/wiki/HTTP "HTTP")와 같은 통신 프로토콜에서 사용되며, 점차 그 중요성이 커지고 있다.



## 개요

기본적으로 인터넷 전자 우편 전송 프로토콜인 SMTP는 7비트 [ASCII](https://ko.wikipedia.org/wiki/ASCII "ASCII") 문자만을 지원한다. 이것은 7비트 ASCII 문자로 표현할 수 없는 영어 이외의 언어로 쓰인 전자 우편은 제대로 전송될 수 없다는 것을 의미한다. MIME은 ASCII가 아닌 [문자 인코딩](https://ko.wikipedia.org/wiki/%EB%AC%B8%EC%9E%90_%EC%9D%B8%EC%BD%94%EB%94%A9 "문자 인코딩")을 이용해 영어가 아닌 다른 언어로 된 전자 우편을 보낼 수 있는 방식을 정의한다. 또한 그림, 음악, 영화, 컴퓨터 프로그램과 같은 8비트짜리 이진 파일을 전자 우편으로 보낼 수 있도록 한다. MIME은 또한 전자 우편과 비슷한 형식의 메시지를 사용하는 [HTTP](https://ko.wikipedia.org/wiki/HTTP "HTTP")와 같은 통신 프로토콜의 기본 구성 요소이다. 메시지를 MIME 형식으로 변환하는 것은 전자 우편 프로그램이나 서버 상에서 자동으로 이루어진다.

전자 우편의 기본적인 형식은 RFC 2821에서 정의하고 있다. 이 문서는 RFC 822를 대체한다. 이 문서는 텍스트 전자 우편의 헤더와 본문의 형식을 명시하고 있으며, 그중에는 우리에게 익숙한 "To:", "Subject:", "From:", "Date:" 등의 헤더가 포함되어 있다. MIME은 메시지의 종류를 나타내는 _content-type_, 메시지 인코딩 방식을 나타내는 _content-transfer-encoding_과 같은 추가적인 [전자 우편](https://ko.wikipedia.org/wiki/%EC%A0%84%EC%9E%90_%EC%9A%B0%ED%8E%B8 "전자 우편") 헤더를 정의하고 있다. MIME은 또한 ASCII가 아닌 문자를 전자 우편 헤더로 사용할 수 있도록 규정하고 있다.

MIME은 확장 가능하다. MIME 표준은 새로운 _content-type_과 또 다른 MIME 속성 값을 등록할 수 있는 방법을 정의하고 있다.

MIME의 명시적인 목표 중 하나는 기존 전자 우편 시스템과의 호환성이다. MIME을 지원하는 클라이언트에서 비 MIME가 제대로 표시될 수 있고, 반대로 MIME을 지원하지 않는 클라이언트에서 간단한 MIME 메시지가 표시될 수 있다.