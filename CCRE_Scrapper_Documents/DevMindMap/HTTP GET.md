
**HTTP `GET` 메서드**는 특정한 리소스를 가져오도록 요청합니다. `GET` 요청은 데이터를 가져올 때만 사용해야 합니다.

**참고 :**

`GET` 요청에 본문이나 페이로드가 담겨있으면 명세에는 금지되어있지 않지만, 의미가 정의되지 않아 기존에 존재하는 구현체에게 요청을 거부당할수 있습니다. 이러한 이유로 `GET` 요청에는 본문이나 페이로드를 담지 않는 것이 바람직합니다.

| 요청에 본문 존재                                                         | 아니오 |
| ----------------------------------------------------------------- | --- |
| 성공 응답에 본문 존재                                                      | 예   |
| [안전함](https://developer.mozilla.org/ko/docs/Glossary/Safe)        | 예   |
| [멱등성](https://developer.mozilla.org/ko/docs/Glossary/Idempotent)  | 예   |
| [캐시 가능](https://developer.mozilla.org/ko/docs/Glossary/Cacheable) | 예   |
| HTML 양식에서 사용 가능                                                   | 예   |

## 구문

```http
GET /index.html
```
