**HTTP `HEAD` 메서드**는 특정 리소스를 [`GET`](https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Methods/GET) 메서드로 요청했을 때 돌아올 헤더를 요청합니다.

`HEAD` 메서드에 대한 응답은 본문을 가져선 안되며, 본문이 존재하더라도 무시해야 합니다. 그러나, [`Content-Length`](https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Headers/Content-Length)처럼 본문 콘텐츠를 설명하는 [개체 헤더](https://developer.mozilla.org/ko/docs/Glossary/Entity_header)는 포함할 수 있습니다. 이 때, 개체 헤더는 비어있어야 하는 `HEAD`의 본문과는 관련이 없고, 대신 [`GET`](https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Methods/GET) 메서드로 동일한 리소스를 요청했을 때의 본문을 설명합니다.

`HEAD` 요청의 응답이 캐시했던 이전 [`GET`](https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Methods/GET) 메서드의 응답을 유효하지 않다고 표시할 경우, 새로운 `GET` 요청을 생성하지 않더라도 캐시를 무효화합니다.

| 요청에 본문 존재                                                         | 아니오 |
| ----------------------------------------------------------------- | --- |
| 성공 응답에 본문 존재                                                      | 아니오 |
| [안전함](https://developer.mozilla.org/ko/docs/Glossary/Safe)        | 예   |
| [멱등성](https://developer.mozilla.org/ko/docs/Glossary/Idempotent)  | 예   |
| [캐시 가능](https://developer.mozilla.org/ko/docs/Glossary/Cacheable) | 예   |
| HTML 양식에서 사용 가능                                                   | 아니오 |
|                                                                   |     |

## 구문

```http
HEAD /index.html
```
